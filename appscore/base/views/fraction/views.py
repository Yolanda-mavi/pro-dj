import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView

from appscore.base.forms import FractionMxForm,FractionUsForm,FractionHtsusForm,FractionUsExpForm
from appscore.base.models import  FractionMx, FractionUs, FractionHtsus,FractionUsExp

class FractionMxListView(LoginRequiredMixin,ListView):
    model = FractionMx
    template_name = 'fraction/fmx_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(FractionMxListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in FractionMx.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de fracciones arancelarias mexicanas"
        context['create_url'] = reverse_lazy('baseu:fmx_create')
        return context

class FractionMxCreateView(LoginRequiredMixin,CreateView):
    model = FractionMx
    form_class = FractionMxForm
    template_name = 'fraction/fmx_crt.html'
    success_url =  reverse_lazy('baseu:fmx_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  FractionMxForm(body)
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
        context['title'] = "Creacion de fracción arancelaria mexicana"
        context['list_url'] = reverse_lazy('baseu:fmx_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(FractionMxCreateView, self).dispatch(request, *args, **kwargs)

class FractionMxUpdateView(LoginRequiredMixin,UpdateView):
    model = FractionMx
    form_class = FractionMxForm
    template_name = 'fraction/fmx_crt.html'
    success_url = reverse_lazy('baseu:fmx_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = FractionMxForm(body, instance=self.object)
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
        context['title'] = "Editar e fracción arancelaria mexicana"
        context['list_url'] = reverse_lazy('baseu:fmx_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionMxUpdateView, self).dispatch(request, *args, **kwargs)

class FractionMxDeleteView(LoginRequiredMixin,DeleteView):
    model = FractionMx
    template_name = "fraction/fmx_dlt.html"
    success_url = reverse_lazy('baseu:fmx_list')

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
        context['title'] = "Eliminar e fracción arancelaria mexicana"
        context['list_url'] = reverse_lazy('baseu:fmx_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionMxDeleteView, self).dispatch(request, *args, **kwargs)

class FractionHtsusListView(LoginRequiredMixin,ListView):
    model = FractionHtsus
    template_name = 'fraction/fhtsus_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(FractionHtsusListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in FractionHtsus.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de fracciones HTSUS"
        context['create_url'] = reverse_lazy('baseu:fhtsus_create')
        return context

class FractionHtsusCreateView(LoginRequiredMixin,CreateView):
    model = FractionHtsus
    form_class = FractionHtsusForm
    template_name = 'fraction/fhtsus_crt.html'
    success_url =  reverse_lazy('baseu:fhtsus_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  FractionMxForm(body)
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
        context['title'] = "Creacion de fracción HTSUS"
        context['list_url'] = reverse_lazy('baseu:fhtsus_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(FractionHtsusCreateView, self).dispatch(request, *args, **kwargs)

class FractionHtsusUpdateView(LoginRequiredMixin,UpdateView):
    model = FractionHtsus
    form_class = FractionHtsusForm
    template_name = 'fraction/fhtsus_crt.html'
    success_url = reverse_lazy('baseu:fhtsus_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = FractionHtsusForm(body, instance=self.object)
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
        context['title'] = "Editar e fracción HTSUS"
        context['list_url'] = reverse_lazy('baseu:fhtsus_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionHtsusUpdateView, self).dispatch(request, *args, **kwargs)

class FractionHtsusDeleteView(LoginRequiredMixin,DeleteView):
    model = FractionHtsus
    template_name = "fraction/fhtsus_dlt.html"
    success_url = reverse_lazy('baseu:fhtsus_list')

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
        context['title'] = "Eliminar e fracción HTSUS"
        context['list_url'] = reverse_lazy('baseu:fhtsus_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionHtsusDeleteView, self).dispatch(request, *args, **kwargs)

class FractionUsListView(LoginRequiredMixin,ListView):
    model = FractionUs
    template_name = 'fraction/fus_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in FractionUs.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de fracciones de usa"
        context['create_url'] = reverse_lazy('baseu:fus_create')
        return context

class FractionUsCreateView(LoginRequiredMixin,CreateView):
    model = FractionUs
    form_class = FractionUsForm
    template_name = 'fraction/fus_crt.html'
    success_url =  reverse_lazy('baseu:fus_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  FractionUsForm(body)
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
        context['title'] = "Creacion de fracción de usa"
        context['list_url'] = reverse_lazy('baseu:fus_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsCreateView, self).dispatch(request, *args, **kwargs)

class FractionUsUpdateView(LoginRequiredMixin,UpdateView):
    model = FractionUs
    form_class = FractionUsForm
    template_name = 'fraction/fus_crt.html'
    success_url = reverse_lazy('baseu:fus_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = FractionMxForm(body, instance=self.object)
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
        context['title'] = "Editar e fracción de usa"
        context['list_url'] = reverse_lazy('baseu:fus_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsUpdateView, self).dispatch(request, *args, **kwargs)

class FractionUsDeleteView(LoginRequiredMixin,DeleteView):
    model = FractionUs
    template_name = "fraction/fus_dlt.html"
    success_url = reverse_lazy('baseu:fus_list')

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
        context['title'] = "Eliminar e fracción de usa"
        context['list_url'] = reverse_lazy('baseu:fus_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsDeleteView, self).dispatch(request, *args, **kwargs)

class FractionUsExpListView(LoginRequiredMixin,ListView):
    model = FractionUsExp
    template_name = 'fraction/fusexp_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsExpListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in FractionUsExp.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de fracciones de usa para exportación"
        context['create_url'] = reverse_lazy('baseu:fusexp_create')
        return context

class FractionUsExpCreateView(LoginRequiredMixin,CreateView):
    model = FractionUsExp
    form_class = FractionUsExpForm
    template_name = 'fraction/fusexp_crt.html'
    success_url =  reverse_lazy('baseu:fusexp_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  FractionUsExpForm(body)
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
        context['title'] = "Creacion de fracción de usa para exportación"
        context['list_url'] = reverse_lazy('baseu:fusexp_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsExpCreateView, self).dispatch(request, *args, **kwargs)

class FractionUsExpUpdateView(LoginRequiredMixin,UpdateView):
    model = FractionUsExp
    form_class = FractionUsExpForm
    template_name = 'fraction/fusexp_crt.html'
    success_url = reverse_lazy('baseu:fusexp_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = FractionMxForm(body, instance=self.object)
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
        context['title'] = "Editar e fracción de usa para exportación"
        context['list_url'] = reverse_lazy('baseu:fusexp_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsExpUpdateView, self).dispatch(request, *args, **kwargs)

class FractionUsExpDeleteView(LoginRequiredMixin,DeleteView):
    model = FractionUsExp
    template_name = "fraction/fusexp_dlt.html"
    success_url = reverse_lazy('baseu:fusexp_list')

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
        context['title'] = "Eliminar e fracción de usa para exportación"
        context['list_url'] = reverse_lazy('baseu:fusexp_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FractionUsExpDeleteView, self).dispatch(request, *args, **kwargs)






