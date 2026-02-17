from django.urls import path
from appscore.login.views import *

urlpatterns = [
    path('', LoginFormLogin.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'), no me sirvio video 39
    path('logout/', LogoutRedirectView.as_view(), name='logout'),


]