from django.db import models, IntegrityError, transaction
from math import log, ceil
import logging

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
        
        if kwargs.get('primary_key', False):
            kwargs.setdefault('editable', False)
        
        super(RandomFieldBase, self).__init__(*args, **kwargs)
    
    def find_available_values(self, model_cls):
        if self.unique:
            choices = set()
            
            # ensure unique values are available
            possibilities = self.possibilities()# count of all possibilities
            t = model_cls.objects.count()# count of taken possibilities
            if t == possibilities:
                raise IntegrityError("All possibilities for field '%s' on %r are taken." % (self.attname, model_cls))
            
            # determine how many random values to generate
            a = float(possibilities)# force float
            p = 1 - ((a - t) / a)# probability of collision
            if p:
                x = log(self.alpha) / log(p)
                x = ceil(x)
                x = int(x)
            else:
                x = 1
            
            # warn if over full
            percent_used = t / a
            if self.warn_at_percent < percent_used:
                remaining_choices = possibilities - t
                logging.warning("%.2f%% of the choices for field '%s' on %r are taken.  There %s remaining." % (
                        percent_used * 100,
                        self.attname,
                        model_cls,
                        ("are %d choices" if 1 < remaining_choices else "is %d choice") % remaining_choices
                    )
                )
    
            # ensure we do not try to generate more values than possible
            count = 1 + x
            if possibilities < count:
                count = possibilities
            
            while len(choices) < count:
                choices.add(self.random())
            
            results = model_cls.objects.filter(
                **{
                    "%s__in" % self.attname: choices
                }
            ).values_list(self.attname, flat=True)
                                    
            available_values = choices.difference(results)
        else:
            available_values = set([self.random()])
        
        return available_values
    
    @property
    def available_values_attname(self):
        return "%s_randomfields_available_values" % self.attname
    
    def persist_available_values(self, obj, available_values):
        setattr(obj, self.available_values_attname, available_values)
    
    def get_available_values(self, obj):
        available_values = getattr(obj, self.available_values_attname, set())
        while not available_values:
            available_values = self.find_available_values(obj.__class__)
        return available_values
    
    def set_available_value(self, obj):
        available_values = self.get_available_values(obj)
        setattr(obj, self.attname, available_values.pop())
        self.persist_available_values(obj, available_values)
    
    def pre_save(self, obj, add):
        if add and getattr(obj, self.attname) in (None, ""):
            self.set_available_value(obj)
            return getattr(obj, self.attname)
        else:
            return super(RandomFieldBase, self).pre_save(obj, add)
    
    def contribute_to_class(self, cls, name):
        super(RandomFieldBase, self).contribute_to_class(cls, name)
        cls_save = cls.save
        def save_wrapper(obj, *args, **kwargs):
            retry = self.max_retry
            success = False
            while retry and not success:
                retry -= 1
                try:
                    with transaction.atomic():
                        cls_save(obj, *args, **kwargs)
                except IntegrityError:
                    if not retry or not self.unique or not hasattr(obj, self.available_values_attname):
                        raise
                    self.set_available_value(obj)
                else:
                    success = True
                    if hasattr(obj, self.available_values_attname):
                        delattr(obj, self.available_values_attname)
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