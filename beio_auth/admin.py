# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from beio_auth.models import BeioUser
from beio_auth.forms import UserCreationForm, PasswordRestForm, ChangeUserForm


# Register your models here.

class BeioUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = ChangeUserForm
    # add_fieldsets = (
    #     (u'基本信息', {'fields': ('date_of_birth',)}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'fields': ('date_of_birth', )}
    #      ),
    # )
    # search_fields = ('username',)
    ordering = ('date_joined',)
    # filter_horizontal = ()


admin.site.register(BeioUser, BeioUserAdmin)
# admin.site.unregister(Group)
# admin.site.register(BeioUser)
