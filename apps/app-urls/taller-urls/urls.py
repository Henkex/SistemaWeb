from django.urls import path
from apps.almacen.views import *
app_name	=	'taller'
urlpatterns	=	[
	path('orden_trabajo/',OrdenTrabajoLista.as_view(),name='lista_orden_trabajo'),

	path('orden_trabajo/nuevo',OrdenTrabajoView.as_view(),name='orden_trabajo'),
]