from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.models import User, VerificationCode
from accounts.froms import UserAdminCreationForm, UserAdminChangeForm



class UserAdmin(BaseUserAdmin, admin.ModelAdmin,):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = (
        "username",
        "email",
        "full_name",
        "created_on",
        "is_active",
    )
    list_filter = (
        "is_active",
        "is_admin",

    )
    fieldsets = (
        (None, {"fields": (
            "username",
            "email",
            "password"
        )}),
        (
            "Personal info",
            {
                "fields": (
                    "full_name",
                    "phone_number",

                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": (
            "email",
            "username",
            "password1",
            "password2"
        )}),
    )
    search_fields = (
        "email",
        "username",
        "full_name",
        "phone_number"
    )

    ordering = ("full_name",)
    filter_horizontal = ()
    actions = [
        "disable_users",
        "enable_users",
    ]


    def disable_users(self, request, queryset):
        queryset.update(is_active=False)

    def enable_users(self, request, queryset):
        queryset.update(is_active=True)


admin.site.register(User, UserAdmin)
admin.site.register(VerificationCode)
admin.site.unregister(Group)

class CustomAdmin(AdminSite):
    admin.site.site_header = "Admin Dashboard"
    admin.site.site_title = "Dashboard"
    admin.site.index_title = ""
    admin.site.index_template = "admin/custom_index.html"

