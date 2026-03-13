import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView

from appscore.base.forms import  CountryForm
from appscore.base.models import Country


class CountryListView(LoginRequiredMixin,ListView):
    model = Country
    template_name = 'country/country_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(CountryListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in Country.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de paises"
        context['create_url'] = reverse_lazy('baseu:country_create')
        return context

class CountryCreateView(LoginRequiredMixin,CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'country/country_crt.html'
    success_url =  reverse_lazy('baseu:country_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  CountryForm(body)
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
        context['title'] = "Creacion de paises"
        context['list_url'] = reverse_lazy('baseu:country_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(CountryCreateView, self).dispatch(request, *args, **kwargs)

class CountryUpdateView(LoginRequiredMixin,UpdateView):
    model = Country
    form_class = CountryForm
    template_name = 'country/country_crt.html'
    success_url = reverse_lazy('baseu:country_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = CountryForm(body, instance=self.object)
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
        context['title'] = "Editar pais"
        context['list_url'] = reverse_lazy('baseu:country_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CountryUpdateView, self).dispatch(request, *args, **kwargs)

class CountryDeleteView(LoginRequiredMixin,DeleteView):
    model = Country
    template_name = "country/country_dlt.html"
    success_url = reverse_lazy('baseu:country_list')

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
        context['title'] = "Eliminar pais"
        context['list_url'] = reverse_lazy('baseu:country_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CountryDeleteView, self).dispatch(request, *args, **kwargs)


