# Generated by Django 5.0.2 on 2024-04-29 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_application_form',
            name='hire',
        ),
        migrations.RemoveField(
            model_name='job_application_form',
            name='reject',
        ),
    ]
