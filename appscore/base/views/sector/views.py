import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView

from appscore.base.forms import SectorForm
from appscore.base.models import Sector

class SectorListView(LoginRequiredMixin,ListView):
    model = Sector
    template_name = 'sector/sector_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(SectorListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in Sector.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado sectores"
        context['create_url'] = reverse_lazy('baseu:sector_create')
        return context

class SectorCreateView(LoginRequiredMixin,CreateView):
    model = Sector
    form_class = SectorForm
    template_name = 'sector/sector_crt.html'
    success_url =  reverse_lazy('baseu:sector_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  SectorForm(body)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': True})
                else:
                    data['error'] = form.errors
            else:
                data['error'] ={'name': ['No ha ingresado a ninguna accion']}
        except Exception as e:
            data['error'] =  {'name': [str(e)]}
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Creacion de sectores"
        context['list_url'] = reverse_lazy('baseu:sector_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(SectorCreateView, self).dispatch(request, *args, **kwargs)

class SectorUpdateView(LoginRequiredMixin,UpdateView):
    model = Sector
    form_class = SectorForm
    template_name = 'sector/sector_crt.html'
    success_url = reverse_lazy('baseu:sector_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = SectorForm(body, instance=self.object)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': True})
                else:
                    data['error'] = form.errors
            else:
                data['error'] ={'name': ['No ha ingresado a ninguna accion']}
        except Exception as e:
            data['error'] =  {'name': [str(e)]}
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar sector"
        context['list_url'] = reverse_lazy('baseu:sector_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SectorUpdateView, self).dispatch(request, *args, **kwargs)

class SectorDeleteView(LoginRequiredMixin,DeleteView):
    model = Sector
    template_name = "sector/sector_dlt.html"
    success_url = reverse_lazy('baseu:sector_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            with transaction.atomic():
                self.object.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            data['error'] = {'name': [str(e)]}
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar sector"
        context['list_url'] = reverse_lazy('baseu:sector_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SectorDeleteView, self).dispatch(request, *args, **kwargs)


