from django.http import HttpResponseRedirect
# import http

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView
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
    def dispatch(self, request, *args, **kwargs):
         return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # data = {'name': 'Hola5',}
        data = {}
        try:
            # pord =Product.objects.get(pk=request.POST['id']) nomalr llamada

            #pord =Product.objects.get(pk=25)

           # data['name'] = pord.name #para corrida normal por campo
            data = Product.objects.get(pk=request.POST['id']).tojson() #devuelve el diccionado creado en modesl
        except Exception as e:
            data['errord'] = str(e)
            return JsonResponse(data)


        return JsonResponse(data)


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
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs) #para que envie el titulo
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Creacion de productos"

        return context



