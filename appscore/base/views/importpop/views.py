import csv

from appscore.base.forms import ImportForm
from django.shortcuts import render,get_object_or_404
#from django.db import models
#from appscore.base.models import FractionUsExp,FractionUs,FractionHtsus,FractionMx,Sector,Country
from appscore.base import models
import io
from django.db import transaction

#from django.http import JsonResponse

def get_order_cols(objModel,header_row):
    order_header = []
    nrow =0
    for col in header_row:

        for field in objModel._meta.fields:
            # if col.strip() == field.verbose_name or col == field.verbose_name :
            if col == field.verbose_name:
                model_related = ''
                if field.get_internal_type() == 'ForeignKey':
                    model_related = field.related_model.__name__
                order_header.append({'nrow':nrow,'name':field.name,'type':field.get_internal_type() ,'model_related':model_related})
        nrow = nrow + 1
    return order_header

def get_format_obj(objModelRelated,list_options_tem):
    obj_list=[]
    for rowlst in list_options_tem:
        obj_list.append( objModelRelated(name=rowlst) )
    return obj_list

def get_list_foreign_keys(lista_csv,order_header):
    matrix_foreign_keys = []
    #num_col = 0
    for rh in order_header:
        list_options_tem=[]
        if rh['type'] == 'ForeignKey':
            objModelRelated = getattr(models, rh['model_related'])
            num_row = 0
            for row in lista_csv:
                if num_row == 0:
                    num_row = 1
                    continue
                #print("renglon====")
                #print(row[num_col])
                #obj_rel_id = objModelRelated.objects.get(name=row[num_col])
                #obj_rel_id = get_object_or_404(objModelRelated, name=row[num_col] )
                #queryset = objModelRelated.objects.filter(name=row[num_col])
                queryset = objModelRelated.objects.filter(name=row[rh['nrow']])
                #if queryset.count()==1:
                #first_obj = queryset.first()
                #print(first_obj)
                #print("------****")
                #if  queryset.count()==0 and row[num_col] not in list_options_tem:
                #    list_options_tem.append(row[num_col])
                if  queryset.count()==0 and row[rh['nrow']] not in list_options_tem:
                    list_options_tem.append(row[rh['nrow']])

            matrix_foreign_keys.append({'name':rh['model_related'],'array': get_format_obj(objModelRelated,list_options_tem)})

        #num_col = num_col + 1
    return matrix_foreign_keys



def import_modal_view(request):
    show_modal = False  # Bandera para el template

    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file_data']
            file_data = csv_file.read().decode('utf-8')
            io_string = io.StringIO(file_data)
            reader = csv.reader(io_string, delimiter=',', quotechar='"')
            lista_csv = list(reader)
            objModel = getattr(models, form.cleaned_data['model_name'])
            order_header = []
            matrix_foreign_keys = []
            if lista_csv:
                header_row=[]
                for row in lista_csv:
                    header_row = row
                    break
                order_header = get_order_cols(objModel,header_row)
                matrix_foreign_keys = get_list_foreign_keys(lista_csv,order_header)

            if lista_csv:
                with transaction.atomic():
                    #import foreignKey#########################
                    for lin in matrix_foreign_keys:
                        if lin['array'] and lin['name']:
                            objModelRelated = getattr(models, lin['name'])
                            objModelRelated.objects.bulk_create(lin['array'] )
                        break
                    ##########################
                    num_row = 0
                    for row in lista_csv:
                        if num_row == 0:
                            num_row = 1
                            continue
                        dict_pack = {}
                        #num_col=0
                        for rh in order_header:
                            #if order_c[1]== 'ForeignKey':
                            if rh['type']== 'ForeignKey':
                                #print("foreig===")
                                # objModelRelated = getattr(models, order_c[2])
                                # obj_rel_id = objModelRelated.objects.get(name=order_c[0])
                                # if not obj_rel_id:
                                #     obj_rel_id = objModelRelated.objects.create(name=order_c[0])
                                #     dict_pack[order_c[0]] = obj_rel_id
                                #objModelRelated = getattr(models, order_c[2])
                                objModelRelated = getattr(models, rh['model_related'])
                                #obj_rel_id = objModelRelated.objects.get(name=row[num_col])
                                #dict_pack[order_c['name']] = obj_rel_id
                                #print("=========")
                                #print(row[num_col])
                                queryset = objModelRelated.objects.filter(name=row[rh['nrow']])
                                #blog_id = objModelRelated.objects.filter(name='My Awesome Blog').values_list('id',  flat=True).first()
                                if queryset.count()==1:
                                    first_obj = queryset.first()
                                    dict_pack[rh['name']+'_id'] = first_obj.id
                                else:
                                    print("enviar error de registros duplicados")
                                # try:
                                #     obj_id = objModelRelated.objects.get(name=row[num_col]).id
                                #     print("encuentra categoria")
                                #     dict_pack[order_c['name']] = obj_id
                                # except objModelRelated.DoesNotExist:
                                #     print("envia el error")
                                #     pass
                            else:
                                #print("normal======")
                                dict_pack[ rh['name'] ]= row[rh['nrow']]

                            #num_col = num_col + 1
                        if dict_pack:
                            objModel.objects.create( **dict_pack)

            # for field in Book._meta.get_fields():
            #     if field.get_internal_type() == "ForeignKey":
            #         print(f"Field '{field.name}' links to Model: {field.related_model.__name__}")
            # for line in lines:
            #     rows = line.split(',')
            #     for row in rows:

                # if form.cleaned_data['model_name'] == 'FractionMx':
            #    print("---")

            # Bomline(
            #     bom_id=bom.id,
            #     product_id=line['product'],
            #     quantity=line['quantity']
            # )
            # Bomline.objects.bulk_create(bom_lines)
            #
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


            # Usar el módulo csv para procesar
            #reader = csv.reader(lines)

            # Redirigir para evitar resubmisión al recargar
            return render(request, 'dashboard/dashboard.html', {'form': ImportForm(), 'show_modal': False})
        else:
            print(form.errors)
            print("opcion 4")
            # Si hay error, mostrar el modal de nuevo con los errores
            show_modal = True
    else:
        form = ImportForm()

    return render(request, 'importpop/importpop.html', {'form': form, 'show_modal': show_modal})


def import_modal_view2(request):

    show_modal = False  # Bandera para el template
    print("linea 8")
    print(request.method)
    if request.method == 'POST':
        #form = ImportForm(request.POST)
        form = ImportForm(request.POST, request.FILES)
        print("opcion 2")
        #form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("opcion 1")
            # Procesar datos (form.cleaned_data)
            #print(form.cleaned_data)
            csv_file = request.FILES['file_data']

            # Decodificar el archivo para lectura
            file_data = csv_file.read().decode('utf-8')
            lines = file_data.split('\n')
            #print(lines)
            objModel = getattr(models, form.cleaned_data['model_name'])
            # for line in lines:
            #     for cols in line.split(','):
            order_cols = []
            if lines.len()>0:
                cols = lines[0].split(',')
                for col in cols:
                    for field in objModel._meta.fields:
                        #if col.strip() == field.verbose_name or col == field.verbose_name :
                        if col == field.verbose_name :
                            model_related=''
                            if field.get_internal_type() == 'ForeignKey':
                                model_related = field.related_model.__name__

                            order_cols.append([ field.name , field.get_internal_type(), model_related ] )
                            #print(f"Campo: {field.name}, Tipo: {field.get_internal_type()}")
                            #print(field.verbose_name)

                for line_file in lines[1:]:
                    cols_file = line_file.split(',')
                    dict_pack = {}
                    num_col=0
                    for order_c in order_cols:
                        if order_c[1]== 'ForeignKey':
                            objModelRelated = getattr(models, order_c[2])
                            # for fieldRelated in objModelRelated._meta.fields:
                            #     if fieldRelated.name == 'name':
                            #         model_related_field = 'name'
                            #         break
                            #buscar si ya existe y validar si tiene campo name
                            obj_rel_id = objModelRelated.objects.get(name=order_c[0])
                            if not obj_rel_id:
                                obj_rel_id = objModelRelated.objects.create(name=order_c[0])
                                dict_pack[order_c[0]] = obj_rel_id
                        else:
                            dict_pack[ order_c[0] ]= cols_file[num_col]

                        num_col = num_col + 1
                    if dict_pack:
                        objModel.objects.create( **dict_pack)

            # for field in Book._meta.get_fields():
            #     if field.get_internal_type() == "ForeignKey":
            #         print(f"Field '{field.name}' links to Model: {field.related_model.__name__}")
            # for line in lines:
            #     rows = line.split(',')
            #     for row in rows:

                # if form.cleaned_data['model_name'] == 'FractionMx':
            #    print("---")

            # Bomline(
            #     bom_id=bom.id,
            #     product_id=line['product'],
            #     quantity=line['quantity']
            # )
            # Bomline.objects.bulk_create(bom_lines)
            #
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


            # Usar el módulo csv para procesar
            #reader = csv.reader(lines)

            # Redirigir para evitar resubmisión al recargar
            return render(request, 'dashboard/dashboard.html', {'form': ImportForm(), 'show_modal': False})
        else:
            print(form.errors)
            print("opcion 4")
            # Si hay error, mostrar el modal de nuevo con los errores
            show_modal = True
    else:
        form = ImportForm()

    return render(request, 'importpop/importpop.html', {'form': form, 'show_modal': show_modal})


# def import_modal_view(request):
#     print(request.method)
#     print("=======")
#     if request.method == 'POST':
#         form = ImportForm(request.POST)
#
#         if form.is_valid():
#             print(form.cleaned_data)
#
#             return JsonResponse({
#                 'success': True
#             })
#
#         else:
#             return render(request, 'importpop/importpop.html', {
#                 'form': form
#             })
#
#     else:
#         form = ImportForm()
#
#     return render(request, 'importpop/importpop.html', {
#         'form': form
#     })
