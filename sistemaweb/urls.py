"""sistemaweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from apps.usuario.views import Login,Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.app-urls.navegacion-urls.urls')),

    # path('producto/',include('apps.app-urls.producto-urls.urls', namespace='productos')),
    # path('configuracion/',include('apps.app-urls.configuracion-urls.urls', namespace='configuracion')),
    path('almacen/',include('apps.app-urls.almacen-urls.urls', namespace='almacen')),
    path('taller/',include('apps.app-urls.taller-urls.urls', namespace='taller')),

    path('login/',Login.as_view()),
    path('logout/', Logout.as_view()),
]
