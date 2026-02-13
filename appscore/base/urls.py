from itertools import product

from django.urls import path

#from appscore.base.views.product.views import product_list
from appscore.base.views.product.views import *



app_name = 'baseu'
urlpatterns = [
    #path('product/list/',product_list)
   # path('uno/',myfirstview),
    #path('dos/',mysecondview)
 #   path('product/list/', product_list,name='product_list'),
    path('product/list/', ProductListView.as_view() ,name='product_list'),
    path('product/list2/', product_list ,name='product_list2'),
    path('product/add/', ProductCreateView.as_view() ,name='product_create'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view() ,name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view() ,name='product_delete'),
]