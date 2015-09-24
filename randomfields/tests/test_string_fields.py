from django.db import IntegrityError, transaction
from django.forms.models import model_to_dict
from django.test import TestCase
from django.utils.six import text_type
from randomfields.fields.integer import IntegerIdentifierValue
from .models import TestIdentifierO2OValue, TestIdentifierValue, TestPrimaryKey, TestUnique, TestMinLengthPossibilities, TestFixLengthPossibilities, TestNonUniqueIntegrityError, TestUniqueNotExistIntegrityError

try:
    from unittest import mock
except ImportError:
    import mock

#
# NEED TO CHECK AND RAISE ERROR IF MODEL DEFINED WITH AN ATTR NAMED
# WITH THE VALUE OF Field.available_values_attname AND WRITE TEST
#

class SaveTests(TestCase):
    def _test_identifier_expected_values(self, model_class, attr):
        value_map = (
            (-2147483648, 2147483648),
            (0, 4294967296),
            (2147483647, 6442450943),
        )
        
        for db_value, display_value in value_map:
            obj = model_class(**{attr: display_value})
            obj.save()
            
            value = getattr(obj, attr)
            self.assertTrue(isinstance(value, IntegerIdentifierValue), "Object attribute '%s' was not an instance of IntegerIdentifierValue.  It was type %r" % (attr, type(value)))
            self.assertEqual(value.display_value, display_value)
            self.assertEqual(value.db_value, db_value)
            
            key = 'id' if attr == "pk" else attr
            data = model_to_dict(obj)
            text = text_type(value)
            self.assertEqual(data.get(key, None), text, "Key '{}' did not match '{}' in the following dict: {}".format(key, text, data))
        
    def test_identifier_expected_values_primary_key_by_fieldname(self):
        self._test_identifier_expected_values(TestIdentifierValue, "id")
        
    def test_identifier_expected_values_primary_key_by_pk(self):
        self._test_identifier_expected_values(TestIdentifierValue, "pk")
            
    def test_auto_primary_key(self):
        obj = TestPrimaryKey()
        obj.save()
        all_pks = TestPrimaryKey.objects.all().values_list("pk", flat=True)
        self.assertIn(obj.pk, all_pks)
    
    def test_specified_primary_key(self):
        pk = "test"
        obj = TestPrimaryKey(pk=pk)
        obj.save()
        all_pks = TestPrimaryKey.objects.all().values_list("pk", flat=True)
        self.assertIn(pk, all_pks)
        
        with self.assertRaises(IntegrityError):
            TestPrimaryKey.objects.create(pk=pk)

    def test_collision_not_corrected_when_set_manually(self):
        obj1 = TestUnique()
        obj1.save()
        obj2 = TestUnique(unique_field=obj1.unique_field)
        with self.assertRaises(IntegrityError):
            obj2.save()

    def test_collision_correction(self):
        obj1 = TestUnique()
        obj1.save()
        obj2 = TestUnique(unique_field=obj1.unique_field)
        
        # begin hack
        # imitate accidental collision.  under normal circumstances,
        # available_values will only be persisted on a model instance
        # during Field.pre_save() or the monkeypatched instance.save().
        # it should never be set manually because it is used to detect
        # if collision correction should occur
        field = obj2._meta.get_field("unique_field")
        field.persist_available_values(obj2, set())
        # endhack
        
        obj2.save()
        
        all_values = TestUnique.objects.all().values_list("unique_field", flat=True)
        self.assertIn(obj1.unique_field, all_values)
        self.assertIn(obj2.unique_field, all_values)
        self.assertNotEqual(obj1.pk, obj2.pk)
    
    def test_atomic_collision_correction(self):
        with transaction.atomic():
            self.test_collision_correction()
    
    def test_available_values_persist_and_removed(self):
        obj1 = TestUnique()
        field1 = obj1._meta.get_field("unique_field")
        self.assertFalse(hasattr(obj1, field1.available_values_attname))
        
        val1 = field1.pre_save(obj1, True)
        self.assertTrue(val1)
        self.assertTrue(hasattr(obj1, field1.available_values_attname))
        
        obj1.save()
        self.assertEqual(val1, obj1.unique_field)
        self.assertFalse(hasattr(obj1, field1.available_values_attname))
    
    def test_available_values_not_persisted(self):
        obj1 = TestUnique(unique_field="foo")
        field1 = obj1._meta.get_field("unique_field")
        self.assertFalse(hasattr(obj1, field1.available_values_attname))
        
        val1 = field1.pre_save(obj1, True)
        self.assertEqual(val1, "foo")
        self.assertFalse(hasattr(obj1, field1.available_values_attname))
        
        obj1.save()
        self.assertEqual(val1, obj1.unique_field)
        self.assertFalse(hasattr(obj1, field1.available_values_attname))
    
    @mock.patch('randomfields.fields.logger')
    def test_warn_at_percent(self, mocked_logger):
        obj1 = TestMinLengthPossibilities()
        self.assertEqual(obj1._meta.get_field("data").valid_chars, "ab")
        self.assertEqual(obj1._meta.get_field("data").max_length, 2)
        self.assertEqual(obj1._meta.get_field("data").min_length, 1)
        self.assertEqual(6, obj1._meta.get_field("data").possibilities())
        self.assertEqual(0, TestMinLengthPossibilities.objects.count())
        
        warn_at = 0.55
        
        for i in (1, 2, 3, 4, 5, 6, 7):
            obj = TestMinLengthPossibilities()
            obj._meta.get_field("data").warn_at_percent = warn_at
            if i == 7:
                with self.assertRaises(IntegrityError):
                    obj.save()
            else:
                obj.save()
                if i < 5:
                    self.assertFalse(mocked_logger.warning.called)
                else:
                    count = i - 4# 4==1, 5==2, 6==3
                    self.assertEqual(count, mocked_logger.warning.call_count)
    
    def test_min_length_possibilities(self):
        # ensure possibilities are calculated properly for min_length
        obj1 = TestMinLengthPossibilities()
        self.assertEqual(obj1._meta.get_field("data").valid_chars, "ab")
        self.assertEqual(obj1._meta.get_field("data").max_length, 2)
        self.assertEqual(obj1._meta.get_field("data").min_length, 1)
        """
            possibilities:
                a
                aa
                ab
                ba
                bb
                b
        """
        self.assertEqual(6, obj1._meta.get_field("data").possibilities())
        
        # ensure all possibilities are saved
        while TestMinLengthPossibilities.objects.count() < 6:
            TestMinLengthPossibilities().save()
        
        all_values = TestMinLengthPossibilities.objects.all().values_list("data", flat=True)
        self.assertIn('a', all_values)
        self.assertIn('aa', all_values)
        self.assertIn('ab', all_values)
        self.assertIn('ba', all_values)
        self.assertIn('bb', all_values)
        self.assertIn('b', all_values)
        
        # ensure an integrity error is thrown on subsequent saves
        self.assertRaises(IntegrityError, TestMinLengthPossibilities().save)
    
    def test_fix_length_possibilities(self):
        obj1 = TestFixLengthPossibilities()
        self.assertEqual(obj1._meta.get_field("data").valid_chars, "ab")
        self.assertEqual(obj1._meta.get_field("data").max_length, 2)
        self.assertIs(obj1._meta.get_field("data").min_length, None)
        """
            possibilities:
                aa
                ab
                ba
                bb
        """
        self.assertEqual(4, obj1._meta.get_field("data").possibilities())
        
        # ensure all possibilities are saved
        while TestFixLengthPossibilities.objects.count() < 4:
            TestFixLengthPossibilities().save()
        
        all_values = TestFixLengthPossibilities.objects.all().values_list("data", flat=True)
        self.assertNotIn('a', all_values)
        self.assertIn('aa', all_values)
        self.assertIn('ab', all_values)
        self.assertIn('ba', all_values)
        self.assertIn('bb', all_values)
        self.assertNotIn('b', all_values)
        
        # ensure an integrity error is thrown on subsequent saves
        self.assertRaises(IntegrityError, TestFixLengthPossibilities().save)
    
    def test_non_unique_survives_integrity_error(self):
        obj1 = TestNonUniqueIntegrityError()
        obj1.unique_int_field = 1
        obj1.save()
        
        obj2 = TestNonUniqueIntegrityError()
        obj2.unique_int_field = obj1.unique_int_field
        field2 = obj2._meta.get_field("non_unique_field")
        val2 = field2.pre_save(obj2, True)
        
        with self.assertRaises(IntegrityError):
            obj2.save()
        
        self.assertEqual(obj2.non_unique_field, val2)
        
        obj2.unique_int_field += 1
        obj2.save()
        self.assertEqual(obj2.non_unique_field, val2)
    
    def test_unique_not_exist_survives_integrity_error(self):
        obj1 = TestUniqueNotExistIntegrityError()
        obj1.unique_int_field = 1
        obj1.unique_rand_field = "foo"
        obj1.save()
        
        obj2 = TestUniqueNotExistIntegrityError()
        obj2.unique_int_field = obj1.unique_int_field
        field2 = obj2._meta.get_field("unique_rand_field")
        val2 = field2.pre_save(obj2, True)
        
        with self.assertRaises(IntegrityError):
            obj2.save()
        
        self.assertEqual(obj2.unique_rand_field, val2)
        
        obj2.unique_int_field += 1
        obj2.save()
        self.assertEqual(obj2.unique_rand_field, val2)
