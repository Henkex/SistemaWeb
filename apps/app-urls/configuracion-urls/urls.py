from django.urls import path
from apps.almacen.views import *
app_name	=	'configuracion'
urlpatterns	=	[
	
	path('empresa/lista',ListaEmpresa.as_view(),name='list_empresa'),
	path('empresa/crear',CrearEmpresa.as_view(),name='crear_empresa'),
	path('empresa/editar/<pk>/',ActualizarEmpresa.as_view(),name='actualizar_empresa'),
	path('empresa/eliminar/<pk>/', EliminarEmpresa.as_view(),name='borrar_empresa'),
]
