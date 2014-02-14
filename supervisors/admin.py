from django.contrib import admin

# Register your models here.
from supervisors.models import *

admin.site.register(ServerGroup)
admin.site.register(Server)

