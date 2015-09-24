from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.six import text_type
from randomfields.tests.models import TestIdentifierM2MO2OPKValue, TestIdentifierM2MFKValue, TestIdentifierValue, TestIdentifierO2OValue, TestIdentifierFKValue, TestIdentifierM2MValue, TestIdentifierAllValue, TestIdentifierM2MO2OValue
from unittest import skip

class DatabaseTest(TestCase):
    def test_superuser_exists(self):
        User = get_user_model()
        user = User.objects.get(username=settings.SUPERUSER_USERNAME)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(settings.SUPERUSER_PASSWORD))

class AdminTests(TestCase):
    def setUp(self):
        self.client.login(username=settings.SUPERUSER_USERNAME, password=settings.SUPERUSER_PASSWORD)
    
    def get_admin_url_prefix(self, obj):
        return "admin:{}".format("_".join([obj._meta.app_label, obj._meta.model_name]))
    
    def get_admin_url(self, obj, action):
        return '{}_{}'.format(self.get_admin_url_prefix(obj), action)
    
    def get_admin_change_url(self, obj):
        return reverse(self.get_admin_url(obj, "change"), args=(obj.pk,))
    
    def _test_identifier_selected_in_html(self, url, value):
        print(type(value))
        value = text_type(value)
        print(type(value))
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
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    def test_identifier_fk_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierFKValue.objects.create(data=obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    def test_identifier_m2m_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MValue.objects.create()
        rel.data.add(obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    def test_identifier_all_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierAllValue.objects.create(o2o=obj, fk=obj)
        rel.m2m.add(obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    @skip("Known to fail. Need to figure out why it passes a model instance to the field's get_prep_value and how to handle it.")
    def test_identifier_m2m_o2opk_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MO2OPKValue.objects.create(pk=obj)
        rel.m2m.add(obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    def test_identifier_m2m_o2o_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MO2OValue.objects.create(o2o=obj)
        rel.m2m.add(obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
    
    def test_identifier_m2m_fk_html(self):
        obj = TestIdentifierValue.objects.create()
        rel = TestIdentifierM2MFKValue.objects.create(fk=obj)
        rel.m2m.add(obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
        