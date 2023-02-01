from django.db import models
from member.models import Member
from datetime import datetime

class PlantsGroup(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200,null=False)
    status=models.CharField(max_length=1,default='0')
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    board_cnt=models.IntegerField(default=0)
    class Meta:
        managed = True
        db_table = "plants_group"

    def __str__(self):
        return "그룹명 : "+self.name+"상태 : "+self.status