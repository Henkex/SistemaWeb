from django.db import models

from apps.producto.models import Producto, LineaProducto
from apps.usuario.models import Empleado, Usuario
from apps.proveedor.models import Proveedor
import datetime
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

class Stock(models.Model):
	fk_id_producto			=	models.ForeignKey(Producto, on_delete=models.CASCADE)
	stk_stock				=	models.IntegerField(blank=True, null=True)
	stk_fecha_actualizacion	=	models.DateTimeField(blank=True)

#Inventario -------------------------------------------------------------------------
	# Importamos una función para traducir al lenguaje del usuario (Funciona si USE_L10N=True en settings)
from django.utils.translation import ugettext_lazy as _

class Inventario(models.Model):
	inv_fecha_inventario	=	models.DateTimeField(auto_now=True, blank=True)
	inv_estado				=	models.BooleanField(default=True,verbose_name='Activo')
	inv_observaciones		= 	models.TextField(max_length=500, blank=True, null=True, default='Sin Comentarios')
	inv_total_ref			=	models.IntegerField(blank=True, null=True)
	inv_total_dif			=	models.IntegerField(blank=True, null=True)
	inv_confiabilidad 		=	models.FloatField(blank=True, null=True)

	# Función para llamar el nombre de Mes del Modelo Inventario
	def getMes(self):
		mes = _(self.inv_fecha_inventario.strftime('%B'))
		return mes

	def getSimpleFecha(self):
		return self.inv_fecha_inventario.strftime("%d/%m/%y")
	# Función que me permite pasar a enteros el indice de confiabilidad para mostrarlo en barras bootstrap
	def intConfiabilidad(self):
		return int(self.inv_confiabilidad)

class DetalleConfiabilidad(models.Model):
	fk_id_inventario	=	models.ForeignKey(Inventario, on_delete=models.CASCADE)
	linea 				=	models.ForeignKey(LineaProducto,on_delete=models.CASCADE)
	total_ref			=	models.IntegerField(blank=True, null=True)
	total_dif			=	models.IntegerField(blank=True, null=True)
	confiabilidad 		=	models.FloatField(blank=True, null=True)

class DetalleInventario(models.Model):
	fk_id_inventario		=	models.ForeignKey(Inventario, on_delete=models.CASCADE)
	fk_id_producto			= 	models.ForeignKey(Producto,on_delete=models.CASCADE)
	fk_id_linea		 		=	models.ForeignKey(LineaProducto,on_delete=models.CASCADE)
	di_stock_logico			=	models.IntegerField(blank=True, null=True)
	di_stock_fisico			=	models.PositiveIntegerField(blank=True, null=True,validators=[MinValueValidator(0)])
	di_variacion_stock		=	models.IntegerField(blank=True, null=True)
	di_estado_concordancia	=	models.BooleanField(default=False)

	def variacion(self):
		variacion_stock = self.di_stock_logico-self.di_stock_fisico
		return variacion_stock

	def concordancia(self):
		if self.di_variacion_stock==0:
			return True
		

#Movimientos de Stock-----------------------------------------------------------------
MOVIMIENTO_TIPO_CHOICES = (
        ('1', 'Salida por Consumo'),
        ('2', 'Salida por ajuste de Inventario'),
        ('3', 'Salida por Traspaso'),
        ('4', 'Ingreso por Compra'),
        ('5', 'Ingreso por ajuste de Inventario'),
        ('6', 'Terminado'),
    )

MOVIMIENTO_TIPO = (
		('1', 'Ingreso de Productos'),
        ('2', 'Orden de trabajo'),
        ('3', 'Guia de Remisión'),
        ('4', 'Ajuste de Inventario'),
    )

class Movimiento (models.Model):
	mov_fecha_reg		=	models.DateTimeField(null=True, blank=True)
	mov_estado			=	models.BooleanField(default=False, verbose_name='Activo')
	mov_tipo			=	models.CharField(max_length=1, choices=MOVIMIENTO_TIPO,blank=True,null=True)
	fk_id_usuario		=	models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True,null=True)
	class Meta:
		verbose_name = "Movimiento"
		verbose_name_plural = "Movimientos"

class DetalleMovimiento(models.Model):
	dm_activo			=	models.BooleanField(default=False)
	fk_id_producto		=	models.ForeignKey(Producto,on_delete=models.CASCADE)
	dm_cant_solicitada	=	models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0)])
	dm_cant_entrada		=	models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0)])
	dm_cant_salida		=	models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0)])
	dm_fecha_operacion	= 	models.DateField(null=True)
	dm_tipo				=	models.CharField(max_length=1, blank=False, choices=MOVIMIENTO_TIPO_CHOICES)
	fk_id_movimiento	=	models.ForeignKey(Movimiento,on_delete=models.CASCADE)

#Orden de trabajo --------------------------------------------------------------------
class Padron(models.Model):
    class Meta:
        verbose_name = "Padron"
        verbose_name_plural = "Padrones"

    pdn_numero		=	models.PositiveIntegerField()
    pdn_placa		=	models.CharField(max_length=10)
    pdn_estado		=	models.BooleanField(default=True)
    pdn_kilometraje	=	models.PositiveIntegerField()

    def __str__(self):
    	return str(self.pdn_numero)

ESTADO_CHOICES = (
        ('1','En Proceso'),
        ('2','Cumplido'),
        ('3','Cumplido con retraso'),
        ('4','Cancelado'),
    )

class OrdenTrabajo(models.Model):
	ot_codigo			=	models.CharField(max_length=15)
	ot_fecha_pedido		=	models.DateTimeField()
	fk_id_usuario		=	models.ForeignKey(Usuario, on_delete=models.CASCADE)
	fk_id_empleado		=	models.ForeignKey(Empleado, on_delete=models.CASCADE)
	fk_id_padron		=	models.ForeignKey(Padron, on_delete=models.CASCADE)
	ot_kilometraje		=	models.PositiveIntegerField()
	ot_estado			=	models.CharField(max_length=1,choices=ESTADO_CHOICES, default='1')
	fk_id_movimiento	=	models.ForeignKey(Movimiento, on_delete=models.CASCADE)

#Parte de ingreso ---------------------------------------------------------------------
class ParteIngreso(models.Model):
	pi_codigo			=	models.CharField(max_length=15)
	fk_id_movimiento	=	models.ForeignKey(Movimiento, on_delete=models.CASCADE)
	fk_id_proveedor		=	models.ForeignKey(Proveedor, on_delete=models.CASCADE)

#Parte de ingreso ---------------------------------------------------------------------
class GuiaRemision(models.Model):
	gr_fecha_envio		= 	models.DateField()
	gr_nro_guia_remision= 	models.CharField(max_length=15, unique=True)
	gr_nombre_courier	=	models.CharField(max_length=150)
	gr_destino			=	models.CharField(max_length=150)
	fk_id_movimiento	=	models.ForeignKey(Movimiento, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Guia de Remisión"
		verbose_name_plural = "Guias de Remisión"