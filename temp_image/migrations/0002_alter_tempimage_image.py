# Generated by Django 4.1.5 on 2023-01-26 07:45

from django.db import migrations, models
import temp_image.models


class Migration(migrations.Migration):

    dependencies = [
        ("temp_image", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tempimage",
            name="image",
            field=models.FileField(upload_to=temp_image.models.user_directory_path),
        ),
    ]
