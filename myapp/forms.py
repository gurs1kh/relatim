from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url',)
		widgets = {
			'title': forms.TextInput(attrs={
				'type':'text',
				'id':'title-input',
				'name':'title-input',
				'placeholder':'insert title...',
				'class':'form-control input-md',
			}),

			'url': forms.TextInput(attrs={
				'type':'text',
				'id':'url-input',
				'name':'url-input',
				'placeholder':'http://...',
				'class':'form-control input-md',
			}),
		}
