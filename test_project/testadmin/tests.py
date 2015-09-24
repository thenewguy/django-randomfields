from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from randomfields.tests.models import TestIdentifierValue, TestIdentifierO2OValue, TestIdentifierFKValue, TestIdentifierM2MValue, TestIdentifierAllValue

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
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        options = soup.find_all('option', value=value)
        self.assertTrue(options)
        selected_options = []
        for option in options:
            try:
                selected_options.append(option["selected"] == "selected")
            except KeyError:
                selected_options.append(False)
        self.assertTrue(all(selected_options))
    
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
        rel = TestIdentifierAllValue.objects.create(id=obj, fk=obj)
        rel.m2m.add(obj)
        self._test_identifier_selected_in_html(self.get_admin_change_url(rel), obj.pk)
        