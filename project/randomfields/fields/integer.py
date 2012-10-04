from django.db import models

from . import urandom_available, RandomFieldBase

if urandom_available:
    from os import urandom
    from struct import unpack
else:
    from random import randint

class RandomBigIntegerField(models.BigIntegerField, RandomFieldBase):
    if urandom_available:
        def random(self):
            return unpack("=q", urandom(8))[0]
    else:
        def random(self):
            return randint(-9223372036854775808, 9223372036854775807)
    
    def possibilities(self):
        return 18446744073709551616# 18,446,744,073,709,551,615 + 1 (for zero)

class RandomIntegerField(models.IntegerField, RandomFieldBase):
    if urandom_available:
        def random(self):
            return unpack("=i", urandom(4))[0]
    else:
        def random(self):
            return randint(-2147483648, 2147483647)
    
    def possibilities(self):
        return 4294967296# 4,294,967,295 + 1 (for zero)

class RandomSmallIntegerField(models.SmallIntegerField, RandomFieldBase):
    if urandom_available:
        def random(self):
            return unpack("=h", urandom(2))[0]
    else:
        def random(self):
            return randint(-32768, 32767)
    
    def possibilities(self):
        return 65536# 65,535 + 1 (for zero)