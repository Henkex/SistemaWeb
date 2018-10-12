from django import forms
from django.forms.models import inlineformset_factory, formset_factory

from .models import *

""" ---------------------------------------------------
    Inventario Forms
----------------------------------------------------- """
class InventarioForm(forms.ModelForm):
	inv_observaciones		=	forms.CharField(widget=forms.Textarea(attrs={'class':'form-control-plaintex',
                                                           'placeholder':'Anotaciones del inventario',
                                                           'cols': 45, 'rows': 5}),
                                                    label="Estado del producto")
	class Meta:
		model 	=	Inventario
		fields 	=	('inv_observaciones',)
# Formulario del DetalleInventario de llamada
class DetalleInventarioForm(forms.ModelForm):
  fk_id_linea    = forms.ModelChoiceField(queryset=LineaProducto.objects.all(),
                                            widget=forms.Select(attrs={'class':'form-control-plaintext',
                                                                     'readonly':'readonly',
                                                                     'disabled' : 'disabled'
                                                                     }),)

  fk_id_producto    = forms.ModelChoiceField(queryset=Producto.objects.filter(p_alta_estado=True),
                                            widget=forms.Select(attrs={'class':'form-control-plaintext',
                                                                     'readonly':'readonly',
                                                                     'disabled' : 'disabled'
                                                                     }),)
  
  di_stock_logico		=	forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control-plaintext',
                                                                  'readonly':'readonly',
                                                                  'min': '0',
                                                                  }),)

  di_stock_fisico   = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'Cantidad',
                                                                  'required':'Ingrese los datos'}),)

  # Funciones que revisan los errores dentro del formulario
  # Validando valor positvo en di_stock_fisico
  def __init__(self, *args, **kwargs):
    super(DetalleInventarioForm, self).__init__(*args, **kwargs)
    self.fields['di_stock_fisico'].widget.attrs['min'] = 0

  # def clean_price(self):
  #   stock_fisico = self.cleaned_data['di_stock_fisico']
  #   if stock_fisico < 0:
  #     raise forms.ValidationError("Debes ingresar un numero positivo")
  #   return stock_fisico
 
  class Meta:
    model 	=	DetalleInventario
    fields 	=	('id','fk_id_linea','fk_id_producto','di_stock_logico','di_stock_fisico',)

DetalleInventarioFormSet  = inlineformset_factory(Inventario,DetalleInventario,extra=0,can_delete=False,form=DetalleInventarioForm)

# Formulario del DetalleInventario para grabar
class DetalleInventarioGrabarForm(forms.ModelForm):
  di_stock_logico   = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control-plaintext',
                                                                  'readonly':'readonly',
                                                                  'min': 0,
                                                                  }),)

  class Meta:
    model   = DetalleInventario
    fields  = ('di_stock_fisico',)
DetalleInventarioGrabarFormSet  = inlineformset_factory(Inventario,DetalleInventario,extra=0,can_delete=False,form=DetalleInventarioGrabarForm)
    
#Movimiento Forms  -------------------------------------------------------------------------------------

# class MovimientoForm(forms.ModelForm):
#   # fk_id_almacen = forms.ModelChoiceField(queryset=Almacen.objects.all(),empty_label="Seleccione el almacen",
#   #                                           widget=forms.Select(attrs={'class':'form-control chosen-select control-almacen',
#   #                                                                    'placeholder':'almacén',
#   #                                                                    'required':True}),
#   #                                           label='Almacén')
  
#   class Meta:
#     model = Movimiento
#     fields = ('fk_id_almacen',)

# class DetalleMovientoForm(forms.ModelForm):
#   class Meta:
#     model  = DetalleMovimiento
#     fields = ('__all__')
# DetalleMovientoFormSet  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=1,can_delete=False,form=DetalleMovientoForm)

#Orden de trabajo Forms  ----------------------------------------------------------------------------------
class OrdenTrabajoForm(forms.ModelForm):
 
  fk_id_empleado  = forms.ModelChoiceField(queryset=Empleado.objects.all(),empty_label="Escoja el Mecánico",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}),
                                            label='Empleado que realiza el servicio')
  fk_id_padron    = forms.ModelChoiceField(queryset=Padron.objects.all(),empty_label="Padrón",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}),
                                            label='Vehículo al que se realiza el servicio')
  ot_kilometraje  = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'kilometraje del padron',
                                                                  'required':True}),
                                  label="Kilometraje")
  class Meta:
    model = OrdenTrabajo
    fields = ('ot_kilometraje','fk_id_empleado','fk_id_padron')
    
class OTDetalleMovimientoForm(forms.ModelForm):
    fk_id_producto      = forms.ModelChoiceField(queryset=Producto.objects.filter(p_alta_estado=True),
                                            empty_label="Seleccione el producto",
                                            widget=forms.Select(attrs={'class':'form-control control-producto',
                                                                     'placeholder':'Cantidad',
                                                                     'data-live-search':'true',
                                                                     'required':True}),
                                            label='Producto')

    dm_cant_solicitada  = forms.IntegerField(
                                      widget=forms.NumberInput(attrs={'class':'form-control control-pedido',
                                                                      'placeholder':'Cantidad',
                                                                      'disabled': False,
                                                                      'required':True}),
                                      label="Cantidad solicitada")
    def clean_cantidad(self):
      dm_cant_solicitada  = self.cleaned_data.get('dm_cant_solicitada')
      if dm_cant_solicitada < 0.0:
        raise forms.ValidationError('La cantidad solicitada debe ser positiva')
      return dm_cant_solicitada

    class Meta:
      model   = DetalleMovimiento
      fields  = ('dm_cant_solicitada','fk_id_producto',)

OTDetalleMovientoFormSet  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=1,can_delete=False,form=OTDetalleMovimientoForm)

#Parte de ingreso   ------------------------------------------------------------------------------------
class ParteIngresoForm(forms.ModelForm):
  pi_codigo         = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                                'placeholder':'Código de ingreso',
                                                                'required':True}),
                                            label="Código de ingreso") 

  fk_id_proveedor   = forms.ModelChoiceField(queryset=Proveedor.objects.all(),empty_label="Seleccione Proveedor",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}),
                                            label='Proveedor')
  class Meta:
      model = ParteIngreso
      fields = ('pi_codigo','fk_id_proveedor',)


class PIDetalleMovimientoForm(forms.ModelForm):
  fk_id_producto      = forms.ModelChoiceField(queryset=Producto.objects.all(),
                                            empty_label="Seleccione el producto",
                                            widget=forms.Select(attrs={'class':'form-control control-producto',
                                                                     'placeholder':'Cantidad',
                                                                     'data-live-search':'true',
                                                                     'required':True}),
                                            label='Producto')

  dm_cant_entrada    = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control control-pedido',
                                                                      'placeholder':'Cantidad',
                                                                      'disabled': False,
                                                                      'required':True}),
                                            label="Cantidad de entrada")

  class Meta:
    model = DetalleMovimiento
    fields = ('dm_cant_entrada','fk_id_producto',)

PIDetalleMovimientoFormset  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=1,can_delete=False,form=PIDetalleMovimientoForm)

#Guía de remisión   ------------------------------------------------------------------------------------ 
class GuiaRemisionForm(forms.ModelForm):
    class Meta:
        model = GuiaRemision
        fields = ('gr_nro_guia_remision','gr_nombre_courier','gr_destino',)

class GRDetalleMovimientoForm(forms.ModelForm):
    fk_id_producto      = forms.ModelChoiceField(queryset=Producto.objects.filter(p_alta_estado=True),
                                            empty_label="Seleccione el producto",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select control-producto',
                                                                     'placeholder':'Cantidad',

                                                                     'required':True}),
                                            label='Producto')
    class Meta:
        model = DetalleMovimiento
        fields = ('dm_cant_salida','fk_id_producto',)

GRDetalleMovimientoFormset  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=2,can_delete=False,form=GRDetalleMovimientoForm)    

#Servicio Orden de trabajo   -----------------------------------------------------------------------------

class SOTDetalleMovimientoForm(forms.ModelForm):
    fk_id_producto      = forms.ModelChoiceField(queryset=Producto.objects.all(),
                                              widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     # 'disabled': 'true',
                                                                     'required':'False'}),
                                          label='Producto: ')

    dm_cant_solicitada  = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  # 'disabled': 'true',
                                                                  'required':'False'}),
                                          label="Cantidad solicitada :")

    dm_cant_salida      = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'value':'0'}),
                                          label="Cantidad entregada :")
    class Meta:
        model = DetalleMovimiento
        fields = ('fk_id_producto','dm_cant_solicitada','dm_cant_salida',)
SOTDetalleMovimientoFormset = inlineformset_factory(Movimiento,DetalleMovimiento,extra=0,can_delete=False,form=SOTDetalleMovimientoForm)  