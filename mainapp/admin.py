from django.contrib import admin

from .models import Area, Deposit, Enterprise, License, Messages, Municipality, MunicipalityType, User

admin.site.register(Area)
admin.site.register(Deposit)
admin.site.register(Enterprise)
admin.site.register(License)
admin.site.register(Messages)
admin.site.register(Municipality)
admin.site.register(MunicipalityType)
admin.site.register(User)
