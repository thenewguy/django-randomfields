from django.test import TestCase

from randomfields.fields.integer import RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField

class FieldTests(TestCase):
    def test_big_integer_bounds(self):
        field = RandomBigIntegerField()
        self.assertEqual(field.lower_bound, -9223372036854775808)
        self.assertEqual(field.upper_bound, 9223372036854775807)
    
    def test_integer_bounds(self):
        field = RandomIntegerField()
        self.assertEqual(field.lower_bound, -2147483648)
        self.assertEqual(field.upper_bound, 2147483647)
    
    def test_small_integer_bounds(self):
        field = RandomSmallIntegerField()
        self.assertEqual(field.lower_bound, -32768)
        self.assertEqual(field.upper_bound, 32767)