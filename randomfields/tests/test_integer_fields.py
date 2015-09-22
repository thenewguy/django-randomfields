from django.test import SimpleTestCase
from django.utils.six.moves import range
from randomfields.fields.integer import RandomIntegerFieldBase, RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField, \
                                        RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField

class FieldTests(SimpleTestCase):
    def test_invalid_rifb_attrs(self):
        class InvalidAttrs1(RandomIntegerFieldBase):
            bytes = None
            lower_bound = None
            upper_bound = None
        
        class InvalidAttrs2(RandomIntegerFieldBase):
            bytes = 4
            unpack_fmt = None
            
        class InvalidAttrs3(RandomIntegerFieldBase):
            bytes = 4
            unpack_fmt = "=i"
            lower_bound = 5
            upper_bound = 10
        
        for cls in [InvalidAttrs1, InvalidAttrs2, InvalidAttrs3]:
            with self.assertRaises(TypeError):
                cls()
        
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
        for _ in range(10):
            value = field.random()
            self.assertGreaterEqual(value, field.lower_bound)
            self.assertLessEqual(value, field.upper_bound)
    
    def test_integer_random(self):
        field = RandomIntegerField()
        for _ in range(10):
            value = field.random()
            self.assertGreaterEqual(value, field.lower_bound)
            self.assertLessEqual(value, field.upper_bound)
    
    def test_small_integer_random(self):
        field = RandomSmallIntegerField()
        for _ in range(10):
            value = field.random()
            self.assertGreaterEqual(value, field.lower_bound)
            self.assertLessEqual(value, field.upper_bound)
    
    def _test_integer_identifier_conversions(self, field_cls, value_map):
        field = field_cls()
        for db_value, display_value in value_map:
            result = field.to_python(db_value)
            self.assertEqual(db_value, result.db_value)
            self.assertEqual(display_value, result.display_value)
            
            result = field.to_python(display_value)
            self.assertEqual(db_value, result.db_value)
            self.assertEqual(display_value, result.display_value)
    
    def test_bigintegerfield_identifier_conversions(self):
        value_map = (
            (-9223372036854775808, 9223372036854775808),
            (0, 18446744073709551616),
            (9223372036854775807, 27670116110564327423),
        )
        self._test_integer_identifier_conversions(RandomBigIntegerIdentifierField, value_map)
    
    def test_integerfield_identifier_conversions(self):
        value_map = (
            (-2147483648, 2147483648),
            (0, 4294967296),
            (2147483647, 6442450943),
        )
        self._test_integer_identifier_conversions(RandomIntegerIdentifierField, value_map)

    def test_smallintegerfield_identifier_conversions(self):
        value_map = (
            (-32768, 32768),
            (0, 65536),
            (32767, 98303),
        )
        self._test_integer_identifier_conversions(RandomSmallIntegerIdentifierField, value_map)
    
    def test_integerfield_identifier_zfill_width(self):
        for field_cls in (RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField):
            field = field_cls()
            lb = "%s" % field.to_python(field.lower_bound)
            ub = "%s" % field.to_python(field.upper_bound)
            self.assertEqual(len(lb), len(ub))