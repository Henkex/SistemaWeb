from django.shortcuts import render

# Create your views here.
from django.views.generic import View, ListView, DeleteView, CreateView,UpdateView
from .models import *
from apps.producto.models import LineaProducto
from .forms import *
from django.urls import reverse_lazy

from django.shortcuts import render, HttpResponseRedirect , redirect, HttpResponse, get_object_or_404
from apps.usuario.views import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, Sum,Case,When
class InventarioAdmin(LoginRequiredMixin,View):
	template_name = 'almacen/index.html'
	def get(self,request):
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
			movimiento.mov_tipo			= '1'
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
		formset  		= GRDetalleMovimientoFormset
		return render(request,self.template_name,locals())

	def post(self,request):
		guia_form		= GuiaRemisionForm(request.POST)
		# formset  		= GRDetalleMovimientoFormset(request.POST,prefix='formset')
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
		# llamo al objeto OrdenTrabajo por id de la url y uso  los datos para los
		# Datos del encabezado de la orden de trabajo
		servicio_orden 		= 	get_object_or_404(OrdenTrabajo,pk=self.kwargs['pk'])
		
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
			movimiento.mov_tipo			=	'2'
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

# Inventario -------------------------------------------------------------------------------------------
class RegistroInventario(LoginRequiredMixin,View):
	template_name 	= "almacen/inventario/inventario.html"
	def get (self, request,*args,**kwargs):
		# llamo al objeto Inventario por id de la url y uso  los datos para llamarlo al template
		inventario  		= 	get_object_or_404(Inventario,pk=self.kwargs['pk'],inv_estado=True)
		# Formularios
		inventario_form		=	InventarioForm(instance=inventario)
		formset 			=	DetalleInventarioFormSet(prefix='formset',instance=inventario)
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		inventario  		= 	get_object_or_404(Inventario,pk=self.kwargs['pk'])		
		# Me aseguro de instanciar el formulario para evitar la creación de un nuevo
		inventario_form		=	InventarioForm(request.POST,instance=inventario)
		""" Ademas de instanciar el formset con el inventario debo recordar colocar {{form.id}} encima de
			del formset en el templte html (entre "for in" y el "end for" del formset)para ubicar y guardar
			los datos actualizados en el mismo registro y evitar la creación de uno nuevo
		"""
		formset_inventario 	=	DetalleInventarioGrabarFormSet(request.POST, prefix='formset',instance=inventario)
		if formset_inventario.is_valid() and inventario_form.is_valid():

			inventario_form.save()
			for ajuste in formset_inventario.save(commit=False):
				ajuste.di_variacion_stock = ajuste.di_stock_fisico-ajuste.di_stock_logico
				ajuste_inventario		  =	Movimiento()
				ajuste_inventario.mov_fecha_reg		  =	timezone.now()
				ajuste_inventario.mov_estado		  =	True
				ajuste_inventario.mov_tipo			  =	'4'
				ajuste_inventario.fk_id_usuario		  =	request.user
				ajuste_inventario.save()

				
				if ajuste.di_variacion_stock != 0:
					ajuste.di_estado_concordancia = True
					MovimientoAlmacen(ajuste.fk_id_producto, ajuste.di_variacion_stock,ajuste_inventario.id, ajuste.di_stock_fisico)
				else:
					ajuste.di_estado_concordancia = False
				ajuste.save()
			
			referencias = DetalleInventario.objects.filter(fk_id_inventario=inventario.id).count()
			diferencias	= DetalleInventario.objects.filter(fk_id_inventario=inventario.id,di_estado_concordancia=True).count()
			inventario.inv_total_dif		= diferencias
			inventario.inv_confiabilidad 	= (1-(diferencias/referencias))*100
			inventario.inv_total_ref 		= referencias
			inventario.inv_estado			= False
			inventario.save()

			confiabilidad = DetalleInventario.objects.filter(fk_id_inventario=inventario.id).values('fk_id_linea').annotate(diferencias=Count(Case(When(di_estado_concordancia=True, then=1)))).annotate(referencias=Count('*'))
			print (confiabilidad)
			
			for conf in confiabilidad:
				nuevo = DetalleConfiabilidad()
				nuevo.fk_id_inventario	= inventario
				nuevo.linea 			= LineaProducto.objects.get(id=conf['fk_id_linea']) 		
				nuevo.total_ref			= conf['referencias']
				nuevo.total_dif			= conf['diferencias']
				nuevo.confiabilidad 	= (1-(conf['diferencias']/conf['referencias']))*100
				nuevo.save()

			return redirect('/almacen/lista_inventarios/')
		# return HttpResponse("es invalido",print (form_inventario.errors))
		else:
			return render(request,self.template_name,locals())
			print (formset_inventario.errors)
			print (inventario_form.errors)

class InicioInventario(LoginRequiredMixin,View):
	template_name	= "almacen/inventario/inicio_inventario.html"
	def get(self,request):
		inventario_activo	=	Inventario.objects.filter(inv_estado=True) 
		lista_inventario	=	Inventario.objects.filter(inv_estado=False).order_by('-id')
		return render(request,self.template_name,locals())

class DetalleInventarios(LoginRequiredMixin,View):
	def get(self,request,id):
		inventario  		= 	get_object_or_404(Inventario,pk=id)
		detalle_inventario	=	DetalleInventario.objects.filter(fk_id_inventario=id)
		template_name		=	"almacen/inventario/detalle_inventario.html"
		return render(request,template_name,locals())

def CrearInventario(request):
	if request.method == 'GET':
		stock_list			=	Stock.objects.all()
		inventario  		= 	Inventario()
		inventario.save()
		
		for item in stock_list:
			detalle             	 =  DetalleInventario()
			detalle.fk_id_inventario = 	inventario
			detalle.fk_id_producto	 = 	item.fk_id_producto
			detalle.di_stock_logico  = 	item.stk_stock
			detalle.fk_id_linea		 = 	item.fk_id_producto.fk_id_linea_producto
			detalle.save()

		return redirect('/almacen/registro_inventario/'+str(inventario.id))

""" ---------------------------------------------------
    TALLER
----------------------------------------------------- """

# Orden de trabajo---------------------------------------------------------------------------------------
class OrdenTrabajoLista(LoginRequiredMixin,View):
	def get(self,request):
		object_list 	= OrdenTrabajo.objects.filter(ot_estado='1').order_by('-ot_codigo')
		template_name 	= 'taller/lista_orden_trabajo.html'
		return render(request,template_name,locals())

class OrdenTrabajoView(LoginRequiredMixin,View):
	template_name	=	'taller/orden_trabajo.html'
	def get(self,request):
		# LLamo al ultimo objeto de OrdenTrabajo creado
		if OrdenTrabajo.objects.exists():
			orden 				=	OrdenTrabajo.objects.latest('id')
			# lo almaceno en una variable y le sumo 1
			id_orden			= 	orden.id
			codigo 				= 	id_orden + 1
		else:
			# Si no existe ningun objeto OrdenTrabajo asigno un codigo inicial
			codigo 				=	1
		# codigo_orden esta formateado y listo para ser llamado en el template
		codigo_orden 		=	"ODT-"+str(codigo).zfill(7)
		# Formularios que llamo
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
			nuevo_ot 					=	ordentrabajo_form.save(commit=False)
			nuevo_ot.fk_id_movimiento	=	movimiento
			nuevo_ot.ot_fecha_pedido	=	timezone.now()
			nuevo_ot.fk_id_usuario		=	request.user
			# Grabo el formulario
			nuevo_ot.save()
			# Instancio el formulario guardado y llamo su ID para crear el codigo de OrdenTrabajo
			nuevo_ot.ot_codigo			=	"ODT-"+str(nuevo_ot.id).zfill(7)
			nuevo_ot.save()	

			detalle_pedido = OTDetalleMovientoFormSet(request.POST,prefix='formset',instance=movimiento,)
			if detalle_pedido.is_valid():
				for detalle in detalle_pedido.save(commit=False):
					detalle.fk_id_movimiento	=	movimiento
				detalle_pedido.save()
			return redirect('/taller/orden_trabajo/')
		else:
			codigo_orden 		=	request.GET.get('codigo')
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


def MovimientoAlmacen(producto_id,variacion,movimiento_id,ajuste_inv):
	stock 		=	Stock.objects.filter(fk_id_producto=producto_id)
	for item in stock:
		ajuste = DetalleMovimiento()
		if variacion<0:
			ajuste.dm_tipo 			= '2'
			ajuste.dm_cant_salida	= variacion*(-1)
		else:
			ajuste.dm_tipo 			= '5'
			ajuste.dm_cant_entrada	= variacion

		ajuste.dm_activo			=	True
		ajuste.fk_id_producto		=	producto_id
		ajuste.dm_fecha_operacion	=	timezone.now()
		ajuste.fk_id_movimiento		=	Movimiento.objects.get(id=movimiento_id)
		ajuste.save()

		item.stk_stock				 =	ajuste_inv
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

""" ---------------------------------------------------
    Funciones de filtros
----------------------------------------------------- """
def PedidosATiempo(request):
	lista = []
	items = OrdenTrabajo.objects.filter(ot_fecha_pedido="2018-10-07")
	pedidos 			= 1
	pedido_atentidos	= 1

	for p in items:
		if p.ot_estado == '2':
			pedido_atentidos += 1
		pedidos += 1
		pass
	total1	= pedido_atentidos
	total2	= pedidos
	ncp = (pedido_atentidos/pedidos)*100
	lista.append({"pedidos":total2,"Pedidos_a_tiempo":total1,"ncp":ncp})
	return HttpResponse(lista)

