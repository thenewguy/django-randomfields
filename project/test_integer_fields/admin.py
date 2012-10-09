from django.contrib import admin
from models import RandomBigIntegerFieldDemo, RandomIntegerFieldDemo, RandomSmallIntegerFieldDemo, \
                   RandomBigIntegerIdentifierFieldDemo, RandomIntegerIdentifierFieldDemo, RandomSmallIntegerIdentifierFieldDemo

class RandomBigIntegerFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomBigIntegerFieldDemo, RandomBigIntegerFieldDemoAdmin)

class RandomIntegerFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomIntegerFieldDemo, RandomIntegerFieldDemoAdmin)

class RandomSmallIntegerFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomSmallIntegerFieldDemo, RandomSmallIntegerFieldDemoAdmin)
admin.site.register(RandomBigIntegerIdentifierFieldDemo)
admin.site.register(RandomIntegerIdentifierFieldDemo)
admin.site.register(RandomSmallIntegerIdentifierFieldDemo)