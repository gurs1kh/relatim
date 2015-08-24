from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Image
from .forms import ImageForm
import requests, json

@login_required(login_url="/relatim/login")
def image_list(request):
	images = Image.objects.order_by('created_date')
	form = ImageForm()
	return render(request, 'relatim/image_list.html', {'images': images, 'form': form})

@login_required(login_url="/relatim/login")
def image_page(request, id):
	image = Image.objects.get(pk=id)
	related_images = json.loads(image.related_images);
	return render(request, 'relatim/image_page.html', {'image': image, 'related_images': related_images})

@login_required(login_url="/relatim/login")
def image_add(request):
	form = ImageForm(request.POST)
	if form.is_valid():
		image = form.save(commit=False)
		if not image.url.startswith("http"):
			image.url = "http://" + image.short_url
		
		imagga_url = "http://api.imagga.com/v1/tagging"
		querystring = {'url': image.url, 'version': '2'}
		headers = {
			'accept': "application/json",
<<<<<<< HEAD
			'authorization': "Basic YWNjXzQ0ODZkZjA5ODg5YTczYzplOTFlMzllNzA4ZGVjYjQxNjk5YTY2MTdhNThiZWM3OA=="
=======
			'authorization': "Basic YWNjX2FmMWM5MjI3NDMyMDUxMTplY2E4Y2Y2YmRlNGVjMTEzZjZhYTcwMWU4YzczMjNjMA=="
>>>>>>> 7fed6307bc9559a6e269985f6697571c6d7531c0
		}
		r = requests.request('GET', imagga_url, headers=headers, params=querystring)
		data = r.json()['results'][0]['tags']
		tag_len = len(data)
		tags = []
		for i in range(0, tag_len - 1):
			tags.append(data[i]['tag'])
		count = 0
		related_images = []
		r2 = requests.request('get',  "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + ' '.join(tags))
		data2 = r2.json()['responseData']['results'];
		while count < 50 and len(tags):
			r2 = requests.request('get',  "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + ' '.join(tags))
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
						if related_images[j]['url'] == related_image['url'] or related_images[j]['thumbnail'] == related_image['thumbnail']:
							contains_image = True
					if not contains_image:
						related_images.append(related_image)
						count += 1

		image.related_images = json.dumps(related_images)
				
		image.save()
	return redirect('myapp.views.image_list')

@login_required(login_url="/relatim/login")
def image_delete(request, id):
	Image.objects.get(pk=id).delete()
	return redirect('myapp.views.image_list')

