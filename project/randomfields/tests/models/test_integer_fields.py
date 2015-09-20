from django.db import models
from randomfields.fields.integer import RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField, \
                                        RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField

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