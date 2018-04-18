from django.test import TestCase
from randomfields.checks import DJANGO_VERSION_17
from randomfields.tests.models import TestIdentifierValue, TestIdentifierFKValue
from unittest import skipIf


@skipIf(DJANGO_VERSION_17, "Not supported on Django 17")
class IdentifierFKTests(TestCase):
    def test_reverse_accessor(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierFKValue.objects.create(data=obj)
        
        instance = TestIdentifierFKValue.objects.get(pk=rel.pk)
        
        # ensure we don't raise a type error when accessing the reverse relation
        # encountering the following exception when we do at the moment:
        #    TypeError: __new__() missing 3 required positional arguments: 'possibilities', 'lower_bound', and 'upper_bound'
        instance.data
    