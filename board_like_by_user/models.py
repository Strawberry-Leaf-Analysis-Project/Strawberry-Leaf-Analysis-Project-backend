from django.db import models
from member.models import Member
from board.models import Board

class BoardLikeByUser(models.Model):
    id=models.AutoField(primary_key=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE,null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    is_delete=models.CharField(max_length=1,default='0')

    class Meta:
        managed = True
        db_table = "board_like_by_user"
'''
    def __str__(self):
        return "그룹명 : "+self.name+"상태 : "+self.status
'''