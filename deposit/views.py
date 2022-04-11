import time
from django.shortcuts import render
from django.db.models import Sum, F
from django.views.generic import DetailView, View, ListView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from docxtpl import DocxTemplate
from io import BytesIO

from .forms import *


# Главная страница
class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


# Страница с историй золотодобычи
class HistoryView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'history.html')


# Карта Забайкальского края
class MapView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'map.html')


# Информация о районе
class AreaDetailView(DetailView):
    model = Area
    context_object_name = 'area'
    template_name = 'area_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit'] = Deposit.objects.filter(id_area=self.kwargs['pk'])
        context['a_b_c1'] = Deposit.objects.filter(id_area=self.kwargs.get('pk')).aggregate(
            abc1=Sum('a_b_c1'))
        context['c2'] = Deposit.objects.filter(id_area=self.kwargs.get('pk')).aggregate(
            c2=Sum('c2'))
        context['off_balance'] = Deposit.objects.filter(id_area=self.kwargs.get('pk')).aggregate(
            off_balance=Sum('off_balance'))
        return context


# Список недропользователей
class SubsoilUsersView(ListView):
    model = SubsoilUsers
    queryset = SubsoilUsers.objects.all().order_by('name')
    context_object_name = 'subsoil_users'
    template_name = 'subsoil_users.html'
    paginate_by = 15


def pagination_subsoil_user(request):
    subsoil_users = SubsoilUsers.objects.all().order_by('name')
    paginator = Paginator(subsoil_users, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'subsoil_users.html', {'page_obj': page_obj})


# Диаграмма распределения запасов между недропользователями
def deposit_balance_chart(request):
    labels = []
    data = []
    # queryset = Deposit.objects.aggregate(deposit_balance=Sum('a_b_c1')+Sum('c2'))
    queryset = Deposit.objects.values('id_license__id_subsoil_users__name').annotate(
        deposit_balance=Sum('a_b_c1') + Sum('c2') + Sum('off_balance')).order_by(
        '-deposit_balance')[:5]
    for dep in queryset:
        labels.append(dep['id_license__id_subsoil_users__name'])
        data.append(dep['deposit_balance'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


# Информация о недропользователях
class SubsoilUserDetailView(DetailView):
    model = SubsoilUsers
    context_object_name = 'subsoil_user'
    template_name = 'subsoil_user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit'] = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).order_by(
            '-id_license__start_date')
        context['a_b_c1'] = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).aggregate(
            abc1=Sum('a_b_c1'))
        context['c2'] = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).aggregate(
            c2=Sum('c2'))
        context['off_balance'] = Deposit.objects.filter(
            id_license__id_subsoil_users=self.kwargs.get('pk')).aggregate(off_balance=Sum('off_balance'))
        return context


# Список населенных пунктов
class LocalitiesView(ListView):
    model = Area
    queryset = Area.objects.all().order_by('name')
    context_object_name = 'area'
    template_name = 'localities.html'

    def get_queryset(self):
        return Area.objects.prefetch_related('localities').all()


# Информация о населенных пунктах
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


# Отчеты DOCX
class GenerateDOCXLocality(View):
    def get(self, request, *args, **kwargs):
        asset_url = 'static/doc_report/report_locality.docx'
        tpl = DocxTemplate(asset_url)
        locality = Localities.objects.get(pk=self.kwargs['pk'])
        context = {'loc_name': locality.name,
                   'loc_type': locality.id_locality_type.name,
                   'loc_area': locality.id_area.name,
                   'loc_dep': LocalitiesDeposit.objects.filter(id_locality=self.kwargs['pk']).values(
                       'id_deposit__name',
                       'id_deposit__id_area__name',
                       'id_deposit__id_license__name',
                       'direction',
                       'distance')
                   }
        byte_io = BytesIO()
        tpl.render(context)
        tpl.save(byte_io)
        byte_io.seek(0)
        return FileResponse(byte_io, as_attachment=True,
                            filename='Отчет_' + str(locality.name) + '_' + time.strftime("%d.%m.%Y %H.%M.%S") + '.docx')


class GenerateDOCXSubsoilUser(View):
    def get(self, request, *args, **kwargs):
        asset_url = 'static/doc_report/report_subsoil_user.docx'
        tpl = DocxTemplate(asset_url)
        subsoil_user = SubsoilUsers.objects.get(pk=self.kwargs['pk'])
        a_b_c1 = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).aggregate(
            abc1=Sum('a_b_c1'))
        c2 = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).aggregate(
            c2=Sum('c2'))
        off_balance = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).aggregate(
            off_balance=Sum('off_balance'))
        context = {'sub_name': subsoil_user.name,
                   'tin': subsoil_user.tin,
                   'iec': subsoil_user.iec,
                   'psrn_psrnsp': subsoil_user.psrn_psrnsp,
                   'date_of_registration': subsoil_user.date_of_registration,
                   'director': subsoil_user.director,
                   'deposit': Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs['pk']).values(
                       'id_license__name',
                       'name',
                       'a_b_c1',
                       'c2',
                       'off_balance',
                       'id_license__start_date',
                       'id_license__end_date',
                       'id_license__cancelled',
                       'id_license__destination'),
                   'a_b_c1': a_b_c1,
                   'c2': c2,
                   "off_balance": off_balance
                   }
        byte_io = BytesIO()
        tpl.render(context)
        tpl.save(byte_io)
        byte_io.seek(0)
        return FileResponse(byte_io, as_attachment=True,
                            filename='Отчет_' + str(subsoil_user.name) + '_' + time.strftime(
                                "%d.%m.%Y %H.%M.%S") + '.docx')


class GenerateDOCXArea(View):
    def get(self, request, *args, **kwargs):
        asset_url = 'static/doc_report/report_area.docx'
        tpl = DocxTemplate(asset_url)
        area = Area.objects.get(pk=self.kwargs['pk'])
        a_b_c1 = Deposit.objects.filter(id_area=self.kwargs.get('pk')).aggregate(
            abc1=Sum('a_b_c1'))
        c2 = Deposit.objects.filter(id_area=self.kwargs.get('pk')).aggregate(
            c2=Sum('c2'))
        off_balance = Deposit.objects.filter(id_area=self.kwargs.get('pk')).aggregate(
            off_balance=Sum('off_balance'))
        context = {'area_name': area.name,
                   'official_portal': area.official_portal,
                   'deposit': Deposit.objects.filter(id_area=self.kwargs['pk']).values(
                       'name',
                       'id_license__id_subsoil_users__name',
                       'id_license__name',
                       'id_license__cancelled',
                       'id_license__destination',
                       'a_b_c1',
                       'c2',
                       'off_balance'),
                   'a_b_c1': a_b_c1,
                   'c2': c2,
                   "off_balance": off_balance
                   }
        byte_io = BytesIO()
        tpl.render(context)
        tpl.save(byte_io)
        byte_io.seek(0)
        return FileResponse(byte_io, as_attachment=True,
                            filename='Отчет_' + str(area.name) + '_район_' + time.strftime(
                                "%d.%m.%Y %H.%M.%S") + '.docx')
