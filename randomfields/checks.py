from django import VERSION as DJANGO_VERSION

DJANGO_VERSION_17 = DJANGO_VERSION < (1, 8) and (1, 7) <= DJANGO_VERSION
DJANGO_VERSION_LT_18 = DJANGO_VERSION < (1, 8)
DJANGO_VERSION_LT_19 = DJANGO_VERSION < (1, 9)
DJANGO_VERSION_LT_20 = DJANGO_VERSION < (2, 0)
