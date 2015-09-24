from django.db import models
from randomfields.fields.string import RandomCharField
from randomfields.fields.integer import RandomIntegerIdentifierField
from uuid import uuid4

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
    data = models.ManyToManyField(TestIdentifierValue, blank=True)

class TestIdentifierAllValue(models.Model):
    o2o = models.OneToOneField(TestIdentifierValue, related_name=uuid4().hex)
    fk = models.ForeignKey(TestIdentifierValue, related_name=uuid4().hex)
    m2m = models.ManyToManyField(TestIdentifierValue, blank=True, related_name=uuid4().hex)

class TestIdentifierM2MO2OPKValue(models.Model):
    id = models.OneToOneField(TestIdentifierValue, primary_key=True, editable=True, related_name=uuid4().hex)
    m2m = models.ManyToManyField(TestIdentifierValue, blank=True, related_name=uuid4().hex)

class TestIdentifierM2MO2OValue(models.Model):
    o2o = models.OneToOneField(TestIdentifierValue, related_name=uuid4().hex)
    m2m = models.ManyToManyField(TestIdentifierValue, blank=True, related_name=uuid4().hex)

class TestIdentifierM2MFKValue(models.Model):
    fk = models.ForeignKey(TestIdentifierValue, related_name=uuid4().hex)
    m2m = models.ManyToManyField(TestIdentifierValue, blank=True, related_name=uuid4().hex)