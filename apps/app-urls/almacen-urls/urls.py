from django.urls import path
from django.conf.urls import url
from apps.almacen.views import *
app_name	=	'almacen'
urlpatterns	=	[
	
	path('almacen/parte_de_ingreso',ParteIngresoView.as_view(),name='parte_ingreso'),
	path('almacen/guia_de_remision',GuiaRemisionView.as_view(),name='guia_remision'),

	# URL de Funciones de selects dinamicos
	# path('operaciones/getproducto/',getProductosAlmacen, name='getProductosAlmacen'),
	url(r'^operaciones/getstock/(\d+)/$',getStockProductos,name='getStockProductos'),
	# path('operaciones/getstock/(d)/(d)/',getStockProductos, name='getStockProductos'),

	path('prueba/<pk>',ServicioOrdenTrabajo.as_view(),name='prueba'),
	
]