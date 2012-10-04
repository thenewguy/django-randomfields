from django.contrib import admin
from models import RandomCharFieldDemo

class RandomCharFieldDemoAdmin(admin.ModelAdmin):
    pass

admin.site.register(RandomCharFieldDemo, RandomCharFieldDemoAdmin)