import datetime
import time

from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
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
        return context


# Список недропользователей
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


# Информация о недропользователях
class SubsoilUserDetailView(DetailView):
    model = SubsoilUsers
    context_object_name = 'subsoil_user'
    template_name = 'subsoil_user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deposit'] = Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs.get('pk')).order_by(
            '-id_license__start_date')
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
        context['loc_dep'] = LocalitiesDeposit.objects.filter(id_locality=self.kwargs.get('pk')).values(
            'id_deposit__name',
            'id_deposit__id_area__name',
            'id_deposit__id_license__name',
            'direction',
            'distance',
        )
        return context


class TestView(View):

    def get(self, request, *args, **kwargs):
        form = SubsoilUsersForm
        return render(request, '11.html', {'form': form})


# Отчеты в PDF
# class GeneratePDFLocality(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('pdf_report/locality_pdf.html')
#         context = {'locality': Localities.objects.get(pk=self.kwargs['pk']),
#                    'loc_dep': LocalitiesDeposit.objects.filter(id_locality=self.kwargs['pk']).values(
#                        'id_deposit__name',
#                        'id_deposit__id_area__name',
#                        'id_deposit__id_license__name',
#                        'direction',
#                        'distance',
#                    ),
#                    'static': 'C:/Python/Django/Deposits/static/font/DejaVuSans.ttf',
#                    'static_img': 'C:/Python/Django/Deposits/static/font/Carousel1.jpg',
#                    }
#
#         html = template.render(context)
#         pdf = render_to_pdf('pdf_report/locality_pdf.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Report_Locality_" + str(context['locality'].id) + "_" + time.strftime("%Y.%m.%d") + ".pdf"
#             content = "inline; filename='%s'" % (filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" % (filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")
#
#
# class GeneratePDFSubsoilUser(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('pdf_report/subsoil_user_pdf.html')
#         context = {'subsoil_user': SubsoilUsers.objects.get(pk=self.kwargs['pk']),
#                    'deposit': Deposit.objects.filter(id_license__id_subsoil_users=self.kwargs['pk']),
#                    }
#         html = template.render(context)
#         pdf = render_to_pdf('pdf_report/subsoil_user_pdf.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Report_" + str(context['subsoil_user'].id) + "_" + time.strftime("%Y.%m.%d") + ".pdf"
#             content = "inline; filename='%s'" % (filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" % (filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")

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
        # tpl = DocxTemplate("static/doc_report/template.docx")
        tpl.render(context)
        tpl.save(byte_io)
        byte_io.seek(0)
        return FileResponse(byte_io, as_attachment=True,
                            filename='Отчет_' + str(locality.name) + '_' + time.strftime("%Y.%m.%d %H.%M.%S") + '.docx')
        # tpl.render(context)
        # tpl.save('deposit/templates/doc_report/Отчет_' + str(locality.name) + '_' + time.strftime("%Y.%m.%d %H.%M.%S") + '.docx')
        # return HttpResponseRedirect(
        #     request.META.get('HTTP_REFERER', '/locality_detail/' + str(self.kwargs['pk']) + '/'))


class GenerateDOCXSubsoilUser(View):
    def get(self, request, *args, **kwargs):
        asset_url = 'static/doc_report/report_subsoil_user.docx'
        tpl = DocxTemplate(asset_url)
        subsoil_user = SubsoilUsers.objects.get(pk=self.kwargs['pk'])
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
                       'id_license__destination')
                   }
        byte_io = BytesIO()
        # tpl = DocxTemplate("deposit/templates/doc_report/template.docx")
        tpl.render(context)
        tpl.save(byte_io)
        byte_io.seek(0)
        return FileResponse(byte_io, as_attachment=True,
                            filename='Отчет_' + str(subsoil_user.name) + '_' + time.strftime(
                                "%Y.%m.%d %H.%M.%S") + '.docx')
        # tpl.render(context)
        # tpl.save('deposit/templates/doc_report/Отчет_' + str(locality.name) + '_' + time.strftime("%Y.%m.%d %H.%M.%S") + '.docx')
        # return HttpResponseRedirect(
        #     request.META.get('HTTP_REFERER', '/locality_detail/' + str(self.kwargs['pk']) + '/'))
