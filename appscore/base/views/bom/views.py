import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView,FormView
from appscore.base.forms import BomForm
from appscore.base.models import Product, Bom,Bomline, models




class BomCreateView(LoginRequiredMixin,CreateView):
    model = Bom
    form_class = BomForm
    template_name = 'bom/bom_crupl.html'
    success_url =  reverse_lazy('baseu:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            body = json.loads(request.body)
            action = body.get('action')

            # 🟢 guardar BOM
            if action == 'add':
                print("addd333")
                form = BomForm(body)

                if form.is_valid():
                    with transaction.atomic():
                        bom = form.save()

                        print("****")
                        print(body.get('lines', []))
                        print("**********")
                        bom_lines =[]
                        for line in body.get('lines', []):
                            bom_lines.append(
                                Bomline(
                                    bom_id=bom.id,
                                    product_id=line['product'],
                                    quantity=line['quantity']
                                )
                            )
                        Bomline.objects.bulk_create(bom_lines)
                            # print("~~~~~~~~~~")
                            # print(line)
                            # print("-----")
                            # print(bom)
                            # #para el id print( Product.objects.get(id=line['product']).id )
                            # Bomline.objects.create(
                            #     bom_id=bom.id,
                            #     product_id=600000,
                            #     quantity=line['quantity']
                            # )
                            # # Bomline.objects.create(
                            # #     bom_id=bom,
                            # #     product_id=Product.objects.get(id=line['product']),
                            # #     quantity=line['quantity']
                            # # )
                    print("Terminar")
                    return JsonResponse({'success': True})

                data['error'] = form.errors

            # elif action == 'searchdata':
            #     return JsonResponse([], safe=False)
            elif action == 'get_products':
                products = Product.objects.all().values('id', 'name')
                return JsonResponse(list(products), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         body = json.loads(request.body)
    #         action = body.get('action')
    #         if action == 'add':
    #             form =  BomForm(body)
    #             if form.is_valid():
    #                 form.save()
    #                 return JsonResponse({'success': True})
    #             else:
    #                 data['error'] = form.errors
    #         else:
    #             data['error'] ={'name': ['No ha ingresado a ninguna accion']}
    #
    #     except Exception as e:
    #         data['error'] =  {'name': [str(e)]}
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Creacion de lista de materiales"
        context['list_url'] = reverse_lazy('baseu:dashboard')
        context['action'] = 'add'
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(BomCreateView, self).dispatch(request, *args, **kwargs)

class BomListView(LoginRequiredMixin,ListView):
    model = Bom
    template_name = 'bom/bom_lst.html'

    def dispatch(self, request, *args, **kwargs):
         return super(BomListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print("accion 123")
        try:
            body = json.loads(request.body)
            action = body.get('action')
            print("la accion de lista")
            print(action)
            if action == 'searchdata':
                data =[]
                for i in Bom.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)


    def get_queryset(self):
        ###Nota:para hacer validaciones  o filtres
        return Bom.objects.all()
        #return Product.objects.filter(name__startswith='P')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("si entra 123")
        ###Nota:aqui podemos agarrar datos de contres para revisarlo
        #context['name'] = "Hola" #para el pasado forma de no clase
        #context['products'] = Product.objects.all() #para el pasado forma de no clases
        context['title'] = "Listas de materiales"
        context['create_url'] = reverse_lazy('baseu:bom_create')
        return context

class BomUpdateView(LoginRequiredMixin, UpdateView):
    model = Bom
    form_class = BomForm
    template_name = 'bom/bom_crupl.html'
    success_url = reverse_lazy('baseu:bom_list')

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')

            if action == 'edit':

                form = BomForm(body, instance=self.object)

                if form.is_valid():
                    with transaction.atomic():

                        bom = form.save()
                        Bomline.objects.filter(bom_id=bom.id).delete()
                        bom_lines = [
                            Bomline(
                                bom_id=bom.id,
                                product_id=line['product'],
                                quantity=line['quantity']
                            )
                            for line in body.get('lines', [])
                        ]

                        Bomline.objects.bulk_create(bom_lines)

                    return JsonResponse({'success': True})

                data['error'] = form.errors

            # elif action == 'get_lines':
            #     lines = Bomline.objects.filter(bom_id=self.object.id).values(
            #         'id',
            #         'product_id',
            #         'quantity',
            #         product_name=models.F('product_id__name')
            #     )
            #     return JsonResponse(list(lines), safe=False)
            elif action == 'get_lines':
                print("entra get_lines")
                lines = Bomline.objects.filter(bom_id=self.object.id).values(
                    'id',
                    'product_id',
                    'quantity',
                    product_name=models.F('product_id__name')
                )
                return JsonResponse(list(lines), safe=False)

            elif action == 'get_products':
                products = Product.objects.all().values('id', 'name')
                return JsonResponse(list(products), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar de lista de materiales"
        context['list_url'] = reverse_lazy('baseu:bom_list')
        context['action'] = 'edit'
        return context

        # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super(BomUpdateView, self).dispatch(request, *args, **kwargs)

class BomDeleteView(LoginRequiredMixin,DeleteView):
    model = Bom
    template_name = "bom/bom_dlt.html"
    success_url = reverse_lazy('baseu:bom_list')

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
        context['title'] = "Eliminar la lista de materiales"
        context['list_url'] = reverse_lazy('baseu:bom_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BomDeleteView, self).dispatch(request, *args, **kwargs)
