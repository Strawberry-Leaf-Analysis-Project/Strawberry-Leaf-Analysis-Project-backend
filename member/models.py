from django.db import models

# Create your models here.

class Member(models.Model):
    id=models.CharField(primary_key=True,max_length=50)
    password = models.CharField(max_length=150,null=False)
    name = models.CharField(max_length=150)
    is_staff = models.CharField(max_length=1,default='0')
    is_delete=models.CharField(max_length=1,default='0')
    email=models.EmailField(max_length=256,null=False)
    board_cnt=models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = "user"

    def __str__(self):
        return "아이디 : "+self.id+"이름 : "+self.name
