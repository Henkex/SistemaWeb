from django.urls import path
from apps.producto.views import *
app_name	=	'producto'
urlpatterns	=	[
	
	path('linea_de_producto/lista',ListaLinea.as_view(),name='list_linea'),
	path('linea_de_producto/crear',CrearLinea.as_view(),name='crear_linea'),
	path('linea_de_producto/editar/<pk>/',ActualizarLinea.as_view(),name='actualizar_linea'),
	path('linea_de_producto/eliminar/<pk>/', EliminarLinea.as_view(),name='borrar_linea'),

	path('producto/lista',ListaProducto.as_view(),name='list_producto'),
	path('producto/crear',CrearProducto.as_view(),name='crear_producto'),
	path('producto/editar/<pk>/',ActualizarProducto.as_view(),name='modificar_producto'),
	path('producto/eliminar/<pk>/', EliminarProducto.as_view(),name='borrar_producto'),
]
