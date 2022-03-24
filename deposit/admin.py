from django.contrib import admin

from .models import *


class AreaAdmin(admin.ModelAdmin):
    model = Area
    search_fields = ('name',)
    ordering = ('name',)


class DepositAdmin(admin.ModelAdmin):
    model = Deposit
    list_display = ['name', 'id_license', 'id_area']
    search_fields = ('name', 'id_license__name', 'id_area__name')
    ordering = ('id',)
    list_filter = ('development',)


class SubsoilUsersAdmin(admin.ModelAdmin):
    model = SubsoilUsers
    list_display = ['name', 'tin', 'director']
    search_fields = ('name', 'tin', 'director',)
    ordering = ('id',)


class LicenseAdmin(admin.ModelAdmin):
    model = License
    list_display = ['name', 'get_deposit', 'id_subsoil_users', 'start_date', 'end_date']
    search_fields = ('name', 'id_subsoil_users__name',)
    ordering = ('id',)
    list_filter = ('cancelled', 'start_date', 'end_date')


class LocalitiesAdmin(admin.ModelAdmin):
    model = Localities
    list_display = ['name', 'id_locality_type', 'id_area']
    search_fields = ('name', 'id_locality_type__name', 'id_area__name')
    ordering = ('name',)
    list_filter = ('id_locality_type',)


class LocalitiesTypeAdmin(admin.ModelAdmin):
    model = LocalitiesType
    search_fields = ('name',)
    ordering = ('name',)


class LocalitiesDepositAdmin(admin.ModelAdmin):
    model = LocalitiesDeposit
    list_display = ['id_locality', 'id_deposit', 'direction', 'distance']
    search_fields = ('id_locality__name', 'id_deposit__name')
    ordering = ('id_deposit',)


admin.site.register(Area, AreaAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(SubsoilUsers, SubsoilUsersAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Localities, LocalitiesAdmin)
admin.site.register(LocalitiesType, LocalitiesTypeAdmin)
admin.site.register(LocalitiesDeposit, LocalitiesDepositAdmin)
