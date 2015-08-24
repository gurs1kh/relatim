from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Image
from .forms import ImageForm
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mysite.serializers import ImageSerializer
from ratelimit.decorators import ratelimit

def logout_view(request):
	logout(request)
	return redirect('myapp.views.image_list')

@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
def image_list(request):
	images = Image.objects.order_by('created_date')
	form = ImageForm()
	return render(request, 'relatim/image_list.html', {'images': images, 'form': form})

@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
def image_page(request, id):
	image = Image.objects.get(pk=id)
	related_images = json.loads(image.related_images);
	return render(request, 'relatim/image_page.html', {'image': image, 'related_images': related_images})

@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
def image_add(request):
	form = ImageForm(request.POST)
	if form.is_valid():
		image = form.save(commit=False)
		image.publish()
		image.save()
	return redirect('/relatim/id/%d' % image.id)

@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
def image_delete(request, id):
	Image.objects.get(pk=id).delete()
	return redirect('myapp.views.image_list')

@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET'])
def api_list(request, format=None):
	images = Image.objects.all()
	serializer = ImageSerializer(images, many=True)
	return Response(serializer.data)
 
@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET'])
def api_details(request, id, format=None):
	try:
		image = Image.objects.get(pk=id)
	except Image.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	serializer = ImageSerializer(image)
	return Response(serializer.data)
 
@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET'])
def api_delete(request, id):
	Image.objects.get(pk=id).delete()
	return redirect('api_list') 

@login_required(login_url="/relatim/login")
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['POST'])
def api_add(request):
	form = ImageForm(request.data)
	if form.is_valid():
		image = form.save(commit=False)
		image.publish()
		image.save()
		serializer = ImageSerializer(image)
		return Response(serializer.data) 
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)
