from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
import os

# Create your models here.

class Career(models.Model):
    title = models.CharField(max_length = 100)
    job_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def serialize(self):
        return{
            "id":self.id,
            "title":self.title,
            "job_description":self.job_description,
        }


class CareerProfie(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    applied_careers = models.ManyToManyField(Career , default = None,related_name = "careers")

class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Position: {self.name}"


class Team(models.Model):
    name = models.CharField(max_length = 10)

    def __str__(self):
        return f"Team: {self.name}"


class Gender(models.Model):
    name = models.CharField(max_length = 10)

    def __str__(self):
        return f"Gender: {self.name}"


class Department(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return f"Department: {self.name}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    positions = models.ManyToManyField(Position, related_name = "employees" )
    teams = models.ManyToManyField(Team , related_name = "employees")
    genders = models.ManyToManyField(Gender , related_name = "employees")
    departments = models.ManyToManyField(Department , related_name = "employees") 
    salary = models.DecimalField(max_digits = 10, decimal_places = 2)
    address = models.TextField()
    contact_number = models.CharField(max_length = 20)
    hiring_date = models.DateTimeField(default = timezone.now)
    hired = models.BooleanField(default = False)
    
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
    job_applier = models.OneToOneField(User,on_delete = models.CASCADE , related_name = "applier")
    position = models.CharField(max_length = 100)
    expected_salary = models.DecimalField(max_digits = 10, decimal_places = 2)
    contact_number = models.CharField(max_length = 20)
    cover_letter = models.TextField()
    apply_date = models.DateTimeField(default = timezone.now)
    hire = models.BooleanField(default = False)
    reject = models.BooleanField(default = False)

                                                                                                                                                                                                                            