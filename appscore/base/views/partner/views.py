import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView,FormView
from appscore.base.forms import PartnerForm, comun_layout
from appscore.base.models import Partner,models



class PartnerCreateView(LoginRequiredMixin,CreateView):
    model = Partner
    form_class = PartnerForm
    template_name = 'partner/partner_crupl.html'
    success_url =  reverse_lazy('baseu:dashboard')

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            body = json.loads(request.body)
            action = body.get('action')

            if action == 'add':
                form = ParnerForm(body)

                if form.is_valid():
                    with transaction.atomic():
                        partner = form.save()
                        # partner_lines =[]
                        # for line in body.get('lines', []):
                        #     partner_lines.append(
                        #         Partnerline(
                        #             bom_id=bom.id,
                        #             product_id=line['product'],
                        #             quantity=line['quantity']
                        #         )
                        #     )
                        #Partnerline.objects.bulk_create(partner_lines)


                    return JsonResponse({'success': True})

                data['error'] = form.errors

            elif action == 'get_partners':
                partners = Partner.objects.all().values('id', 'name')
                return JsonResponse(list(partners), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['title'] = "Crear de contacto"
        context['list_url'] = reverse_lazy('baseu:partner_list')
        context['action'] = 'add'
        context['formf_head'] = comun_layout(form,[
            ['customer','supplier','agency','repr','driver'],
            ['name'],
            ['first_surname', 'second_surname'],
            ['phone', 'mobile','email', 'website'],
        ])
        context['formf_tabinfo'] = comun_layout(form, [
            ['patent', 'active'],
            ['curp', 'rfc'],
            ['irs', 'alr'],
        ])
        context['formf_tabdir'] = comun_layout(form, [
            ['country', 'state', 'city', 'address'],
            ['address_num', 'address_num_int', 'zip', 'po_box']
        ])

        return context

    def dispatch(self, request, *args, **kwargs):
        return super(PartnerCreateView, self).dispatch(request, *args, **kwargs)

class PartnerListView(LoginRequiredMixin,ListView):
    model = Partner
    template_name = 'partner/partner_lst.html'

    def dispatch(self, request, *args, **kwargs):
         return super(PartnerListView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            body = json.loads(request.body)
            action = body.get('action')
            if action == 'searchdata':
                data =[]
                for i in Partner.objects.all():
                    data.append(i.tojson())
            else:
                data['error'] = {'name': ["Ha ocurrido un error"]}
        except Exception as e:
            print(str(e))
        return JsonResponse(data, safe=False)


    def get_queryset(self):
        ###Nota:para hacer validaciones  o filtres
        return Partner.objects.all()
        #return Product.objects.filter(name__startswith='P')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = "Listas de contactos"
        context['create_url'] = reverse_lazy('baseu:partner_create')
        return context

class PartnerUpdateView(LoginRequiredMixin, UpdateView):
    model = Partner
    form_class = PartnerForm
    template_name = 'partner/partner_crupl.html'
    success_url = reverse_lazy('baseu:partner_list')

    def post(self, request, *args, **kwargs):
        data = {}

        try:
            self.object = self.get_object()
            body = json.loads(request.body)
            action = body.get('action')

            if action == 'edit':

                form = PartnerForm(body, instance=self.object)

                if form.is_valid():
                    with transaction.atomic():

                        partner = form.save()
                        Partnerline.objects.filter(partner_id=parner.id).delete()
                        # partner_lines = [
                        #     Parnerline(
                        #         bom_id=bom.id,
                        #         product_id=line['product'],
                        #         quantity=line['quantity']
                        #     )
                        #     for line in body.get('lines', [])
                        # ]

                        Partnerline.objects.bulk_create(partner_lines)

                    return JsonResponse({'success': True})

                data['error'] = form.errors


            elif action == 'get_lines':
                lines = Partnerline.objects.filter(bom_id=self.object.id).values(
                    'id',
                    'product_id',
                    'quantity',
                    product_name=models.F('product_id__name')
                )
                return JsonResponse(list(lines), safe=False)

            elif action == 'get_partners':
                partners = Partner.objects.all().values('id', 'name')
                return JsonResponse(list(partners), safe=False)

        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        context['title'] = "Editar de lista contactos"
        context['list_url'] = reverse_lazy('baseu:partner_list')
        context['action'] = 'edit'
        context['formf_head'] = comun_layout(form, [
            ['customer', 'supplier', 'agency', 'repr', 'driver'],
            ['name'],
            ['first_surname', 'second_surname'],
            ['phone', 'mobile', 'email', 'website'],
        ])
        context['formf_tabinfo'] = comun_layout(form, [
            ['patent', 'active'],
            ['curp', 'rfc'],
            ['irs', 'alr'],
        ])
        context['formf_tabdir'] = comun_layout(form, [
            ['country', 'state', 'city', 'address'],
            ['address_num', 'address_num_int', 'zip', 'po_box']
        ])
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(PartnerUpdateView, self).dispatch(request, *args, **kwargs)

class PartnerDeleteView(LoginRequiredMixin,DeleteView):
    model = Partner
    template_name = "partner/partner_dlt.html"
    success_url = reverse_lazy('baseu:partner_list')

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
        context['title'] = "Eliminar contacto"
        context['list_url'] = reverse_lazy('baseu:partner_list')
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(PartnerDeleteView, self).dispatch(request, *args, **kwargs)

