from django.db import models
from member.models import Member

def user_directory_path(instance,filename):
    name="temp_image1.jpg"
    return 'image/{0}/{1}'.format(instance.user.id,name)

class TempImage(models.Model):
    id=models.AutoField(primary_key=True)
    image=models.FileField(upload_to=user_directory_path,null=False)
    user=models.ForeignKey(Member,on_delete=models.CASCADE,null=True)

    class Meta:
        managed = True
        db_table = "temp_image"
    '''
    def __str__(self):
        return "그룹명 : "+self.name+"상태 : "+self.status
    '''