from django import forms
from .models import Service,Career,Job_application_form

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description' , 'image']


class CareerForm(forms.ModelForm):
    class Meta:
        model = Career
        fields = ['title','job_description']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = Job_application_form
        exclude = ['hire','reject']
        fields = ['job_applier','position','expected_salary','contact_number','cover_letter','apply_date']
