from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('history/', HistoryView.as_view(), name='history'),
    path('map/', MapView.as_view(), name='map'),
    path('subsoil_users/', SubsoilUsersView.as_view(), name='subsoil_users'),
    path('test/', TestView.as_view(), name='test'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
