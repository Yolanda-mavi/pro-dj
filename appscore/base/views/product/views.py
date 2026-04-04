import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
#from django.http import HttpResponseRedirect
# import http
#from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from unicodedata import category

#import appscore.base.urls
from appscore.base.forms import ProductForm, CategoryForm, ProductUomForm, comun_layout,customfield2_layout
from appscore.base.models import Product, Category,ProductSupplier,models, Partner, ProductUom


def product_list(request):
    data = {'name': 'Hola',
            'products': Product.objects.all(),
            'title':"Listado de productos"}

    return render(request, 'product/product_lst.html', data)

class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'product/product_lst.html'
    #permission_required = 'base.view_product' es un mixion que valida si el susuario tiene el permiso par ver etitar etc
    # @method_decorator(login_required)
    #despues tambien se debe agregar el tocken
    #@method_decorator(csrf_exempt)#se usa para que no tenga seguridad de login este lugar
    # @method_decorator(login_required) se puede agregar el mixin en vez del decorador
    def dispatch(self, request, *args, **kwargs):
         return super(ProductListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        #print("post search--")
        try:
            body = json.loads(request.body)
            action = body.get('action')
            #print(action)
            #print("action--")
            if action == 'searchdata':
                data =[]
                #print("hola search data")
                for i in Product.objects.all():
                    data.append(i.tojson())
                #data = list(Product.objects.values('id', 'name'))
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
            #print("el erro try")
            #data['error'] =  {'name': [str(e)]} marca error
        return JsonResponse(data, safe=False)
    # def post(self, request, *args, **kwargs):
    #     # data = {'name': 'Hola5',}
    #     data = {}
    #     try:
    #         # pord =Product.objects.get(pk=request.POST['id']) nomalr llamada
    #         #pord =Product.objects.get(pk=25)
    #        # data['name'] = pord.name #para corrida normal por campo
    #         data = Product.objects.get(pk=request.POST['id']).tojson() #devuelve el diccionado creado en modesl
    #     except Exception as e:
    #         data['error'] = str(e)
    #         return JsonResponse(data)
    #     return JsonResponse(data)

    # def dispatch(self, request, *args, **kwargs):
    #     #para hacer decoradores o reescritura de metodos gets etc
    #     if request.method == 'GET':
    #         return redirect('baseu:product_list2')
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
        context['title'] = "Listado de productos"
        context['create_url'] = reverse_lazy('baseu:product_create')
        return context

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_crupl.html'
    success_url =  reverse_lazy('baseu:product_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form = ProductForm(body)
                if form.is_valid():
                    with transaction.atomic():
                        Prod = form.save()
                        supplier_lines = []
                        for line in body.get('lines', []):
                            supplier_lines.append(
                                ProductSupplier(
                                    product_id=Prod.id,
                                    partner_id=line['partner_id'],
                                    price=line['price']
                                )
                            )
                        ProductSupplier.objects.bulk_create(supplier_lines)
                    return JsonResponse({'success': True})

                data['error'] = form.errors

            elif action == 'get_suppliers':
                partner = Partner.objects.all().values('id', 'name')
                return JsonResponse(list(partner), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['title'] = "Crear producto"
        context['list_url'] = reverse_lazy('baseu:product_list')
        context['action'] = 'add'
        context['formf_head'] = comun_layout(form, [
            ['name', 'code'],
            ['description', 'description_us'],
            ['category', 'type'],
            ['active', 'status']
        ])
        context['formf_tabinfo'] = comun_layout(form, [
            ['sector', 'country'],
            ['fraction_mx', 'fraction_htsus','fraction_us','fraction_us_exp'],
        ])
        context['formf_customfield2'] = customfield2_layout(form, [
            ['fac_bom', 'fac_bom_uom', 'fac_po', 'fac_po_uom'],
            ['fac_so', 'fac_so_uom', 'fac_co', 'fac_co_uom'],
            ['fac_rate', 'fac_rate_uom', 'fac_rate_us', 'fac_rate_us_uom']
        ])
        context['formf_weigth'] = comun_layout(form, [
            ['weight_pack'],
            ['weight_mat'],
            ['weight'],
        ])
        context['formf_matcost'] = customfield2_layout(form, [
            ['uc_mat_or', 'uc_mat_nor'],
            ['uc_pack_or', 'uc_pack_nor'],
            ['uc_or_stot', 'uc_nor_stot'],
        ])


        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(request, *args, **kwargs)

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_crupl.html'
    success_url = reverse_lazy('baseu:product_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')

            if action == 'edit':

                form = ProductForm(body, instance=self.object)

                if form.is_valid():
                    with transaction.atomic():
                        Prod = form.save()
                        ProductSupplier.objects.filter(product_id=Prod.id).delete()
                        supplier_lines = [
                            ProductSupplier(
                                product_id=Prod.id,
                                price=line['price'],
                                partner_id=line['partner_id']
                            )
                            for line in body.get('lines', [])
                        ]

                        ProductSupplier.objects.bulk_create(supplier_lines)

                    return JsonResponse({'success': True})

                data['error'] = form.errors
            elif action == 'get_lines':
                lines = ProductSupplier.objects.filter(product_id=self.object.id).values(
                    'id',
                    'product_id',
                    'price',
                    'partner_id',
                    product_name=models.F('product_id__name')
                )
                return JsonResponse(list(lines), safe=False)

            elif action == 'get_suppliers':
                suppliers = Partner.objects.all().values('id', 'name')
                return JsonResponse(list(suppliers), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['title'] = "Editar producto"
        context['list_url'] = reverse_lazy('baseu:product_list')
        context['action'] = 'edit'
        context['formf_head'] = comun_layout(form, [
            ['name', 'code'],
            ['description', 'description_us'],
            ['category', 'type'],
            ['active', 'status']
        ])
        context['formf_tabinfo'] = comun_layout(form, [
            ['sector', 'country'],
            ['fraction_mx', 'fraction_htsus', 'fraction_us', 'fraction_us_exp'],
        ])
        context['formf_customfield2'] = customfield2_layout(form, [
            [ 'fac_bom', 'fac_bom_uom','fac_po', 'fac_po_uom'],
            ['fac_so', 'fac_so_uom','fac_co', 'fac_co_uom'],
            ['fac_rate', 'fac_rate_uom','fac_rate_us', 'fac_rate_us_uom']
        ])
        context['formf_weigth'] = comun_layout(form, [
            ['weight_pack'],
            ['weight_mat'],
            ['weight'],
        ])

        context['formf_matcost'] = customfield2_layout(form, [
            ['uc_mat_or', 'uc_mat_nor'],
            ['uc_pack_or', 'uc_pack_nor'],
            ['uc_or_stot', 'uc_nor_stot'],

        ])

        #print("hola update")
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = "product/product_dlt.html"
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

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)



# class ProductCreateView(LoginRequiredMixin,CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'product/product_crt.html'
#     success_url =  reverse_lazy('baseu:product_list')
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         #print("Hola vistas create")
#         #error=''
#         try:
#             #action =request.POST['action']
#             body = json.loads(request.body)
#             action = body.get('action')
#             ##################
#             #para usar imagen se usa este comando
#             #action = request.POST.get('action')
#             ##############################
#             if action == 'add':
#                 #form = self.get_form()
#                 #########################
#                 #para usar iamgen se usa el sigueite
#                 #form = ProductForm(request.POST, request.FILES)
#                 ###################
#                 form =  ProductForm(body)
#                 #form = ProductForm(request.POST) es lo mismo que la linea anterior
#                 if form.is_valid():
#                     form.save()
#                     return JsonResponse({'success': True})
#                     #return JsonResponse({'success': True , 'redirect_url': '/products/' })
#                 else:
#                     #data= form.errors
#                     #error = form.errors
#                     data['error'] = form.errors
#             else:
#                 data['error'] ={'name': ['No ha ingresado a ninguna accion']}
#                 #error = "No ha ingresado a ninguna accion"
#             #data = Product.objects.get(pk=request.POST['id']).tojson()
#         except Exception as e:
#             data['error'] =  {'name': [str(e)]}
#             #error = str(e)
#         return JsonResponse(data)
#         # return JsonResponse({
#         #     'success': False,
#         #     'errors': error
#         # }, status=400)
#     # def post(self, request, *args, **kwargs):
#     #     form = ProductForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         return HttpResponseRedirect(self.success_url)
#     #     self.object = None
#     #     context = self.get_context_data(**kwargs) #para que envie el titulo
#     #     context['form'] = form
#     #     return render(request, self.template_name, context)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Creacion de productos"
#         context['list_url'] = reverse_lazy('baseu:product_list')
#         context['action'] = 'add'
#         return context
#
#     #@method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(ProductCreateView, self).dispatch(request, *args, **kwargs)
#
# class ProductUpdateView(LoginRequiredMixin,UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'product/product_crt.html'
#     success_url = reverse_lazy('baseu:product_list')
#     def post(self, request, *args, **kwargs):
#         data = {}
#         #print("post update edit")
#         try:
#             self.object = self.get_object()
#             body = json.loads(request.body)
#             action = body.get('action')
#             #print("====")
#             #print(action)
#             if action == 'edit':
#                 form = ProductForm(body, instance=self.object)
#                 #form =  ProductForm(body)
#                 if form.is_valid():
#                     form.save()
#                     return JsonResponse({'success': True})
#                 else:
#                     data['error'] = form.errors
#             else:
#                 data['error'] ={'name': ['No ha ingresado a ninguna accion']}
#         except Exception as e:
#             data['error'] =  {'name': [str(e)]}
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Editar producto"
#         context['list_url'] = reverse_lazy('baseu:product_list')
#         context['action'] = 'edit'
#         #print("hola update")
#         return context
#
#     #@method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

#video 36 quedo mas o menos y comentar el ajax del form
# class ProductFromView(FormView):
#     form_class = ProductForm
#     template_name = 'product/product_create.html'
#     success_url =  reverse_lazy('baseu:product_list')
#     # def __init__(self):
#     #     super().__init__()
#     #     self.fields['name'].widget.attrs['autofocus'] = True
#     def form_valid(self, form):
#         print(form.is_valid())
#         print(form)
#         return super().form_valid(form)
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
#         return context

class CategoryListView(LoginRequiredMixin,ListView):
    model = Category
    template_name = 'product/category_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(CategoryListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    # def get_queryset(self):
    #     ###Nota:para hacer validaciones  o filtres
    #     return Category.objects.all()
    #     # return Product.objects.filter(name__startswith='P')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de categorias"
        context['create_url'] = reverse_lazy('baseu:category_create')
        return context

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'product/category_crt.html'
    success_url =  reverse_lazy('baseu:category_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  CategoryForm(body)
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
        context['title'] = "Crear categorias"
        context['list_url'] = reverse_lazy('baseu:category_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'product/category_crt.html'
    success_url = reverse_lazy('baseu:category_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = CategoryForm(body, instance=self.object)
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
        context['title'] = "Editar Categoria"
        context['list_url'] = reverse_lazy('baseu:category_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = "product/category_dlt.html"
    success_url = reverse_lazy('baseu:category_list')

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
        context['title'] = "Eliminar categoria"
        context['list_url'] = reverse_lazy('baseu:category_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)

class ProductUomListView(LoginRequiredMixin,ListView):
    model = ProductUom
    template_name = 'product/uom_lst.html'

    def dispatch(self, request, *args, **kwargs):
        return super(ProductUomListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data = []
                for i in ProductUom.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado de unidades de medida"
        context['create_url'] = reverse_lazy('baseu:uom_create')
        return context

class ProductUomCreateView(LoginRequiredMixin,CreateView):
    model = ProductUom
    form_class = ProductUomForm
    template_name = 'product/uom_crt.html'
    success_url =  reverse_lazy('baseu:uom_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'add':
                form =  ProductUomForm(body)
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
        context['title'] = "Crear unidade de medida"
        context['list_url'] = reverse_lazy('baseu:uom_list')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(ProductUomCreateView, self).dispatch(request, *args, **kwargs)

class ProductUomUpdateView(LoginRequiredMixin,UpdateView):
    model = ProductUom
    form_class = ProductUomForm
    template_name = 'product/uom_crt.html'
    success_url = reverse_lazy('baseu:uom_list')
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'edit':
                form = ProductUomForm(body, instance=self.object)
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
        context['title'] = "Editar unidad de medida"
        context['list_url'] = reverse_lazy('baseu:uom_list')
        context['action'] = 'edit'
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUomUpdateView, self).dispatch(request, *args, **kwargs)

class ProductUomDeleteView(LoginRequiredMixin,DeleteView):
    model = ProductUom
    template_name = "product/uom_dlt.html"
    success_url = reverse_lazy('baseu:uom_list')

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
        context['title'] = "Eliminar unidad de medida"
        context['list_url'] = reverse_lazy('baseu:uom_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUomDeleteView, self).dispatch(request, *args, **kwargs)



