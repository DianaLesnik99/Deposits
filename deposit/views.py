from django.shortcuts import render
from django.views.generic import DetailView, View


class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class HistoryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'history.html')


class TestView(View):

    def get(self, request, *args, **kwargs):
        return render(request, '11.html')
