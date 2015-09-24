from django.db import models
from django.utils.six import text_type
from . import RandomFieldBase
from random import randint
from os import urandom
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
        
        self._possibilities = self.upper_bound - self.lower_bound + 1
    
    def random(self):
        if urandom_available and self.bytes:
            value = unpack(self.unpack_fmt, urandom(self.bytes))[0]
        else:
            value = randint(self.lower_bound, self.upper_bound)
        return value
    
    def possibilities(self):
        return self._possibilities
    
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

class NarrowPositiveIntegerField(models.IntegerField, RandomIntegerFieldBase):
    """
        This field is a drop in replacement for AutoField primary keys.
        It returns a random integer between 1,000,000,000 and 2,147,483,647.
        These values were chosen specifically so that the string representation
        would be fixed length without requiring zero padding.  This class is
        meant to be used until django works more reliably with fields like
        RandomIntegerIdentifierField which provide a larger range of values
        but cause quirks with django like https://code.djangoproject.com/ticket/23335
    """
    lower_bound = 1000000000
    upper_bound = 2147483647

class IntegerIdentifierValue(text_type):
    def __new__(cls, value, possibilities, lower_bound, upper_bound):
        # verify types are acceptable
        value = int(value)
        possibilities = int(possibilities)
        lower_bound = int(lower_bound)
        upper_bound = int(upper_bound)
        
        # for 32 bit int, possibilities is 4,294,967,296
        # because the possible unsigned values are [0, 4294967295]
        # In this case, map 0 to 4,294,967,296 and map
        # 4,294,967,295 to 8,589,934,591
        discriminator = possibilities - abs(lower_bound)
        if value < discriminator:
            display_value = value + possibilities
            db_value = value
        else:
            display_value = value
            db_value = value - possibilities
        
        length = len(text_type(possibilities + upper_bound))
        
        display_str = text_type(display_value).zfill(length)
        
        obj = super(IntegerIdentifierValue, cls).__new__(cls, display_str)
        obj.db_value = db_value
        obj.display_value = display_value
        
        return obj
    
    def __int__(self):
        return self.db_value

class IntegerIdentifierBase(models.Field):
    __metaclass__ = models.SubfieldBase
        
    def to_python(self, value):
        if value is not None and not isinstance(value, IntegerIdentifierValue):
            value = IntegerIdentifierValue(value, self.possibilities(), self.lower_bound, self.upper_bound)
        return value
    
    def get_prep_value(self, value):
        if value is not None:
            value = self.to_python(value).db_value
        return value
    
    def from_db_value(self, value, *args):
        return self.to_python(value)
    
    def formfield(self, **kwargs):
        defaults = {
            'min_value': IntegerIdentifierValue(self.lower_bound, self.possibilities(), self.lower_bound, self.upper_bound),
            'max_value': IntegerIdentifierValue(self.upper_bound, self.possibilities(), self.lower_bound, self.upper_bound),
        }
        defaults.update(kwargs)
        return super(IntegerIdentifierBase, self).formfield(**defaults)

class RandomBigIntegerIdentifierField(IntegerIdentifierBase, RandomBigIntegerField):
    pass

class RandomIntegerIdentifierField(IntegerIdentifierBase, RandomIntegerField):
    pass

class RandomSmallIntegerIdentifierField(IntegerIdentifierBase, RandomSmallIntegerField):
    pass