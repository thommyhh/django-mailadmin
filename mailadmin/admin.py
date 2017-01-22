from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from django import forms

from .models import *

admin.site.register(Domain)
admin.site.register(Account)
admin.site.register(Alias)
admin.site.register(Mailinglist)
admin.site.register(Redirect)
admin.site.register(ExternalReceiver)


class UserAdditionAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'roles': forms.Select
        }


class UserAdditionsInline(admin.StackedInline):
    model = UserAdditions
    can_delete = False
    form = UserAdditionAdminForm


class UserAdmin(DjangoUserAdmin):
    inlines = (UserAdditionsInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
