from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('history/', HistoryView.as_view(), name='history'),
    path('test/', TestView.as_view(), name='test'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
