from django.contrib import admin

from profiles.models.profilePicture import ProfilePicture
from profiles.models.user import User
from django.contrib.gis.admin import OSMGeoAdmin

# admin.site.register(User, UserAdmin)

admin.site.register(ProfilePicture)

@admin.register(User)
class UserAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')