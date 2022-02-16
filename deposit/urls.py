from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]