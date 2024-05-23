from django.db import models

# Create your models here.

from django.db import models

class Image(models.Model):
    # 图片
    img = models.ImageField(upload_to='img')
    # 创建时间
    time = models.DateTimeField(auto_now_add=True)