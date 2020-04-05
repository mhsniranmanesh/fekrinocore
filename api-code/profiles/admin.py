from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from fekrino.profiles.models.user import User
from django.contrib.gis.admin import OSMGeoAdmin

# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')