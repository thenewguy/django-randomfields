from unittest import skipIf, skipUnless
from django import VERSION as DJANGO_VERSION

DJANGO_VERSION_17 = DJANGO_VERSION < (1, 8) and (1, 7) <= DJANGO_VERSION
DJANGO_VERSION_LT_18 = DJANGO_VERSION < (1, 8)