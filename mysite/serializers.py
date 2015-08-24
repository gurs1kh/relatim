from django.forms import widgets
from rest_framework import serializers
from myapp.models import Image

class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = ('id', 'title', 'url', 'related_images', 'created_date')
