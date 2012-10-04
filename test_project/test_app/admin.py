from django.contrib import admin
from models import Instances

class InstancesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Instances, InstancesAdmin)