from django.db import models
from . import RandomFieldBase

from os import urandom
try:
    urandom(1)
except NotImplementedError:
    urandom_available = False
    from random import randint
else:
    urandom_available = True
    from struct import unpack    

class RandomIntegerFieldBase(RandomFieldBase):
    _bytes = None
    _unpack_fmt = None
    
    def __init__(self, *args, **kwargs):
        super(RandomIntegerFieldBase, self).__init__(*args, **kwargs)
        
        bit_exp = self.bytes * 8 - 1
        self.lower_bound = -(2 ** bit_exp)
        self.upper_bound = 2 ** bit_exp - 1
        self._possibilities = self.upper_bound - self.lower_bound + 1
    
    if urandom_available:
        def random(self):
            return unpack(self.unpack_fmt, urandom(self.bytes))[0]
    else:
        def random(self):
            return randint(self.lower_bound, self.upper_bound)
    
    def possibilities(self):
        return self._possibilities
    
    @property
    def bytes(self):
        if self._bytes is None:
            raise NotImplementedError("Subclasses must define self._bytes as an integer specifying how many bytes the integer is.")
        return self._bytes
    
    @property
    def unpack_fmt(self):
        if self._unpack_fmt is None:
            raise NotImplementedError("Subclasses must define self._unpack_fmt as a string to be passed directly to unpack.")
        return self._unpack_fmt

class RandomBigIntegerField(models.BigIntegerField, RandomIntegerFieldBase):
    _bytes = 8
    _unpack_fmt = "=q"

class RandomIntegerField(models.IntegerField, RandomIntegerFieldBase):
    _bytes = 4
    _unpack_fmt = "=i"

class RandomSmallIntegerField(models.SmallIntegerField, RandomIntegerFieldBase):
    _bytes = 2
    _unpack_fmt = "=h"

class IntegerIdentifierValue(object):
    def __init__(self, value, possibilities):
        # for 32 bit int, possibilities is 4,294,967,296
        # because the possible unsigned values are [0, 4294967295]
        # In this case, map 0 to 4,294,967,296 and map
        # 4,294,967,295 to 8,589,934,591
        if value < possibilities:
            self.display_value = value + possibilities
            self.db_value = value
        else:
            self.display_value = value
            self.db_value = value - possibilities
        
        self.length = len(str(possibilities))
    
    def __str__(self):
        return str(self.display_value).zfill(self.length)
    
    def __unicode__(self):
        return unicode(self.__str__())
    
    def __int__(self):
        return self.display_value
    
    def get_prep_value(self):
        return self.db_value

class IntegerIdentifierBase(models.Field):
    __metaclass__ = models.SubfieldBase
        
    def to_python(self, value):
        """
            Deal gracefully with any of the following arguments:
                - An instance of the correct type (e.g., Hand in our ongoing example).
                - A string (e.g., from a deserializer).
                - Whatever the database returns for the column type you're using.
        """
        if value is not None and not isinstance(value, IntegerIdentifierValue):
            value = super(IntegerIdentifierBase, self).to_python(value)
            value = IntegerIdentifierValue(value, self.possibilities())
        
        return value
    
    def get_prep_value(self, value):
        if value is not None:
            if not isinstance(value, IntegerIdentifierValue):
                value = self.to_python(value)
            value = value.db_value
        return value

class RandomBigIntegerIdentifierField(IntegerIdentifierBase, RandomBigIntegerField):
    pass

class RandomIntegerIdentifierField(IntegerIdentifierBase, RandomIntegerField):
    pass

class RandomSmallIntegerIdentifierField(IntegerIdentifierBase, RandomSmallIntegerField):
    pass