from django import forms
from .models import Service,Career

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description' , 'image']


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['title','job_description']
