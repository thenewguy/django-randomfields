from django.contrib import admin
from models import RandomCharFieldDemo, WarnAtPercentDemo

class RandomCharFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomCharFieldDemo, RandomCharFieldDemoAdmin)
admin.site.register(WarnAtPercentDemo)