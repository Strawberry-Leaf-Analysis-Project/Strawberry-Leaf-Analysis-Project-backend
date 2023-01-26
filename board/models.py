from datetime import datetime
from pytz import timezone

from django.db import models
from member.models import Member
from plants_group.models import PlantsGroup
#이미지 저장 경로 지정 함수
def user_directory_path(instance,filename):
    name='input_image.jpg'
    b_id=str(instance.id)
    return 'image/{0}/{1}/{2}/{3}'.format(instance.user.id,instance.plant_group.name,instance.user.board_cnt,name)

class Board(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,null=True)
    explain = models.CharField(max_length=500,null=True)
    date = models.DateTimeField(default=datetime.now)
    input_image = models.ImageField(upload_to=user_directory_path,null=True)
    output_image = models.FileField(upload_to=user_directory_path,null=True) #위치 지정해야하는데 나중에 설정해야할듯?
    views=models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    leaf_cnt = models.IntegerField(default=0)
    is_delete=models.CharField(max_length=1,default='0')
    is_writing = models.CharField(max_length=1, default='1')
    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    plant_group=models.ForeignKey(PlantsGroup,on_delete=models.CASCADE,null=True)
    class Meta:
        managed = True
        db_table = "board"

    def __str__(self):
        return "제목 : "+self.title+"설명 : "+self.explain