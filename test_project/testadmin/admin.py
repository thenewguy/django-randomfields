from django.contrib import admin
from randomfields.tests.models import TestIdentifierM2MO2OPKValue, TestIdentifierM2MFKValue, TestIdentifierValue, TestIdentifierO2OValue, TestIdentifierFKValue, TestIdentifierM2MValue, TestIdentifierAllValue, TestIdentifierM2MO2OValue

admin.site.register(TestIdentifierValue)
admin.site.register(TestIdentifierO2OValue)
admin.site.register(TestIdentifierFKValue)
admin.site.register(TestIdentifierM2MValue)
admin.site.register(TestIdentifierAllValue)
admin.site.register(TestIdentifierM2MO2OValue)
admin.site.register(TestIdentifierM2MFKValue)
admin.site.register(TestIdentifierM2MO2OPKValue)