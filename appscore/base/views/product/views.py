import json

from django.db import transaction
from django.http import HttpResponseRedirect
# import http

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView,DeleteView,FormView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

import appscore.base.urls
from appscore.base.forms import ProductForm
from appscore.base.models import Product


def product_list(request):
    data = {'name': 'Hola',
            'products': Product.objects.all(),
            'title':"Listado de produtos"}

    return render(request, 'product/product_list.html', data)

class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'


    # @method_decorator(login_required)
    #despues tambinen se debe agregar el tocken
    @method_decorator(csrf_exempt)#se usa para que no tenga seguridad de login este lugar
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
         return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print("post search--")
        try:
            body = json.loads(request.body)
            action = body.get('action')
            print(action)
            print("action--")
            if action == 'searchdata':
                data =[]
                print("hola search data")
                for i in Product.objects.all():
                    data.append(i.tojson())
                #data = list(Product.objects.values('id', 'name'))
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
            print("el erro try")
            data['error'] =  {'name': [str(e)]}
        return JsonResponse(data, safe=False)


    # def post(self, request, *args, **kwargs):
    #     # data = {'name': 'Hola5',}
    #     data = {}
    #     try:
    #         # pord =Product.objects.get(pk=request.POST['id']) nomalr llamada
    #
    #         #pord =Product.objects.get(pk=25)
    #
    #        # data['name'] = pord.name #para corrida normal por campo
    #         data = Product.objects.get(pk=request.POST['id']).tojson() #devuelve el diccionado creado en modesl
    #     except Exception as e:
    #         data['error'] = str(e)
    #         return JsonResponse(data)
    #
    #
    #     return JsonResponse(data)


    # def dispatch(self, request, *args, **kwargs):
    #     #para hacer decoradores o reescritura de metodos gets etc
    #     if request.method == 'GET':
    #         return redirect('baseu:product_list2')
    #
    #     return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        ###Nota:para hacer validaciones  o filtres
        return Product.objects.all()
        #return Product.objects.filter(name__startswith='P')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ###Nota:aqui podemos agarrar datos de contres para revisarlo
        #context['name'] = "Hola" #para el pasado forma de no clase
        #context['products'] = Product.objects.all() #para el pasado forma de no clases
        context['title'] = "Listado de produtos"
        context['create_url'] = reverse_lazy('baseu:product_create')
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_create.html'
    success_url =  reverse_lazy('baseu:product_list')

    def post(self, request, *args, **kwargs):
        data = {}
        print("Hola vistas create")
        #error=''
        try:
            #action =request.POST['action']
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                #form = self.get_form()
                form =  ProductForm(body)
                #form = ProductForm(request.POST) es lo mismo que la linea anterior
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': True})
                    #return JsonResponse({'success': True , 'redirect_url': '/products/' })
                else:
                    #data= form.errors
                    #error = form.errors
                    data['error'] = form.errors
            else:
                data['error'] ={'name': ['No ha ingresado a ninguna accion']}
                #error = "No ha ingresado a ninguna accion"
            #data = Product.objects.get(pk=request.POST['id']).tojson()
        except Exception as e:
            data['error'] =  {'name': [str(e)]}
            #error = str(e)
        return JsonResponse(data)
        # return JsonResponse({
        #     'success': False,
        #     'errors': error
        # }, status=400)
    # def post(self, request, *args, **kwargs):
    #     form = ProductForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs) #para que envie el titulo
    #     context['form'] = form
    #     return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Creacion de productos"
        context['list_url'] = reverse_lazy('baseu:product_list')
        context['action'] = 'add'

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('baseu:product_list')

    def post(self, request, *args, **kwargs):
        data = {}
        print("post update edit")
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            print("====")
            print(action)
            if action == 'edit':
                form = ProductForm(body, instance=self.object)
                #form =  ProductForm(body)
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
        context['title'] = "Editar producto"
        context['list_url'] = reverse_lazy('baseu:product_list')
        context['action'] = 'edit'
        print("hola update")
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product/product_delete.html"
    success_url = reverse_lazy('baseu:product_list')

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
        context['title'] = "Eliminar producto"
        context['list_url'] = reverse_lazy('baseu:product_list')

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)

#video 36 quedo mas o menos y comentar el ajax del form
# class ProductFromView(FormView):
#     form_class = ProductForm
#     template_name = 'product/product_create.html'
#     success_url =  reverse_lazy('baseu:product_list')
#
#     # def __init__(self):
#     #     super().__init__()
#     #     self.fields['name'].widget.attrs['autofocus'] = True
#
#     def form_valid(self, form):
#         print(form.is_valid())
#         print(form)
#         return super().form_valid(form)
#
#
#     def form_invalid(self, form):
#         print(form.is_valid())
#         print(form.errors)
#         return super().form_invalid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Form de productos"
#         context['list_url'] = reverse_lazy('baseu:product_list')
#         context['action'] = 'add'
#
#         return context

