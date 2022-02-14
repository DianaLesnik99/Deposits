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


class EnterpriseAdmin(admin.ModelAdmin):
    model = Enterprise
    list_display = ['name', 'tin', 'director']
    search_fields = ('name', 'tin', 'director',)
    ordering = ('id',)


class LicenseAdmin(admin.ModelAdmin):
    model = License
    list_display = ['name', 'id_enterprise', 'start_date', 'end_date']
    search_fields = ('name', 'id_enterprise__name',)
    ordering = ('id',)
    list_filter = ('cancelled', 'start_date', 'end_date')


class MunicipalityAdmin(admin.ModelAdmin):
    model = Municipality
    list_display = ['name', 'id_deposit', 'id_area']
    search_fields = ('name', 'id_deposit__name', 'id_area__name')
    ordering = ('id_deposit',)
    list_filter = ('id_municipality_type',)


class MunicipalityTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Area, AreaAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(MunicipalityType, MunicipalityTypeAdmin)
