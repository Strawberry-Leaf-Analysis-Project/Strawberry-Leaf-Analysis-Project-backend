from datetime import datetime

from django.db import models
from board.models import Board
#이미지 저장 경로 지정 함수(변경필요)
def user_directory_path(instance,filename):
    name=instance.board.date.strftime("%Y-%m-%d-%H:%M:%S")+filename.split('.')[-1]
    return 'image/{0}/{1}/{2}.jpg'.format(instance.board.user.id,instance.board.plant_group.name,name)

class PlantsDetail(models.Model):
    id=models.AutoField(primary_key=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE, null=True)
    leaf_image=models.ImageField(upload_to=user_directory_path,null=False)

    class Meta:
        managed = True
        db_table = "plants_detail"

'''
    def __str__(self):
        return "제목 : "+self.title+"설명 : "+self.explain
'''