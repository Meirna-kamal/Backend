from django.db import models

# Create your models here.
class file(models.Model):
    path=models.CharField(max_length=1000,default="No path yet")
    progress=models.IntegerField(default=0)
    exercise=models.IntegerField(default=0)