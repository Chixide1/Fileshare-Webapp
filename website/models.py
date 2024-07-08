from django.db import models
from django.conf import settings
# Create your models here.

class File(models.Model):
    
    date_created = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(null=True)
    file_name = models.CharField(max_length=200, null=True)
    file_extention = models.CharField(max_length=200, null=True)
    file_size = models.IntegerField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None,null=True)

    def __str__(self) -> str:
        return self.file_name