import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView,FormView
from appscore.mrp.forms import BomForm
from appscore.mrp.models import Bom,Bomline
from appscore.inventory.models import Product
from django.utils import timezone

class BomCreateView(LoginRequiredMixin,CreateView):
    model = Bom
    form_class = BomForm
    template_name = 'bom/bom_crupl.html'
    success_url =  reverse_lazy('baseu:dashboard')

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #
    #     try:
    #         body = json.loads(request.body)
    #         action = body.get('action')
    #
    #         if action == 'add':
    #             form = BomForm(body)
    #
    #             if form.is_valid():
    #                 with transaction.atomic():
    #                     bom = form.save()
    #                     bom_lines =[]
    #                     for line in body.get('lines', []):
    #                         bom_lines.append(
    #                             Bomline(
    #                                 bom_id=bom.id,
    #                                 product_id=line['product'],
    #                                 quantity=line['quantity']
    #                             )
    #                         )
    #                     Bomline.objects.bulk_create(bom_lines)
    #
    #                 print("Terminar")
    #                 return JsonResponse({'success': True})
    #
    #             data['error'] = form.errors
    #
    #         elif action == 'get_products':
    #             products = Product.objects.all().values('id', 'name')
    #             return JsonResponse(list(products), safe=False)
    #
    #     except Exception as e:
    #         data['error'] = str(e)
    #
    #     return JsonResponse(data)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            user = request.user
            now = timezone.now()
            if action == 'add':
                form = BomForm(body)
                if form.is_valid():
                    with transaction.atomic():
                        Bom = form.save()
                        bom_lines = []
                        for line in body.get('lines', []):
                            bom_lines.append(
                                Bomline(
                                    bom_id=Bom.id,
                                    product_id=line['product_id'],
                                    quantity=line['quantity'],
                                    created_by=user,
                                    updated_by=user,
                                    created_dt=now,
                                    updated_dt=now
                                )
                            )
                        Bomline.objects.bulk_create(bom_lines)
                    return JsonResponse({'success': True})

                data['error'] = form.errors
            elif action == 'get_products':
                products = Product.objects.all().values('id', 'name')
                return JsonResponse(list(products), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Crear lista de materiales"
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
        try:
            body = json.loads(request.body)
            action = body.get('action')
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
        ###Nota:aqui podemos agarrar datos de contres para revisarlo
        #context['name'] = "Hola" #para el pasado forma de no clase
        #context['products'] = Product.objects.all() #para el pasado forma de no clases
        context['title'] = "Listas de materiales"
        context['create_url'] = reverse_lazy('mrpu:bom_create')
        return context

class BomUpdateView(LoginRequiredMixin, UpdateView):
    model = Bom
    form_class = BomForm
    template_name = 'bom/bom_crupl.html'
    success_url = reverse_lazy('mrpu:bom_list')


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')
            user = request.user
            now = timezone.now()

            if action == 'edit':

                form = BomForm(body, instance=self.object)
                print("Hola 1")
                if form.is_valid():
                    with transaction.atomic():
                        bom = form.save()

                        lines = body.get('lines', [])

                        existing_ids = set(
                            Bomline.objects.filter(bom_id=bom.id).values_list('id', flat=True)
                        )
                        print("Hola 2")
                        incoming_ids = set()
                        to_create = []
                        to_update = []

                        for line in lines:
                            line_id = int(line['id']) if line.get('id') else None
                            print("hola 3")
                            if line_id:
                                print("Hola update")
                                incoming_ids.add(line_id)
                                to_update.append(
                                    Bomline(
                                        id=line_id,
                                        bom_id=bom.id,
                                        product_id=line['product_id'],
                                        quantity=line['quantity'],
                                        updated_by=user,
                                        updated_dt=now
                                    )
                                )
                            else:
                                print("hola create")
                                print(bom)
                                print(bom.id)
                                print(line['product_id'])
                                print(line['quantity'])
                                to_create.append(
                                    Bomline(
                                        bom_id=bom.id,
                                        product_id=line['product_id'],
                                        quantity=line['quantity'],
                                        created_by=user,
                                        updated_by=user,
                                        created_dt=now,
                                        updated_dt=now
                                    )
                                )
                                print("despues")
                        #print(to_create)
                        print("----")
                        if to_create:
                            print("entra a create")
                            print(to_create)
                            Bomline.objects.bulk_create(to_create)

                        if to_update:
                            Bomline.objects.bulk_update(
                                to_update,
                                ['product_id', 'quantity', 'updated_by', 'updated_dt']
                            )

                        to_delete = existing_ids - incoming_ids
                        if to_delete:
                            Bomline.objects.filter(id__in=to_delete).delete()

                    return JsonResponse({'success': True})

                data['error'] = form.errors
            elif action == 'get_lines':
                print("entra a getlines")
                lines = Bomline.objects.filter(bom_id=self.object.id).values(
                    'id',
                    'bom_id',
                    'product_id',
                    'quantity',
                )
                print(lines)
                return JsonResponse(list(lines), safe=False)

            elif action == 'get_products':
                products = Product.objects.all().values('id', 'name')
                return JsonResponse(list(products), safe=False)

        except Exception as e:
            print("informacion error 235")
            print(e)
            data['error'] = str(e)

        return JsonResponse(data)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #
    #     try:
    #         self.object = self.get_object()
    #         body = json.loads(request.body)
    #         action = body.get('action')
    #
    #         if action == 'edit':
    #
    #             form = BomForm(body, instance=self.object)
    #
    #             if form.is_valid():
    #                 with transaction.atomic():
    #
    #                     bom = form.save()
    #                     Bomline.objects.filter(bom_id=bom.id).delete()
    #                     bom_lines = [
    #                         Bomline(
    #                             bom_id=bom.id,
    #                             product_id=line['product'],
    #                             quantity=line['quantity']
    #                         )
    #                         for line in body.get('lines', [])
    #                     ]
    #
    #                     Bomline.objects.bulk_create(bom_lines)
    #
    #                 return JsonResponse({'success': True})
    #
    #             data['error'] = form.errors
    #
    #
    #         elif action == 'get_lines':
    #             print("entra get_lines")
    #             lines = Bomline.objects.filter(bom_id=self.object.id).values(
    #                 'id',
    #                 'product_id',
    #                 'quantity',
    #                 product_name=models.F('product_id__name')
    #             )
    #             return JsonResponse(list(lines), safe=False)
    #
    #         elif action == 'get_products':
    #             products = Product.objects.all().values('id', 'name')
    #             return JsonResponse(list(products), safe=False)
    #
    #     except Exception as e:
    #         data['error'] = str(e)
    #
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar de lista de materiales"
        context['list_url'] = reverse_lazy('mrpu:bom_list')
        context['action'] = 'edit'
        return context

        # @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super(BomUpdateView, self).dispatch(request, *args, **kwargs)

class BomDeleteView(LoginRequiredMixin,DeleteView):
    model = Bom
    template_name = "bom/bom_dlt.html"
    success_url = reverse_lazy('mrpu:bom_list')

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
        context['list_url'] = reverse_lazy('mrpu:bom_list')
        return context

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BomDeleteView, self).dispatch(request, *args, **kwargs)
