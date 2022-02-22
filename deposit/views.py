from django.shortcuts import render
from django.views.generic import DetailView, View

from .forms import *


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class HistoryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'history.html')


class MapView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'map.html')


class SubsoilUsersView(View):

    def get(self, request, *args, **kwargs):
        form = SubsoilUsersForm
        return render(request, 'subsoil_users.html', {'form': form})


class TestView(View):

    def get(self, request, *args, **kwargs):
        return render(request, '11.html')
