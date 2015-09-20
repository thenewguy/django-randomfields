from django.db import IntegrityError
from django.test import TransactionTestCase
from .models import TestPrimaryKey, TestUnique, TestMinLengthPossibilities, TestFixLengthPossibilities

class SaveTests(TransactionTestCase):
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

    def test_collision_correction(self):
        obj1 = TestUnique()
        obj1.save()
        obj2 = TestUnique(unique_field=obj1.unique_field)
        obj2.save()
        all_values = TestUnique.objects.all().values_list("unique_field", flat=True)
        self.assertIn(obj1.unique_field, all_values)
        self.assertIn(obj2.unique_field, all_values)
        self.assertNotEqual(obj1.pk, obj2.pk)
    
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