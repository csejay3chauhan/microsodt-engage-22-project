# Generated by Django 3.0.5 on 2020-07-02 06:57

import attendence_sys.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendence_sys', '0014_auto_20200702_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=attendence_sys.models.user_directory_path),
        ),
    ]