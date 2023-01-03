from django.db import models

# Create your models here.

class Member(models.Model):
    key=models.AutoField(db_column='key',primary_key=True)
    id=models.CharField(db_column='id',max_length=50)
    password = models.CharField(db_column='password', max_length=150)
    visited = models.CharField(db_column='visited',max_length=1,default='0')
    name = models.CharField(db_column='name', max_length=150)
    is_staff = models.CharField(db_column='is_staff',max_length=1,default='0')

    class Meta:
        managed = False
        db_table = "user"

    def __str__(self):
        return "아이디 : "+self.id+"이름 : "+self.name
