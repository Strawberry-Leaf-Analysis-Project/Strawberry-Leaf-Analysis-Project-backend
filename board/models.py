from django.db import models

# Create your models here.
class Board(models.Model):
    key=models.AutoField(db_column='key',primary_key=True)
    title=models.CharField(db_column='title',max_length=100)
    explain = models.CharField(db_column='explain', max_length=500)
    user_key=models.IntegerField(db_column='user_key')
    image = models.CharField(db_column='image',max_length=1000)
    ##
    #result = models.ImageField(db_column='result')
    date=models.DateTimeField(db_column='date')
    views=models.IntegerField(db_column='views')
    like = models.IntegerField(db_column='like')
    disease = models.CharField(db_column='disease', max_length=100)
    growth = models.CharField(db_column='growth', max_length=100)

    class Meta:
        managed = False
        db_table = "board"

    def __str__(self):
        return "제목 : "+self.title+"설명 : "+self.explain