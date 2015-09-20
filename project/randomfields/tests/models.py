from django.db import models
from randomfields.fields.integer import RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField, \
                                        RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField
from randomfields.fields.string import RandomCharField

class RandomBigIntegerFieldDemo(models.Model):
    id = RandomBigIntegerField(primary_key=True)
    unique = RandomBigIntegerField(unique=True)
    normal = RandomBigIntegerField()
    
    def __unicode__(self):
        return u"%s" % self.id

class RandomIntegerFieldDemo(models.Model):
    id = RandomIntegerField(primary_key=True)
    unique = RandomIntegerField(unique=True)
    normal = RandomIntegerField()
    
    def __unicode__(self):
        return u"%s" % self.id

class RandomSmallIntegerFieldDemo(models.Model):
    id = RandomSmallIntegerField(primary_key=True)
    unique = RandomSmallIntegerField(unique=True)
    normal = RandomSmallIntegerField()
    
    def __unicode__(self):
        return u"%s" % self.id

class RandomBigIntegerIdentifierFieldDemo(models.Model):
    id = RandomBigIntegerIdentifierField(primary_key=True)
    unique = RandomBigIntegerIdentifierField(unique=True)
    normal = RandomBigIntegerIdentifierField()
    
    def __unicode__(self):
        return u"%s" % self.id

class RandomIntegerIdentifierFieldDemo(models.Model):
    id = RandomIntegerIdentifierField(primary_key=True)
    unique = RandomIntegerIdentifierField(unique=True)
    normal = RandomIntegerIdentifierField()
    
    def __unicode__(self):
        return u"%s" % self.id

class RandomSmallIntegerIdentifierFieldDemo(models.Model):
    id = RandomSmallIntegerIdentifierField(primary_key=True)
    unique = RandomSmallIntegerIdentifierField(unique=True)
    normal = RandomSmallIntegerIdentifierField()
    
    def __unicode__(self):
        return u"%s" % self.id

class RandomCharFieldDemo(models.Model):
    id = RandomCharField(primary_key=True, max_length=10)
    unique = RandomCharField(unique=True, max_length=25)
    normal = RandomCharField(max_length=40, min_length=1)
    
    def __unicode__(self):
        return u"%s" % self.id

class WarnAtPercentDemo(models.Model):
    id = RandomCharField(primary_key=True, max_length=3, min_length=1, valid_chars="0123ABC", warn_at_percent=0.6)
    
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