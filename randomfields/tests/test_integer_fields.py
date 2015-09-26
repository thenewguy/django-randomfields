from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.utils.six.moves import range
from randomfields.models.fields.integer import RandomIntegerFieldBase, RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField, \
                                        RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField, \
                                        NarrowPositiveIntegerField

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
    
    def test_integer_formfield_bounds(self):
        for field_cls in [RandomIntegerField, RandomBigIntegerField, RandomSmallIntegerField, NarrowPositiveIntegerField]:
            field = field_cls()
            form_field = field.formfield()
            
            # no exceptions
            form_field.clean(field.lower_bound)
            form_field.clean(field.upper_bound)
            for value in [int(field.lower_bound + p * (field.possibilities() - 2)) for p in (.1, .3, .5, .7, .9)]:
                form_field.clean(value)
            
            with self.assertRaises(ValidationError):
                form_field.clean(field.lower_bound-1)
            with self.assertRaises(ValidationError):
                form_field.clean(field.upper_bound+1)
    
    def test_integer_random(self):
        for field_cls in [RandomIntegerField, RandomBigIntegerField, RandomSmallIntegerField]:
            field = field_cls()
            bytes_ = field.bytes
            for _ in range(10):
                val1 = field.random()
                self.assertGreaterEqual(val1, field.lower_bound)
                self.assertLessEqual(val1, field.upper_bound)
                
                # force random method to use randint instead of unpack/urandom
                field.bytes = None
                val2 = field.random()
                self.assertGreaterEqual(val2, field.lower_bound)
                self.assertLessEqual(val2, field.upper_bound)
                
                # reset
                field.bytes = bytes_
    
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
    
    def test_integerfield_identifier_formfield_validation(self):
        for field_cls in (RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField):
            field = field_cls()
            form_field = field.formfield()
            
            # identifiers are mapped to value + possibilities, so values range (lowerbound, upperbound)
            # should raise validation errors
            with self.assertRaises(ValidationError):
                form_field.clean(field.lower_bound)
            with self.assertRaises(ValidationError):
                form_field.clean(field.upper_bound)
            for value in [int(field.lower_bound + p * (field.possibilities() - 2)) for p in (.1, .3, .5, .7, .9)]:
                with self.assertRaises(ValidationError):
                    form_field.clean(value)
            
            # no exceptions
            possibilities = field.possibilities()
            form_field.clean(field.lower_bound + possibilities)
            form_field.clean(field.upper_bound + possibilities)
            for value in [int(field.lower_bound + p * (field.possibilities() - 2)) for p in (.1, .3, .5, .7, .9)]:
                form_field.clean(value + possibilities)
    
    def test_integerfield_identifier_zfill_width(self):
        for field_cls in (NarrowPositiveIntegerField, RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField):
            field = field_cls()
            lb = "%s" % field.to_python(field.lower_bound)
            ub = "%s" % field.to_python(field.upper_bound)
            lb_len = len(lb)
            ub_len = len(ub)
            self.assertEqual(lb_len, ub_len, "{} and {} are of different string width, {} != {}".format(lb, ub, lb_len, ub_len))