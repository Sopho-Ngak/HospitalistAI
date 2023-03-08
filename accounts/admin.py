from django.contrib import admin
from accounts.models import User, VerificationCode

admin.site.register(User)
admin.site.register(VerificationCode)

# Register your models here.
