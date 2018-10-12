from django.urls import path
from django.conf.urls import url
from apps.almacen.views import *
app_name	=	'almacen'
urlpatterns	=	[
	
	path('parte_de_ingreso',ParteIngresoView.as_view(),name='parte_ingreso'),
	path('guia_de_remision',GuiaRemisionView.as_view(),name='guia_remision'),

	# URL de Funciones de selects dinamicos
	# path('operaciones/getproducto/',getProductosAlmacen, name='getProductosAlmacen'),
	url(r'^operaciones/getstock/(\d+)/$',getStockProductos,name='getStockProductos'),
	# path('operaciones/getstock/(d)/(d)/',getStockProductos, name='getStockProductos'),

	path('prueba/<pk>',ServicioOrdenTrabajo.as_view(),name='prueba'),

	# path('prueba2/',PedidosATiempo,name='prueba2'),
	
	# Inventario 
	path('lista_inventarios/',InicioInventario.as_view(),name='lista_inventarios'),
	path('registro_inventario/<pk>',RegistroInventario.as_view(),name='registro_inventario'),
	path('crear_inventario/',CrearInventario,name='crear_inventario')
]