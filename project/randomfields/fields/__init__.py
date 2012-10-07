from django.db import models, IntegrityError
from math import log, ceil
import logging

from os import urandom
try:
    urandom(1)
except NotImplementedError:
    urandom_available = False
else:
    urandom_available = True

class RandomFieldBase(models.Field):
    empty_strings_allowed = False
    
    def __init__(self, *args, **kwargs):
        self.max_retry = kwargs.pop("max_retry", 3)
        self.alpha = kwargs.pop("alpha", 0.0001)
        
        # Default to the percent that causes us to generate 100 values.
        # This is roughly 91.2% full with an alpha of 0.0001.
        self.warn_at_percent = kwargs.pop("warn_at_percent", self.alpha ** (1.0 / 100))
        
        kwargs['blank'] = True
        kwargs['null'] = False
        super(RandomFieldBase, self).__init__(*args, **kwargs)
        
        self.was_added = False
    
    def pre_save(self, obj, add):
        self.was_added = add
        if add and getattr(obj, self.attname) in (None, ""):
            value = self.random()
            setattr(obj, self.attname, value)
            return getattr(obj, self.attname)
        else:
            return super(RandomFieldBase, self).pre_save(obj, add)
    
    def contribute_to_class(self, cls, name):
        super(RandomFieldBase, self).contribute_to_class(cls, name)
        
        cls_save = cls.save
        def save_wrapper(obj, *args, **kwargs):
            unsaved = True
            retry = self.max_retry
            
            while unsaved and retry:
                unsaved = False
                try:
                    cls_save(obj, *args, **kwargs)
                except IntegrityError, e:
                    unsaved = e
                    if self.was_added and self.unique:
                        # 'force_insert' is required to prevent the instance from
                        # being saved as an update and erroneously overwriting a
                        # database instance on subsequent retries
                        kwargs["force_insert"] = True
                        
                        value = getattr(obj, name)
                        
                        choices = set()
                        choices.add(value)
                        
                        # ensure unique values are available
                        possibilities = self.possibilities()# count of all possibilities
                        t = obj.__class__.objects.count()# count of taken possibilities
                        if t == possibilities:
                            raise IntegrityError("All possibilities for field '%s' on %r are taken. This may or may not be the only issue.  Additional details: %s" % (
                                        name,
                                        obj.__class__,
                                        e
                                )
                            )
                        
                        # determine how many random values to generate
                        a = float(possibilities)# force float
                        p = 1 - ((a - t) / a)# probability of collision
                        x = log(self.alpha) / log(p)
                        x = ceil(x)
                        x = int(x)
                        
                        # warn if over full
                        percent_used = t / a
                        if self.warn_at_percent < percent_used:
                            remaining_choices = possibilities - t
                            logging.warning("%.2f%% of the choices for field '%s' on %r are taken.  There %s remaining." % (
                                    percent_used * 100,
                                    name,
                                    obj.__class__,
                                    ("are %d choices" if 1 < remaining_choices else "is %d choice") % remaining_choices
                                )
                            )

                        # ensure we do not try to generate more values than possible
                        count = 1 + x
                        if possibilities < count:
                            count = possibilities
                        
                        while len(choices) < count:
                            choices.add(self.random())
                        
                        results = cls.objects.filter(
                            **{
                                "%s__in" % name: choices
                            }
                        ).values_list(name, flat=True)
                                                
                        if value in results:
                            availables = choices.difference(results)
                            if availables:
                                setattr(obj, name, availables.pop())
                            else:
                                unsaved = IntegrityError("A unique value could not be produced for field '%s'. This may or may not be the only issue.  Additional details: %s" % (
                                        name,
                                        e
                                    )
                                )
                        else:
                            raise e
                retry -= 1

            if isinstance(unsaved, Exception):
                raise unsaved
            elif unsaved:
                raise RuntimeError("'%r' was not saved.  Details not available." % obj)

        cls.save = save_wrapper
    
    def random(self):
        """
            method returns a random value for the field
        """
        raise NotImplementedError("random() must be implemented by subclasses.")
    
    def possibilities(self):
        """
            method returns the number of possibilities that a random value may take as an integer
        """
        raise NotImplementedError("possibilities() must be implemented by subclasses.")