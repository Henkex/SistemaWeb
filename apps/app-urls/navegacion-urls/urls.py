from django.urls import path
from apps.almacen.views import *
app_name	=	'navegacion'

urlpatterns	=	[
	path('',InventarioAdmin.as_view()),
]