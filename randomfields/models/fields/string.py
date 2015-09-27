from django.core import checks
from django.db import models
from django.utils.six import text_type
from django.utils.six.moves import range
from .base import RandomFieldBase, random

default_valid_chars = text_type("0123456789ABCDEFGHJKMNPQRSTVWXYZ")
class RandomStringFieldBase(RandomFieldBase):
    def __init__(self, *args, **kwargs):
        self.valid_chars = text_type(kwargs.pop("valid_chars", default_valid_chars))
        min_length = kwargs.pop("min_length", None)
        self.min_length = None if min_length is None else int(min_length)
        
        super(RandomStringFieldBase, self).__init__(*args, **kwargs)
        
        if min_length is not None and not 0 < self.min_length:
            raise ValueError("If set, min_length must evaluate to an integer greater than zero. You provided '%s'." % min_length)
        
        if self.min_length is None or self.min_length == self.max_length:
            self.possibilities = len(self.valid_chars) ** self.max_length
        else:
            vcl = len(self.valid_chars)
            self.possibilities = sum([vcl ** n for n in range(self.min_length, self.max_length+1)])
    
    def random(self):
        if self.min_length is None:
            length = self.max_length
        else:
            length = random.randint(self.min_length, self.max_length)
        return text_type("").join([random.choice(self.valid_chars) for _ in range(length)])
    
    def check(self, **kwargs):
        errors = super(RandomStringFieldBase, self).check(**kwargs)
        errors.extend(self.check_max_length(**kwargs))
        return errors
    
    def check_max_length(self, **kwargs):
        try:
            max_length = int(self.max_length)
            if max_length <= 0:
                raise ValueError()
        except TypeError:
            return [
                checks.Error(
                    "Subclasses of RandomStringFieldBase must define a 'max_length' attribute.",
                    hint=None,
                    obj=self,
                    id='%s.%s.MissingMaxLength' % (__name__, self.__class__.__name__),
                )
            ]
        except ValueError:
            return [
                checks.Error(
                    "'max_length' must be a positive integer.",
                    hint=None,
                    obj=self,
                    id='%s.%s.InvalidMaxLength' % (__name__, self.__class__.__name__),
                )
            ]
        return []
    
    def formfield(self, **kwargs):
        defaults = {
            'max_length': self.max_length,
            'min_length': self.min_length,
        }
        defaults.update(kwargs)
        return super(RandomStringFieldBase, self).formfield(**kwargs)

class RandomCharField(models.CharField, RandomStringFieldBase):
    def check_max_length(self, **kwargs):
        errors = super(RandomCharField, self).check_max_length(**kwargs)
        try:
            max_length = int(self.max_length)
        except (ValueError, TypeError):
            pass
        else:
            if 255 < max_length:
                errors.append(checks.Warning(
                    "It is recommended to restrict the CharField 'max_length' kwarg to 255 or less for database portability.",
                    hint="Use 'RandomTextField' instead.",
                    obj=self,
                    id='%s.%s.MaxLengthGT255' % (__name__, self.__class__.__name__),
                ))
        return errors

class RandomTextField(models.TextField, RandomStringFieldBase):
    pass