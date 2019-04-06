from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.models.user import User

admin.site.register(User, UserAdmin)