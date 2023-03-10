# Generated by Django 4.1.5 on 2023-01-26 18:35

import board.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("plants_group", "0001_initial"),
        ("member", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=100, null=True)),
                ("explain", models.CharField(max_length=500, null=True)),
                ("date", models.DateTimeField(default=datetime.datetime.now)),
                (
                    "input_image",
                    models.ImageField(
                        null=True, upload_to=board.models.user_directory_path
                    ),
                ),
                (
                    "output_image",
                    models.FileField(
                        null=True, upload_to=board.models.user_directory_path
                    ),
                ),
                ("views", models.IntegerField(default=0)),
                ("likes", models.IntegerField(default=0)),
                ("leaf_cnt", models.IntegerField(default=0)),
                ("is_delete", models.CharField(default="0", max_length=1)),
                ("is_writing", models.CharField(default="0", max_length=1)),
                (
                    "plant_group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plants_group.plantsgroup",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="member.member",
                    ),
                ),
            ],
            options={"db_table": "board", "managed": True,},
        ),
    ]
