import requests, json
imageurl = 'http://playground.imagga.com/static/img/example_photo.jpg'
imagga_url = "http://api.imagga.com/v1/tagging"                                
querystring = {'url': imageurl, 'version': '2'}
headers = {
	'accept': "application/json",
	'authorization': "Basic YWNjXzQ0ODZkZjA5ODg5YTczYzplOTFlMzllNzA4ZGVjYjQxNjk5YTY2MTdhNThiZWM3OA=="
}
r = requests.request('GET', imagga_url, headers=headers, params=querystring)
json1 = r.json()['results'][0]['tags']
tag_len = len(json1)
tags = []
for i in range(0, tag_len - 1):
	tags.append(json1[i]['tag'])
count = 0
related_images = []
r2 = requests.request('get',  "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + ' '.join(tags))
json2 = r2.json()['responseData']['results'];
while count < 50 and len(tags):
	r2 = requests.request('get',  "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + ' '.join(tags))
	json2 = r2.json()['responseData']['results'];
	related_len = len(json2)
	tags.pop()
	for i in range(0, related_len - 1):
		if (count >= 50):
			i = related_len
		else:
			related_images.append({'url': json2[i]['url'], 'thumbnail': json2[i]['tbUrl']})
			count += 1

print(json.dumps(related_images))
