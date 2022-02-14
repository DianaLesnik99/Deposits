from django.contrib import admin
from .models import *


class MessagesAdmin(admin.ModelAdmin):
    model = Messages
    list_filter = ('date',)

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['login', 'first_name', 'last_name', 'email', 'phone']
    search_fields = ('login', 'first_name', 'last_name', 'email')


admin.site.register(Messages)
admin.site.register(User)

