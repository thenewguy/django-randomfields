from django.db import models
from random import choice, randint
from . import RandomFieldBase

default_valid_chars = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
class RandomCharField(models.CharField, RandomFieldBase):
    def __init__(self, *args, **kwargs):
        self.valid_chars = kwargs.pop("valid_chars", default_valid_chars)
        min_length = kwargs.pop("min_length", None)
        self.min_length = None if min_length is None else int(min_length)
        
        super(RandomCharField, self).__init__(*args, **kwargs)
        
        if min_length is not None and not 0 < self.min_length:
            raise ValueError("If set, min_length must evaluate to an integer greater than zero. You provided '%s'." % min_length)
        
    def random(self):
        if self.min_length is None:
            length = self.max_length
        else:
            length = randint(self.min_length, self.max_length)
        return "".join([choice(self.valid_chars) for _ in xrange(length)])
    
    def possibilities(self):
        if self.min_length is None or self.min_length == self.max_length:
            return len(self.valid_chars) ** self.max_length
        else:
            vcl = len(self.valid_chars)
            return sum([vcl ** n for n in xrange(self.min_length, self.max_length+1)])