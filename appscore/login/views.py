from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView
from django.urls import reverse_lazy
from core import settings


# Create your views here.

class LoginFormLogin(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        #print(request.user)#VERIFICA SI TIENE SESSION
        if request.user.is_authenticated:
            # return redirect('baseu:product_list')
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super(LoginFormLogin, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(LoginFormLogin, self).get_context_data(**kwargs)
        context['title'] = 'iniciar sesion'
        return context
#funciona de ambas formas depende lo que ocupas hacer
class LoginFormLogin2(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('baseu:product_list')

    def dispatch(self, request, *args, **kwargs):
        #print(request.user)#VERIFICA SI TIENE SESSION
        if request.user.is_authenticated:
            return redirect('baseu:product_list')
        return super(LoginFormLogin2, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super(LoginFormLogin2, self).get_context_data(**kwargs)
        context['title'] = 'iniciar sesion'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutRedirectView, self).dispatch(request, *args, **kwargs)