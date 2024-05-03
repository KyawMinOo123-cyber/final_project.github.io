# Generated by Django 5.0.2 on 2024-05-03 05:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_company', '0004_job_application_form_applied_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_application_form',
            name='applied_users',
        ),
        migrations.AddField(
            model_name='career',
            name='applied_users',
            field=models.ManyToManyField(related_name='job_applications', to=settings.AUTH_USER_MODEL),
        ),
    ]
