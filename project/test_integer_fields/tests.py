from django.test import TestCase

from randomfields.fields.integer import RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField, \
                                        RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField

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
    
    def test_big_integer_random(self):
        field = RandomBigIntegerField()
        for _ in xrange(10):
            value = field.random()
            self.assertGreaterEqual(value, field.lower_bound)
            self.assertLessEqual(value, field.upper_bound)
    
    def test_integer_random(self):
        field = RandomIntegerField()
        for _ in xrange(10):
            value = field.random()
            self.assertGreaterEqual(value, field.lower_bound)
            self.assertLessEqual(value, field.upper_bound)
    
    def test_small_integer_random(self):
        field = RandomSmallIntegerField()
        for _ in xrange(10):
            value = field.random()
            self.assertGreaterEqual(value, field.lower_bound)
            self.assertLessEqual(value, field.upper_bound)
    
    def test_integer_identifier_conversions(self):
        for cls in [RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField]:
            field = cls()
            for value in xrange(-20, 21, 1):
                for x in [value, field.random()]:
                    res = field.to_python(x)
                    self.assertEqual(field.get_prep_value(res), x)