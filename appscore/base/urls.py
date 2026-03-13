from itertools import product

from django.urls import path

from appscore.base.models import FractionHtsus
from appscore.base.views.dashboard.views import DashboardView
#from appscore.base.views.product.views import product_list
from appscore.base.views.product.views import *
from appscore.base.views.bom.views import *
from appscore.base.views.importpop.views import *
# from appscore.base.views.uom.views import *
from appscore.base.views.country.views import *
from appscore.base.views.sector.views import *
from appscore.base.views.fraction.views import *


app_name = 'baseu'
urlpatterns = [
    #path('product/list/',product_list)
   # path('uno/',myfirstview),
    #path('dos/',mysecondview)
 #   path('product/list/', product_list,name='product_list'),
    path('product/list/', ProductListView.as_view() ,name='product_list'),
    # path('porduct/list2/', product_list ,name='product_list2'),
    path('product/add/', ProductCreateView.as_view() ,name='product_create'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view() ,name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view() ,name='product_delete'),
    # path('porduct/form/', ProductFromView.as_view() ,name='product_form'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('category/list/', CategoryListView.as_view() ,name='category_list'),
    path('category/add/', CategoryCreateView.as_view() ,name='category_create'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view() ,name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view() ,name='category_delete'),

    path('bom/add/', BomCreateView.as_view() ,name='bom_create'),
    path('bom/list/', BomListView.as_view() ,name='bom_list'),
    path('bom/edit/<int:pk>/', BomUpdateView.as_view() ,name='bom_update'),
    path('bom/delete/<int:pk>/', BomDeleteView.as_view() , name='bom_delete'),

    path('uom/list/', ProductUomListView.as_view() ,name='uom_list'),
    path('uom/add/', ProductUomCreateView.as_view() ,name='uom_create'),
    path('uom/edit/<int:pk>/', ProductUomUpdateView.as_view() ,name='uom_update'),
    path('uom/delete/<int:pk>/', ProductUomDeleteView.as_view() ,name='uom_delete'),

    path('country/list/', CountryListView.as_view(), name='country_list'),
    path('country/add/', CountryCreateView.as_view(), name='country_create'),
    path('country/edit/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),

    path('sector/list/', SectorListView.as_view(), name='sector_list'),
    path('sector/add/', SectorCreateView.as_view(), name='sector_create'),
    path('sector/edit/<int:pk>/', SectorUpdateView.as_view(), name='sector_update'),
    path('sector/delete/<int:pk>/', SectorDeleteView.as_view(), name='sector_delete'),

    path('fhtsus/list/', FractionHtsusListView.as_view(), name='fhtsus_list'),
    path('fhtsus/add/', FractionHtsusCreateView.as_view(), name='fhtsus_create'),
    path('fhtsus/edit/<int:pk>/', FractionHtsusUpdateView.as_view(), name='fhtsus_update'),
    path('fhtsus/delete/<int:pk>/', FractionHtsusDeleteView.as_view(), name='fhtsus_delete'),

    path('fmx/list/', FractionMxListView.as_view(), name='fmx_list'),
    path('fmx/add/', FractionMxCreateView.as_view(), name='fmx_create'),
    path('fmx/edit/<int:pk>/', FractionMxUpdateView.as_view(), name='fmx_update'),
    path('fmx/delete/<int:pk>/', FractionMxDeleteView.as_view(), name='fmx_delete'),

    path('fus/list/', FractionUsListView.as_view(), name='fus_list'),
    path('fus/add/', FractionUsUpdateView.as_view(), name='fus_create'),
    path('fus/edit/<int:pk>/', FractionUsUpdateView.as_view(), name='fus_update'),
    path('fus/delete/<int:pk>/', FractionUsDeleteView.as_view(), name='fus_delete'),

    path('fusexp/list/', FractionUsExpListView.as_view(), name='fusexp_list'),
    path('fusexp/add/', FractionUsExpUpdateView.as_view(), name='fusexp_create'),
    path('fusexp/edit/<int:pk>/', FractionUsExpUpdateView.as_view(), name='fusexp_update'),
    path('fusexp/delete/<int:pk>/', FractionUsExpDeleteView.as_view(), name='fusexp_delete'),

    path('import/add/', import_modal_view ,name='import_modal'),

]