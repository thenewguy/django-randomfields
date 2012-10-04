from django.db import models
from random import choice
from . import RandomFieldBase

default_valid_chars = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
class RandomCharField(models.CharField, RandomFieldBase):
    def __init__(self, *args, **kwargs):
        super(RandomCharField, self).__init__(*args, **kwargs)
        self.valid_chars = kwargs.get("valid_chars", default_valid_chars)
        
    def random(self):
        return "".join([choice(self.valid_chars) for _ in xrange(self.max_length)])
    
    def possibilities(self):
        return len(self.valid_chars) ** self.max_length