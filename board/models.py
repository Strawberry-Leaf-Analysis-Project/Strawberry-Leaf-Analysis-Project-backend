from datetime import datetime

from django.db import models

#이미지 저장 경로 지정 함수
def user_directory_path(instance,filename):
    name=instance.date.strftime("%Y-%m-%d-%H:%M:%S")+filename.split('.')[-1]
    return 'image/{0}/{1}.jpg'.format(instance.user_key,name)

class Board(models.Model):
    key=models.AutoField(db_column='key',primary_key=True)
    title=models.CharField(db_column='title',max_length=100)
    explain = models.CharField(db_column='explain', max_length=500)
    user_key = models.IntegerField(db_column='user_key')
    image = models.ImageField(db_column='image',upload_to=user_directory_path)
    #result = models.ImageField(db_column='result')
    date=models.DateTimeField(db_column='date')
    views=models.IntegerField(db_column='views')
    like = models.IntegerField(db_column='like')
    disease = models.CharField(db_column='disease', max_length=100)
    growth = models.CharField(db_column='growth', max_length=100)
    is_delete=models.IntegerField(db_column='is_delete')

    class Meta:
        managed = False
        db_table = "board"

    def __str__(self):
        return "제목 : "+self.title+"설명 : "+self.explain