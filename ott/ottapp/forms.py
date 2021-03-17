from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm

class AddMovieForm(forms.Form):
    movie_name = forms.CharField(required=False)
    poster = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpeg','png', 'jpg'])],required=False)
    genre = forms.CharField(required=False)
    release_date = forms.DateField(required=False)
    ratting = forms.FloatField(required=False)
    running_time = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea,required=False)
    video = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])],required=False)
    trailer = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])],required=False)