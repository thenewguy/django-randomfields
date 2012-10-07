from django.db import models
from randomfields.fields.string import RandomCharField

class RandomCharFieldDemo(models.Model):
    id = RandomCharField(primary_key=True, max_length=10)
    unique = RandomCharField(unique=True, max_length=25)
    normal = RandomCharField(max_length=40, min_length=1)
    
    def __unicode__(self):
        return u"%s" % self.id

class TestPrimaryKey(models.Model):
    id = RandomCharField(primary_key=True, max_length=10)

class TestUnique(models.Model):
    unique_field = RandomCharField(unique=True, max_length=10)

class TestMinLengthPossibilities(models.Model):
    data = RandomCharField(unique=True, max_length=2, min_length=1, valid_chars="ab")

class TestFixLengthPossibilities(models.Model):
    data = RandomCharField(unique=True, max_length=2, valid_chars="ab")