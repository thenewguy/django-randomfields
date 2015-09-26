from django.apps import AppConfig
from django.db.models.signals import class_prepared
from django.dispatch import receiver
from json import dumps
from .fields.integer import IntegerIdentifierBase, RandomFieldBase
from .tests.checks import DJANGO_VERSION_17

all_prepared_model_classes = []
@receiver(class_prepared)
def store_model_class(sender, **kwargs):
    all_prepared_model_classes.append(sender)

class RandomFieldConfig(AppConfig):
    name = "randomfields"
    unsupported_fields = tuple()
    masked_attrs = tuple()
    
    def ready(self):
        unsupported_fields = []
        masked_attrs = []
        for model_class in all_prepared_model_classes:
            obj = model_class()
            for field in obj._meta.fields:
                if DJANGO_VERSION_17 and isinstance(field, IntegerIdentifierBase):
                    unsupported_fields.append((repr(model_class), repr(field)))
                if isinstance(field, RandomFieldBase):
                    if hasattr(obj, field.available_values_attname):
                        masked_attrs.append((repr(model_class), field.available_values_attname))
        self.raise_for_unsupported_fields(unsupported_fields)
        self.raise_for_masked_attrs(masked_attrs)
    
    def dumps(self, value):
        return dumps(value, sort_keys=True, indent=4, separators=(',', ': '))
    
    def raise_for_unsupported_fields(self, unsupported_fields):
        if unsupported_fields:
            unsupported = self.dumps(unsupported_fields)
            raise NotImplementedError("The following model fields currently in use are unsupported:\n%s" % unsupported)
    
    def raise_for_masked_attrs(self, masked_attrs):
        if masked_attrs:
            masked = self.dumps(masked_attrs)
            raise ValueError("The following models currently mask required attributes:\n%s" % masked)

class RandomFieldTestConfig(RandomFieldConfig):
    def raise_for_unsupported_fields(self, unsupported_fields):
        self.unsupported_fields = tuple(unsupported_fields)
    
    def raise_for_masked_attrs(self, masked_attrs):
        self.masked_attrs = tuple(masked_attrs)