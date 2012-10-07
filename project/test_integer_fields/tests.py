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