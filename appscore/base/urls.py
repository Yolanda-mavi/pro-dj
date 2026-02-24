from itertools import product

from django.urls import path

from appscore.base.views.dashboard.views import DashboardView
#from appscore.base.views.product.views import product_list
from appscore.base.views.product.views import *
from appscore.base.views.bom.views import *



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

]