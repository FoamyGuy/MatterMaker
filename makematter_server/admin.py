from django.contrib import admin

# Register your models here.
from makematter_server.models import MatterObject, MatterTemplate, MatterTemplateVar

admin.site.register(MatterObject)
admin.site.register(MatterTemplate)
admin.site.register(MatterTemplateVar)