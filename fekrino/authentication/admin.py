from django.contrib import admin

# Register your models here.
from authentication.models.phoneActivation import PhoneActivationToken

admin.site.register(PhoneActivationToken)