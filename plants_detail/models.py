from datetime import datetime

from django.db import models
from board.models import Board
#이미지 저장 경로 지정 함수(변경필요)
def user_directory_path(instance,filename):
    return 'image/{0}/{1}/{2}/{3}'.format(instance.board.user.id,instance.board.plant_group.name,instance.board.plant_group.board_cnt,filename)

class PlantsDetail(models.Model):
    id=models.AutoField(primary_key=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE, null=True)
    is_disease = models.CharField(max_length=1, default='0')
    leaf_image=models.FileField(upload_to=user_directory_path,null=True)

    class Meta:
        managed = True
        db_table = "plants_detail"

'''
    def __str__(self):
        return "제목 : "+self.title+"설명 : "+self.explain
'''