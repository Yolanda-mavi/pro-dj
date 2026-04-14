
from django.urls import path
from appscore.rdata.views.partner.views import *

app_name = 'rdatau'

urlpatterns = [

    path('partner/list/', PartnerListView.as_view(), name='partner_list'),
    path('partner/add/', PartnerCreateView.as_view(), name='partner_create'),
    path('partner/edit/<int:pk>/', PartnerUpdateView.as_view(), name='partner_update'),
    path('partner/delete/<int:pk>/', PartnerDeleteView.as_view(), name='partner_delete'),

]