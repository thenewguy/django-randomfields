from django.contrib import admin
from models import RandomIntegerFieldDemo

class RandomIntegerFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomIntegerFieldDemo, RandomIntegerFieldDemoAdmin)