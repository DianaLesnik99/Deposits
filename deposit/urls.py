from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('history/', HistoryView.as_view(), name='history'),
    path('map/', MapView.as_view(), name='map'),
    path('area_detail/<int:pk>/', AreaDetailView.as_view(), name='area_detail'),
    path('subsoil_users/', SubsoilUsersView.as_view(), name='subsoil_users'),
    path('subsoil_users_detail/<int:pk>/', SubsoilUserDetailView.as_view(), name='subsoil_user_detail'),
    path('subsoil_users_doc/<int:pk>/', GenerateDOCXSubsoilUser.as_view(), name='subsoil_user_doc'),
    path('localities/', LocalitiesView.as_view(), name='localities'),
    path('locality_detail/<int:pk>/', LocalityDetailView.as_view(), name='locality_detail'),
    # path('locality_pdf/<int:pk>/', GeneratePDFLocality.as_view(), name='locality_pdf'),
    path('locality_doc/<int:pk>/', GenerateDOCXLocality.as_view(), name='locality_doc'),
    # path('subsoil_user_pdf/<int:pk>/', GeneratePDFSubsoilUser.as_view(), name='subsoil_user_pdf'),
    path('test/', TestView.as_view(), name='test'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
