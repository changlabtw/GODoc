from django.db import models
from datetime import datetime
class Profile(models.Model):
    user_name = models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    comment=models.FileField(max_length=50000)
    testfile=models.FileField(max_length=50000)
    date_time = models.DateTimeField(default = datetime.now())
    def __unicode__(self):
        return self.name
# Create your models here.
