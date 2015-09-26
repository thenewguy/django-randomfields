from django.core import checks
from django.db import models
from random import randint
from os import urandom
from ..base import RandomFieldBase
try:
    urandom(1)
except NotImplementedError:
    urandom_available = False
else:
    urandom_available = True
    from struct import unpack    

class RandomIntegerFieldBase(RandomFieldBase):
    bytes = None
    unpack_fmt = None
    lower_bound = None
    upper_bound = None
    
    def __init__(self, *args, **kwargs):
        super(RandomIntegerFieldBase, self).__init__(*args, **kwargs)
        
        if self.bytes:
            if self.unpack_fmt is None:
                raise TypeError("unpack_fmt must not be None when bytes is specified")
            
            if self.lower_bound is None and self.upper_bound is None:
                bit_exp = self.bytes * 8 - 1
                self.lower_bound = -(2 ** bit_exp)
                self.upper_bound = 2 ** bit_exp - 1
            else:
                raise TypeError("lower_bound and upper_bound must be None when bytes is specified")
            
        elif self.lower_bound is None or self.upper_bound is None:
            raise TypeError("lower_bound and upper_bound must be specified when bytes is not")
        
        self.possibilities = self.upper_bound - self.lower_bound + 1
    
    def random(self):
        if urandom_available and self.bytes:
            value = unpack(self.unpack_fmt, urandom(self.bytes))[0]
        else:
            value = randint(self.lower_bound, self.upper_bound)
        return value
    
    def formfield(self, **kwargs):
        defaults = {
            'min_value': self.lower_bound,
            'max_value': self.upper_bound,
        }
        defaults.update(kwargs)
        return super(RandomIntegerFieldBase, self).formfield(**defaults)

class RandomBigIntegerField(models.BigIntegerField, RandomIntegerFieldBase):
    bytes = 8
    unpack_fmt = "=q"

class RandomIntegerField(models.IntegerField, RandomIntegerFieldBase):
    bytes = 4
    unpack_fmt = "=i"

class RandomSmallIntegerField(models.SmallIntegerField, RandomIntegerFieldBase):
    bytes = 2
    unpack_fmt = "=h"

class RandomNarrowIntegerField(models.IntegerField, RandomIntegerFieldBase):
    """
        This field is a drop in replacement for AutoField primary keys.
        It returns a random integer between 1,000,000,000 and 2,147,483,647.
        These values were chosen specifically so that the string representation
        would be fixed length without requiring zero padding.
        
        This field uses a simpler approach to mimic the functionality of the
        identifier fields like `RandomBigIntegerIdentifierField`,
        `RandomIntegerIdentifierField`, and `RandomSmallIntegerIdentifierField`
        which cannot be reliably implemented under older versions of Django (< 1.8)
        due to lack of Field.from_db_value() support.
    """
    lower_bound = 1000000000
    upper_bound = 2147483647

class NarrowPositiveIntegerField(RandomNarrowIntegerField):
    def check(self, **kwargs):
        errors = super(NarrowPositiveIntegerField, self).check(**kwargs)
        errors.append(checks.Warning(
            'NarrowPositiveIntegerField has been deprecated.',
            hint='Use RandomNarrowIntegerField instead.',
            obj=self,
            id='%s.%s.Depreciated' % (__name__, self.__class__.__name__),
        ))
        return errors
