from django.db import models
from django.utils import timezone
from jsonfield import JSONField

class Image(models.Model):
	title = models.CharField(max_length=70)
	url = models.CharField(max_length=2083)
	related_images = JSONField()
	created_date = models.DateTimeField(default=timezone.now)
	
	def publish(self):
		self.save()
	
	def __str__(self):
		return self.title
