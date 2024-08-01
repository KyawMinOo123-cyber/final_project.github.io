from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
import os

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length = 10)

    def serialize(self):
        return { 
            "id":self.id,
            "name":self.name
            }

class Career(models.Model):
    title = models.CharField(max_length = 100)
    job_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    applied_users = models.ManyToManyField(User, related_name = "job_applications")

    def serialize(self, applied = False):
        data = {
            "id":self.id,
            "title":self.title,
            "job_description":self.job_description,
            "applied":applied
        }
        return data

class CareerProfie(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    applied_careers = models.ManyToManyField(Career , default = None,related_name = "careers")

class Employee(models.Model):
    applier = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.TextField(max_length = 20,blank = True, null = True)
    positions = models.TextField(blank = True, null = True )
    team = models.TextField( blank = True, null = True)
    gender = models.TextField( blank = True, null = True)
    department = models.TextField( blank = True, null = True) 
    salary = models.DecimalField(max_digits = 100, decimal_places = 2)
    address = models.TextField()
    contact_number = models.CharField(max_length = 20)
    hiring_date = models.DateTimeField(default = timezone.now)
    hired = models.BooleanField(default = False)

    def serialize(self):
        return{
            "id":self.id,
            "applier":{
                "id":self.applier.id,
                "username":self.applier.username,
                "email":self.applier.email,
                "first_name":self.applier.first_name,
                "last_name":self.applier.last_name
            },
            "name":self.name,
            "position":self.positions,
            "team":self.team,
            "gender":self.gender,
            "department":self.department,
            "salary":self.salary,
            "address":self.address,
            "contact_number":self.contact_number,
            "hiring_date":self.hiring_date,
            "hired":self.hired
        }
    
##Migration still needed
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "image":self.image.url
        }


@receiver(pre_delete, sender=Service)
def delete_service_image(sender, instance, **kwargs):
    # Check if the image exists
    if instance.image:
        # Delete the image file from the file system
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Job_application_form(models.Model):
    applying_user = models.OneToOneField(User,on_delete = models.CASCADE,blank = True, null = True)
    job_applier = models.CharField( max_length = 25)
    position = models.CharField(max_length = 100)
    expected_salary = models.DecimalField(max_digits = 100, decimal_places = 2)
    contact_number = models.CharField(max_length = 20)
    cover_letter = models.TextField()
    apply_date = models.DateTimeField(default = timezone.now)
    timestamp = models.DateTimeField(auto_now_add = True,blank = True, null = True)
    interview = models.BooleanField(default = False)

    def serialize(self):
        return{
            "id":self.id,
            "applying_user":{
                "id": self.applying_user.id,
                "username": self.applying_user.username,
                "email": self.applying_user.email,
                "first_name": self.applying_user.first_name,
                "last_name": self.applying_user.last_name
            } if self.applying_user else None,
            "job_applier":self.job_applier,
            "position":self.position,
            "expected_salary":self.expected_salary,
            "contact_number":self.contact_number,
            "cover_letter":self.cover_letter,
            "apply_date":self.apply_date,
            "timestamp":self.timestamp,
            "interview":self.interview
        }     

class Interviewing_form(models.Model):
    interviewing = models.ManyToManyField(Job_application_form,related_name = "interview_forms")   
     

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = models.TextField(max_length = 200)
    create_at = models.DateTimeField(auto_now_add = True)
    is_read = models.BooleanField(default = False)

    def __str__(self):
        return f"Notification for {self.user.username}"
                                                                                                            