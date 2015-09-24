from django.db import models
from randomfields.fields.string import RandomCharField
from randomfields.fields.integer import RandomIntegerIdentifierField

class TestPrimaryKey(models.Model):
    id = RandomCharField(primary_key=True, max_length=10)

class TestUnique(models.Model):
    unique_field = RandomCharField(unique=True, max_length=10)

class TestNonUniqueIntegrityError(models.Model):
    unique_int_field = models.IntegerField(unique=True)
    non_unique_field = RandomCharField(max_length=10)

class TestUniqueNotExistIntegrityError(models.Model):
    unique_int_field = models.IntegerField(unique=True)
    unique_rand_field = RandomCharField(unique=True, max_length=10)

class TestMinLengthPossibilities(models.Model):
    data = RandomCharField(unique=True, max_length=2, min_length=1, valid_chars="ab")

class TestFixLengthPossibilities(models.Model):
    data = RandomCharField(unique=True, max_length=2, valid_chars="ab")

class TestIdentifierValue(models.Model):
    id = RandomIntegerIdentifierField(primary_key=True, editable=True)

class TestIdentifierO2OValue(models.Model):
    id = models.OneToOneField(TestIdentifierValue, primary_key=True, editable=True)

class TestIdentifierFKValue(models.Model):
    data = models.ForeignKey(TestIdentifierValue)

class TestIdentifierM2MValue(models.Model):
    data = models.ManyToManyField(TestIdentifierValue, null=True, blank=True)

class TestIdentifierAllValue(models.Model):
    id = models.OneToOneField(TestIdentifierValue, primary_key=True, editable=True)
    fk = models.ForeignKey(TestIdentifierValue)
    m2m = models.ManyToManyField(TestIdentifierValue, null=True, blank=True)
