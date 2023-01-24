from django.db import models
from disease.models import Disease
from board.models import Board

class PlantsByDisease(models.Model):
    id=models.AutoField(primary_key=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE,null=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = "plants_by_disease"
'''
    def __str__(self):
        return "그룹명 : "+self.name+"상태 : "+self.status
'''