from django.db import models
from django.utils import timezone
from jsonfield import JSONField
import requests, json

class Image(models.Model):
	title = models.CharField(max_length=70)
	url = models.CharField(max_length=2083)
	related_images = JSONField()
	created_date = models.DateTimeField(default=timezone.now())

	def publish(self):
		if not self.url.startswith("http"):
			self.url = "http://" + self.url
		imagga_url = "http://api.imagga.com/v1/tagging"
		querystring = {'url': self.url, 'version': '2'}
		headers = {
			'accept': "application/json",
			'authorization': "Basic YWNjXzQ0ODZkZjA5ODg5YTczYzplOTFlMzllNzA4ZGVjYjQxNjk5YTY2MTdhNThiZWM3OA=="
		}
		r = requests.request('GET', imagga_url, headers=headers, params=querystring)
		data = r.json()['results'][0]['tags']
		tag_len = len(data)
		tags = []
		for i in range(0, tag_len - 1):
			tags.append(data[i]['tag'])
		count = 0
		related_images = []
		r2 = requests.request('get', "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + ' '.join(tags))
		data2 = r2.json()['responseData']['results'];
		while count < 50 and len(tags):
			r2 = requests.request('get', "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + ' '.join(tags))
			data2 = r2.json()['responseData']['results'];
			related_len = len(data2)
			tags.pop()
			for i in range(0, related_len - 1):
				if (count >= 50):
					i = related_len
				else:
					related_image = {'url': data2[i]['url'], 'thumbnail': data2[i]['tbUrl']}
					contains_image = False
					for j in range(0, len(related_images)- 1):
						if related_images[j] == related_image:
							contains_image = True
					if not contains_image:
						related_images.append(related_image)
						count += 1
		self.related_images = json.dumps(related_images)
		self.save()
	
	def __str__(self):
		return self.title
