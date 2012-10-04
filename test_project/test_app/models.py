from django.db import models
from randomfields.fields.integer import RandomIntegerField

class Instances(models.Model):
    id = RandomIntegerField(primary_key=True)
    unique = RandomIntegerField(unique=True)
    normal = RandomIntegerField()
    
    def __unicode__(self):
        return u"%s" % self.id