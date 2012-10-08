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