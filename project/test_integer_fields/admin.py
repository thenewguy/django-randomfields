from django.contrib import admin
from models import RandomIntegerFieldDemo, RandomSmallIntegerFieldDemo

class RandomIntegerFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomIntegerFieldDemo, RandomIntegerFieldDemoAdmin)

class RandomSmallIntegerFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomSmallIntegerFieldDemo, RandomSmallIntegerFieldDemoAdmin)