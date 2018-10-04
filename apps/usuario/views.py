from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class Login(View):
    form_class              =   LoginForm
    template_name           =   'login.html'
    user_check_failure_path =   '/login'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form_class()
        return render(request, self.template_name, {'form':form })

    def post(self,request):
        form = self.form_class(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)
                if request.GET:
                    return redirect(request.GET['next'])
                else:
                    return redirect('/')
        return render(request, self.template_name, {'form': form, 'error': 'La cuenta esta deshabilitada'})

class Logout(View):
    def get(self,request):
            logout(request)
            return redirect('/login')

class LoginRequiredMixin(object):
    u"""Se asegura que el usuario este autentificado para acceder a las vistas!."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)