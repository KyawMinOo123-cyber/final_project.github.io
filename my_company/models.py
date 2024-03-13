from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
import os

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    


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


