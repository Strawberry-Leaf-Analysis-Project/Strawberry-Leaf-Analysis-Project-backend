from datetime import datetime

from django.db import models
from member.models import Member
#이미지 저장 경로 지정 함수
def user_directory_path(instance,filename):
    name=instance.date.strftime("%Y-%m-%d-%H:%M:%S")+filename.split('.')[-1]
    return 'image/{0}/{1}.jpg'.format(instance.user.id,name)

class Board(models.Model):
    key=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    explain = models.CharField(max_length=500)
    user= models.ForeignKey(Member,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to=user_directory_path)
    result = models.ImageField(upload_to='',null=True)
    date=models.DateTimeField(default=datetime.now)
    views=models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    disease = models.CharField(max_length=100,null=True)
    growth = models.CharField(max_length=100,null=True)
    is_delete=models.CharField(max_length=1,default='0')

    class Meta:
        managed = True
        db_table = "board"

    def __str__(self):
        return "제목 : "+self.title+"설명 : "+self.explain