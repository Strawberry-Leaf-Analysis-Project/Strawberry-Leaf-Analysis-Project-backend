# Generated by Django 4.1.5 on 2023-01-03 07:26

import board.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('key', models.AutoField(db_column='key', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='title', max_length=100)),
                ('explain', models.CharField(db_column='explain', max_length=500)),
                ('user_key', models.IntegerField(db_column='user_key')),
                ('image', models.ImageField(db_column='image', upload_to=board.models.user_directory_path)),
                ('date', models.DateTimeField(db_column='date')),
                ('views', models.IntegerField(db_column='views')),
                ('like', models.IntegerField(db_column='like')),
                ('disease', models.CharField(db_column='disease', max_length=100)),
                ('growth', models.CharField(db_column='growth', max_length=100)),
                ('is_delete', models.IntegerField(db_column='is_delete')),
            ],
            options={
                'db_table': 'board',
                'managed': False,
            },
        ),
    ]