# Generated by Django 4.1.5 on 2023-01-26 18:35

from django.db import migrations, models
import django.db.models.deletion
import plants_detail.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlantsDetail",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_disease", models.CharField(default="0", max_length=1)),
                (
                    "leaf_image",
                    models.FileField(
                        null=True, upload_to=plants_detail.models.user_directory_path
                    ),
                ),
                (
                    "board",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="board.board",
                    ),
                ),
            ],
            options={"db_table": "plants_detail", "managed": True,},
        ),
    ]
