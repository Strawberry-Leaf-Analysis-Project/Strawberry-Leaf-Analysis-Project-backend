from django.db import models

# Create your models here.

class Member(models.Model):
    key=models.AutoField(primary_key=True)
    id=models.CharField(max_length=50)
    password = models.CharField(max_length=150)
    visited = models.CharField(max_length=1,default='0')
    name = models.CharField(max_length=150)
    is_staff = models.CharField(max_length=1,default='0')
    is_delete=models.CharField(max_length=1,default='0')git

    class Meta:
        managed = True
        db_table = "user"

    def __str__(self):
        return "아이디 : "+self.id+"이름 : "+self.name
