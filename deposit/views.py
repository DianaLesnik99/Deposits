from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
from django.core.paginator import Paginator

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


class SubsoilUsersView(ListView):
    model = SubsoilUsers
    queryset = SubsoilUsers.objects.all().order_by('name')
    context_object_name = 'subsoil_users'
    template_name = 'subsoil_users.html'
    paginate_by = 20


def pagination_subsoil_user(request):
    subsoil_users = SubsoilUsers.objects.all().order_by('name')
    paginator = Paginator(subsoil_users, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'subsoil_users.html', {'page_obj': page_obj})


class SubsoilUserDetailView(DetailView):
    model = SubsoilUsers
    context_object_name = 'subsoil_user'
    template_name = 'subsoil_user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lisense'] = License.objects.filter(id_subsoil_users=self.kwargs.get('pk'))
        context['deposit'] = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).order_by(
            '-id_license__start_date')
        return context


class LocalitiesView(ListView):
    model = Area
    queryset = Area.objects.all().order_by('name')
    context_object_name = 'area'
    template_name = 'localities.html'
    # paginate_by = 20

    def get_queryset(self):
        return Area.objects.prefetch_related('localities').all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['localities'] = Localities.objects.filter(id_area=self.kwargs.get('pk'))
    #     return context
#
#
# def pagination_localities(request):
#     municipality = Localities.objects.all().order_by('name')
#     paginator = Paginator(municipality, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'localities.html', {'page_obj': page_obj})


class LocalityDetailView(DetailView):
    model = Localities
    context_object_name = 'locality'
    template_name = 'locality_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loc_dep'] = LocalitiesDeposit.objects.filter(id_locality=self.kwargs.get('pk'))
        return context


class TestView(View):

    def get(self, request, *args, **kwargs):
        form = SubsoilUsersForm
        return render(request, '11.html', {'form': form})
