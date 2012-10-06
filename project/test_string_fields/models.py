from django.db import models
from randomfields.fields.string import RandomCharField

class RandomCharFieldDemo(models.Model):
    id = RandomCharField(primary_key=True, max_length=10, min_length=3)
    unique = RandomCharField(unique=True, max_length=25)
    normal = RandomCharField(max_length=3)
    
    def __unicode__(self):
        return u"%s" % self.id