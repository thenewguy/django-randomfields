from django.db import models

from . import urandom_available, RandomFieldBase

if urandom_available:
    from os import urandom
    from struct import unpack
else:
    from random import randint

class RandomIntegerField(models.IntegerField, RandomFieldBase):
    if urandom_available:
        def random(self):
            return unpack("=i", urandom(4))[0]
    else:
        def random(self):
            return randint(-2147483648, 2147483647)
    
    def possibilities(self):
        return 4294967295# 4,294,967,295