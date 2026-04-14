
from django.urls import path
from appscore.inventory.views.product.views import *
from appscore.inventory.views.fraction.views import *

app_name = 'inventoryu'

urlpatterns = [

    path('product/list/', ProductListView.as_view() ,name='product_list'),
    path('product/add/', ProductCreateView.as_view() ,name='product_create'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view() ,name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view() ,name='product_delete'),

    path('category/list/', CategoryListView.as_view() ,name='category_list'),
    path('category/add/', CategoryCreateView.as_view() ,name='category_create'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view() ,name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view() ,name='category_delete'),

    path('fhtsus/list/', FractionHtsusListView.as_view(), name='fhtsus_list'),
    path('fhtsus/add/', FractionHtsusCreateView.as_view(), name='fhtsus_create'),
    path('fhtsus/edit/<int:pk>/', FractionHtsusUpdateView.as_view(), name='fhtsus_update'),
    path('fhtsus/delete/<int:pk>/', FractionHtsusDeleteView.as_view(), name='fhtsus_delete'),

    path('fmx/list/', FractionMxListView.as_view(), name='fmx_list'),
    path('fmx/add/', FractionMxCreateView.as_view(), name='fmx_create'),
    path('fmx/edit/<int:pk>/', FractionMxUpdateView.as_view(), name='fmx_update'),
    path('fmx/delete/<int:pk>/', FractionMxDeleteView.as_view(), name='fmx_delete'),

    path('fus/list/', FractionUsListView.as_view(), name='fus_list'),
    path('fus/add/', FractionUsCreateView.as_view(), name='fus_create'),
    path('fus/edit/<int:pk>/', FractionUsUpdateView.as_view(), name='fus_update'),
    path('fus/delete/<int:pk>/', FractionUsDeleteView.as_view(), name='fus_delete'),

    path('fusexp/list/', FractionUsExpListView.as_view(), name='fusexp_list'),
    path('fusexp/add/', FractionUsExpCreateView.as_view(), name='fusexp_create'),
    path('fusexp/edit/<int:pk>/', FractionUsExpUpdateView.as_view(), name='fusexp_update'),
    path('fusexp/delete/<int:pk>/', FractionUsExpDeleteView.as_view(), name='fusexp_delete'),

    path('uom/list/', ProductUomListView.as_view() ,name='uom_list'),
    path('uom/add/', ProductUomCreateView.as_view() ,name='uom_create'),
    path('uom/edit/<int:pk>/', ProductUomUpdateView.as_view() ,name='uom_update'),
    path('uom/delete/<int:pk>/', ProductUomDeleteView.as_view() ,name='uom_delete'),
]