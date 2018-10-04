from django.shortcuts import render

# Create your views here.
from django.views.generic import View, ListView, DeleteView, CreateView,UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy

from django.shortcuts import render, HttpResponseRedirect , redirect, HttpResponse, get_object_or_404
from apps.usuario.views import LoginRequiredMixin
from django.utils import timezone

class InventarioAdmin(LoginRequiredMixin,View):
	template_name = 'almacen/index.html'
	def get(self,request):
		return render(request,self.template_name,locals())

""" ---------------------------------------------------
    TALLER
----------------------------------------------------- """

# Orden de trabajo---------------------------------------------------------------------------------------
class OrdenTrabajoLista(LoginRequiredMixin,View):
	def get(self,request):
		object_list 	= OrdenTrabajo.objects.filter(ot_estado='1')
		template_name 	= 'taller/lista_orden_trabajo.html'
		return render(request,template_name,locals())

class OrdenTrabajoView(LoginRequiredMixin,View):
	template_name	=	'taller/orden_trabajo.html'
	def get(self,request):
		ordentrabajo_form	=	OrdenTrabajoForm
		formset 			=	OTDetalleMovientoFormSet(prefix='formset')
		return  render(request,self.template_name,locals())

	def post(self,request):
		ordentrabajo_form	=	OrdenTrabajoForm(request.POST)
		formset  		 	= 	OTDetalleMovientoFormSet(request.POST,prefix='formset')
		# Creo un nuevo objeto Movimiento Para la Orden de trabajo
		movimiento 			=	Movimiento()
		if ordentrabajo_form.is_valid() and formset.is_valid():
			movimiento.save()
			nuevo_ot 	=	ordentrabajo_form.save(commit=False)
			nuevo_ot.fk_id_movimiento	=	movimiento
			nuevo_ot.ot_fecha_pedido	=	timezone.now()
			nuevo_ot.fk_id_usuario		=	request.user
			nuevo_ot.save()	

			detalle_pedido = OTDetalleMovientoFormSet(request.POST,prefix='formset',instance=movimiento,)
			if detalle_pedido.is_valid():
				for detalle in detalle_pedido.save(commit=False):
					detalle.fk_id_movimiento	=	movimiento
				detalle_pedido.save()
			return redirect('/taller/orden_trabajo/')
		else:
			return render(request,self.template_name,locals())
""" ---------------------------------------------------
    Almácen
----------------------------------------------------- """
# Parte de ingreso---------------------------------------------------------------------------------------
class ParteIngresoView(LoginRequiredMixin,View):
	template_name	=	'almacen/ingresos/parte_de_ingreso.html'
	def get(self,request):
		parte_ingreso_form 	=	ParteIngresoForm
		formset 			=	PIDetalleMovimientoFormset(prefix='formset')
		return render(request,self.template_name,locals())

	def post(self,request):
		parte_ingreso_form	=	ParteIngresoForm(request.POST)
		formset  		 	= 	PIDetalleMovimientoFormset(request.POST,prefix='formset')
		# Creo un nuevo objeto Movimiento Para la Orden de trabajo
		movimiento 			=	Movimiento()
		if parte_ingreso_form.is_valid() and formset.is_valid():
			movimiento.fk_id_usuario	= request.user
			movimiento.mov_estado		= True
			movimiento.mov_fecha_reg	= timezone.now()
			movimiento.mov_tipo			= '4'
			movimiento.save()

			nuevo_ingreso					= parte_ingreso_form.save(commit=False)
			nuevo_ingreso.fk_id_movimiento	= movimiento
			nuevo_ingreso.save()

			detalle_ingreso = PIDetalleMovimientoFormset(request.POST,prefix='formset',instance=movimiento,)
			if detalle_ingreso.is_valid():
				for detalle in detalle_ingreso.save(commit=False):
					detalle.dm_activo			= True
					detalle.dm_fecha_operacion	= timezone.now()
					detalle.dm_tipo				= '4'
				detalle_ingreso.save()
				InsertarStock(movimiento.id)
				return redirect('/taller/orden_trabajo/')
		else:
			return render(request,self.template_name,locals())

# Guía de remisión---------------------------------------------------------------------------------------
class GuiaRemisionView(LoginRequiredMixin,View):
	template_name	=	'almacen/salidas/guia_remision.html'

	def get(self,request):
		guia_form		= GuiaRemisionForm
		formset  		= GRDetalleMovimientoFormset(prefix='formset')
		return render(request,self.template_name,locals())

	def post(self,request):
		guia_form		= GuiaRemisionForm(request.POST)
		formset  		= GRDetalleMovimientoFormset(request.POST,prefix='formset')
		# Creo un nuevo objeto Movimiento Para la Guia de remisión
		salida 			=	Movimiento()
		if guia_form.is_valid() and formset.is_valid():
			salida.mov_fecha_reg	= timezone.now()
			salida.mov_estado		= True
			salida.mov_tipo			= '3'
			salida.fk_id_usuario	= request.user
			salida.save()

			nueva_guia					= guia_form.save(commit=False)
			nueva_guia.gr_fecha_envio	= timezone.now()
			nueva_guia.fk_id_movimiento	= salida
			nueva_guia.save()

			detalle_guia = GRDetalleMovimientoFormset(request.POST,prefix='formset',instance=salida,)
			if detalle_guia.is_valid():
				for detalle in detalle_guia.save(commit=False):
					detalle.dm_activo			= True
					detalle.dm_fecha_operacion	= timezone.now()
					detalle.dm_tipo				= '3'
					RegistrarSalida(detalle.fk_id_producto,detalle.dm_cant_salida)
				detalle_guia.save()
				return redirect('/taller/orden_trabajo/')
		else:
			return render(request,self.template_name,locals())

# Entregar Productos de Ordenes de trabajo----------------------------------------------------------------
from datetime import datetime, date, timedelta
class ServicioOrdenTrabajo(LoginRequiredMixin,View):
	template_name	=	'almacen/salidas/servicio_orden_trabajo.html'
	
	def get (self, request,*args,**kwargs):
		# llamo al objeto OrdenTrabajo por id de la url
		servicio_orden 		= 	get_object_or_404(OrdenTrabajo,pk=self.kwargs['pk'])
		ordentrabajo_form	=	ServicioOrdenTrabajoForm(instance=servicio_orden)
		# llamo al obejeto Movimiento a travez de uno de los atributos del objeto OrdenTrabajo
		movimiento 			= 	get_object_or_404(Movimiento,pk=servicio_orden.fk_id_movimiento.id)
		formset 			=	SOTDetalleMovimientoFormset(prefix='formset',instance=movimiento)
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		servicio_orden 		= 	get_object_or_404(OrdenTrabajo,pk=self.kwargs['pk'])
		movimiento 			= 	get_object_or_404(Movimiento,pk=servicio_orden.fk_id_movimiento.id)
		formset 			=	SOTDetalleMovimientoFormset(request.POST,prefix='formset',instance=movimiento)
		if formset.is_valid():
			movimiento.mov_fecha_reg	=	timezone.now()
			movimiento.mov_estado		=	True
			movimiento.mov_tipo			=	'1'
			movimiento.fk_id_usuario	=	request.user
			movimiento.save()

			fecha_pedido 	=	servicio_orden.ot_fecha_pedido
			fecha_pedido_form	=	fecha_pedido.strftime('%Y-%m-%d')
			fecha_entrega	=	movimiento.mov_fecha_reg
			fecha_entrega_form	=	fecha_entrega.strftime('%Y-%m-%d')
			salida_formset = SOTDetalleMovimientoFormset(request.POST,prefix='formset',instance=movimiento,)
			if salida_formset.is_valid():
				for salida in salida_formset.save(commit=False):
					salida.dm_activo			= True
					salida.dm_fecha_operacion	= timezone.now()
					salida.dm_tipo				= '1'
					RegistrarSalida(salida.fk_id_producto,salida.dm_cant_salida)
				salida_formset.save()

			if str(fecha_pedido_form) < str(fecha_entrega_form):
				servicio_orden.ot_estado	=	'3'
				servicio_orden.save()
				return render(request,self.template_name,locals())
			servicio_orden.ot_estado	=	'2'
			servicio_orden.save()
			return render(request,self.template_name,locals())
		return render(request,self.template_name,locals())


""" ---------------------------------------------------
    Funciones de ingreso y salidas
----------------------------------------------------- """

# Función Ingreso Stock---------------------------------------------------------------------------------------
def InsertarStock(ingreso_id):
	for p in DetalleMovimiento.objects.filter(fk_id_movimiento=ingreso_id).distinct():
		objeto=DetalleMovimiento.objects.filter(fk_id_movimiento=ingreso_id,fk_id_producto=p.fk_id_producto.id)
		dm_cant_entrada = 0
		for r in objeto:
			dm_cant_entrada = dm_cant_entrada + r.dm_cant_entrada

		updateStock = Stock.objects.filter(fk_id_producto=p.fk_id_producto.id)
		updateProd 	= Producto.objects.filter(id=p.fk_id_producto.id)
		# Inserto la cantidad ingresada al stock de almacen
		for stock in updateStock:
			stock.stk_stock 					= stock.stk_stock + dm_cant_entrada
			stock.stk_fecha_actualizacion		= timezone.now()
			stock.save()
		# si el producto no tiene un stock asignado creo un nuevo objeto stock

		if len(updateStock)==0:
			objeto	= Stock()
			objeto.fk_id_producto			= Producto.objects.get(pk=p.fk_id_producto.id)
			objeto.stk_stock				= dm_cant_entrada
			objeto.stk_fecha_actualizacion	= timezone.now()
			objeto.save()
			# Productos que se les asigna un nuevo stock se dan de alta
			pass
		for item in updateProd:
			item.p_alta_estado 		= True
			item.save()	


def RegistrarSalida(producto_id,cantidad):
	salida 	=	Stock.objects.filter(fk_id_producto=producto_id)
	for item in salida:
		item.stk_stock				 =	item.stk_stock - cantidad
		item.stk_fecha_actualizacion = 	timezone.now()
		item.save()

""" ---------------------------------------------------
    Funciones de selects dinamicos
----------------------------------------------------- """
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getStockProductos(request,producto_id):
    lista = []
    items = Stock.objects.filter(fk_id_producto=producto_id)
    for i in items:
        lista.append({"max_value":i.stk_stock},)
    return HttpResponse(json.dumps(lista),content_type='application/json')

