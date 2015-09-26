from bs4 import BeautifulSoup
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from randomfields.tests.checks import skipIf, DJANGO_VERSION_17
from randomfields.tests.models import TestMaskedAttrDetection, TestIdentifierM2MO2OPKValue, TestIdentifierM2MFKValue, TestIdentifierValue, TestIdentifierO2OValue, TestIdentifierFKValue, TestIdentifierM2MValue, TestIdentifierAllValue, TestIdentifierM2MO2OValue
from randomfields.tests.test_string_fields import AppConfigTests

class DatabaseTest(TestCase):
    def test_superuser_exists(self):
        User = get_user_model()
        user = User.objects.get(username=settings.SUPERUSER_USERNAME)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(settings.SUPERUSER_PASSWORD))

class AppTestConfigTests(AppConfigTests):
    def test_tests_are_installed(self):
        self.assertTrue(apps.is_installed("%s.tests" % self.app))
    
    def test_unsupported_fields(self):
        errors = TestIdentifierValue().check()
        key = "randomfields.models.fields.integer.identifier.IntegerIdentifierBase.Unsupported"
        ids = [error.id for error in errors]
        
        if DJANGO_VERSION_17:
            self.assertIn(key, ids)
        else:
            self.assertNotIn(key, ids)

    def test_masked_attrs(self):
        errors = TestMaskedAttrDetection().check()
        ids = [error.id for error in errors]
        self.assertIn("randomfields.models.fields.base.RandomFieldBase.MaskedAttr", ids)

@skipIf(DJANGO_VERSION_17, "Not supported on Django 17")
class IdentifierAdminTests(TestCase):
    def setUp(self):
        self.client.login(username=settings.SUPERUSER_USERNAME, password=settings.SUPERUSER_PASSWORD)
    
    def get_admin_url_prefix(self, obj):
        return "admin:{}".format("_".join([obj._meta.app_label, obj._meta.model_name]))
    
    def get_admin_url(self, obj, action):
        return '{}_{}'.format(self.get_admin_url_prefix(obj), action)
    
    def get_admin_change_url(self, obj):
        return reverse(self.get_admin_url(obj, "change"), args=(obj.pk,))
    
    def run_full_clean(self, *args):
        for obj in args:
            obj.full_clean()
    
    def _test_identifier_selected_in_html(self, url, value):
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        options = soup.find_all('option', value=value)
        self.assertTrue(options, "No options found with value '%s'.  All options: %s" % (value, soup.find_all('option')))
        for option in options:
            try:
                selected = option["selected"]
            except KeyError:
                selected = "Key error.  Option html: %s" % option
            self.assertEqual(selected, "selected")
    
    def test_identifier_o2o_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierO2OValue.objects.create(id=obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)
    
    def test_identifier_fk_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierFKValue.objects.create(data=obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)
    
    def test_identifier_m2m_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MValue.objects.create()
        rel.data.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)
    
    def test_identifier_all_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierAllValue.objects.create(o2o=obj, fk=obj)
        rel.m2m.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)
    
    def test_identifier_m2m_o2opk_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MO2OPKValue.objects.create(id=obj)
        rel.m2m.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)

    def test_identifier_m2m_o2oid_html_pk(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MO2OPKValue.objects.create(pk=obj.pk)
        rel.m2m.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)
    
    def test_identifier_m2m_o2oid_html_id(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MO2OPKValue.objects.create(id=obj)
        rel.m2m.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.id)
    
    def test_identifier_m2m_o2o_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MO2OValue.objects.create(o2o=obj)
        rel.m2m.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    def test_identifier_m2m_fk_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MFKValue.objects.create(fk=obj)
        rel.m2m.add(obj)
        self.run_full_clean(obj, rel)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
        