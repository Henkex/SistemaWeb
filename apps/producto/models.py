from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
class LineaProducto(models.Model):
	lp_nombre			=	models.CharField(unique=True, max_length=30, verbose_name="Linea")
	lp_nombre_corto		=	models.CharField(unique=True,max_length=4, verbose_name="Nombre Corto")
	def __str__(self):
		return self.lp_nombre

	def get_nombre_corto(self):
		return self.lp_nombre_corto

	def get_full_name(self):
		return self.lp_nombre

	class Meta:
		verbose_name = 'Linea de Producto'
		verbose_name_plural = 'Lineas de Productos'
# --------------------------------------------------------------------------------------------------
UNIDAD_CHOICES	=	(
        ('UND', 'UNIDAD'),
        ('JGO', 'JUEGO'),
        ('LTS', 'LITROS'),
        ('MTS', 'METROS'),
        ('CMS', 'CENTIMETROS'),
    )
class Producto(models.Model):
	p_codigo				=	models.CharField(max_length=15,unique=True, verbose_name="Código")
	p_nombre				=	models.CharField(max_length=45,unique=True, verbose_name='Nombre Producto')
	p_descripcion			=	models.CharField(max_length=120, verbose_name="Descripción")
	p_unidad_de_medida		= 	models.CharField(max_length=3, blank=False, choices=UNIDAD_CHOICES, verbose_name="Unidad de medida")
	p_stock_minimo			=	models.IntegerField(blank=True, null=True,validators=[MinValueValidator(0)])
	p_alta_estado 			=	models.BooleanField(default=False,verbose_name='Alta del producto')
	fk_id_linea_producto	=	models.ForeignKey(LineaProducto, on_delete=models.CASCADE, verbose_name="Línea de producto")
	
	def __str__(self):
		return self.p_descripcion

	def get_codigo_producto(self):
		return self.p_codigo

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
