from django.db import IntegrityError, transaction
from django.test import TestCase
from .models import TestPrimaryKey, TestUnique, TestMinLengthPossibilities, TestFixLengthPossibilities, TestNonUniqueIntegrityError, TestUniqueNotExistIntegrityError

#
# NEED TO CHECK AND RAISE ERROR IF MODEL DEFINED WITH AN ATTR NAMED
# WITH THE VALUE OF Field.available_values_attname AND WRITE TEST
#

class SaveTests(TestCase):
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
