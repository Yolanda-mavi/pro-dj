
from django.urls import path
from appscore.mrp.views.bom.views import *

app_name = 'mrpu'
urlpatterns = [
    path('bom/add/', BomCreateView.as_view() ,name='bom_create'),
    path('bom/list/', BomListView.as_view() ,name='bom_list'),
    path('bom/edit/<int:pk>/', BomUpdateView.as_view() ,name='bom_update'),
    path('bom/delete/<int:pk>/', BomDeleteView.as_view() , name='bom_delete'),
]