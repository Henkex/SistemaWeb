from django import forms
from django.forms.models import inlineformset_factory, formset_factory

from .models import *
#Inventario Forms  ---------------------------------------------------------------------------------------
class InventarioForm(forms.ModelForm):
	inv_observaciones		=	forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                           'placeholder':'Estado',
                                                           'required':True}),
                                                    label="Estado del producto")
	class Meta:
		model 	=	Inventario
		fields 	=	('__all__')

class DetalleInventarioForm(forms.ModelForm):
	di_stock_registrado		=	forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'Cantidad',
                                                                  'required':True}),
								label="Cantidad")
	di_stock_auditado		=	forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'Cantidad',
                                                                  'required':True}),
								label="Cantidad")
	di_estado_concordancia	=	forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                           'placeholder':'Estado',
                                                           'required':True}),
                                                    label="Estado del producto")
	di_variacion_stock		=	forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'Cantidad',
                                                                  'required':True}),
								label="Cantidad")
	fk_id_inventario		=	forms.ModelChoiceField(queryset=Inventario.objects.all(),empty_label="Escoja un producto",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}))
	fk_id_stock				=	forms.ModelChoiceField(queryset=Stock.objects.all(),empty_label="Escoja un producto",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}))
	class Meta:
		model 	=	DetalleInventario
		fields 	=	('__all__')
DetalleInventarioFormSet	=	inlineformset_factory(Inventario,DetalleInventario, 
												extra=1,can_delete=False, 
												form=DetalleInventarioForm)

#Movimiento Forms  -------------------------------------------------------------------------------------
class ParteIngresoForm(forms.ModelForm):
    class Meta:
        model = ParteIngreso
        fields = ('__all__')

# class MovimientoForm(forms.ModelForm):
#   # fk_id_almacen = forms.ModelChoiceField(queryset=Almacen.objects.all(),empty_label="Seleccione el almacen",
#   #                                           widget=forms.Select(attrs={'class':'form-control chosen-select control-almacen',
#   #                                                                    'placeholder':'almacén',
#   #                                                                    'required':True}),
#   #                                           label='Almacén')
  
#   class Meta:
#     model = Movimiento
#     fields = ('fk_id_almacen',)

class DetalleMovientoForm(forms.ModelForm):
  class Meta:
    model  = DetalleMovimiento
    fields = ('__all__')
DetalleMovientoFormSet  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=1,can_delete=False,form=DetalleMovientoForm)

#Orden de trabajo Forms  ----------------------------------------------------------------------------------
class OrdenTrabajoForm(forms.ModelForm):
  ot_codigo       = forms.CharField(max_length=11,
                                    widget=forms.TextInput(attrs={'class':'form-control',
                                                                       'placeholder':'Nro Orden de trabajo',
                                                                       'required':True}),
                                    label="Nº Orden de trabajo")
  fk_id_empleado  = forms.ModelChoiceField(queryset=Empleado.objects.all(),empty_label="Escoja el Mecánico",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}),
                                            label='Empleado que realiza el servicio')
  fk_id_padron    = forms.ModelChoiceField(queryset=Padron.objects.all(),empty_label="Escoja el vehiculo",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'placeholder':'Codigo',
                                                                     'required':True}),
                                            label='Vehiculo al que se realiza el servicio')
  ot_kilometraje  = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'placeholder':'kilometraje del padron',
                                                                  'required':True}),
                                  label="Kilometraje")
  class Meta:
    model = OrdenTrabajo
    fields = ('ot_codigo','ot_kilometraje','fk_id_empleado','fk_id_padron')
    
class OTDetalleMovimientoForm(forms.ModelForm):
    fk_id_producto      = forms.ModelChoiceField(queryset=Producto.objects.filter(p_alta_estado=True),
                                            empty_label="Seleccione el producto",
                                            widget=forms.Select(attrs={'class':'form-control chosen-select control-producto',
                                                                     'placeholder':'Cantidad',

                                                                     'required':True}),
                                            label='Producto')

    dm_cant_solicitada  = forms.IntegerField(
                                      widget=forms.NumberInput(attrs={'class':'form-control',
                                                                      'placeholder':'Cantidad',
                                                                      'disabled': 'true',
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

OTDetalleMovientoFormSet  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=2,can_delete=False,form=OTDetalleMovimientoForm)

#Parte de ingreso   ------------------------------------------------------------------------------------
class ParteIngresoForm(forms.ModelForm):
    class Meta:
        model = ParteIngreso
        fields = ('pi_codigo','fk_id_proveedor',)

class PIDetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = ('dm_cant_entrada','fk_id_producto',)

PIDetalleMovimientoFormset  = inlineformset_factory(Movimiento,DetalleMovimiento,extra=2,can_delete=False,form=PIDetalleMovimientoForm)

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
from django.forms import DateTimeField
class ServicioOrdenTrabajoForm(forms.ModelForm):
      ot_codigo       = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                                  'disabled': 'true',
                                                                  'required':False}),
                                          label="Código Orden de Trabajo")

      ot_fecha_pedido = DateTimeField(widget=forms.widgets.DateTimeInput(format="%d %b %Y %H:%M:%S %Z",
                                      attrs={'class':'form-control','disabled': 'true','required':False}),
                                      label="Fecha de Pedido")
                                            
      fk_id_usuario   = forms.ModelChoiceField(queryset=Usuario.objects.all(),
                                              widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'disabled': 'true',
                                                                     'required':False}),
                                          label='Autorizado por: ')

      fk_id_empleado  = forms.ModelChoiceField(queryset=Empleado.objects.all(),
                                              widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'disabled': 'true',
                                                                     'required':False}),
                                          label='Mecánico: ')
      fk_id_padron    = forms.ModelChoiceField(queryset=Usuario.objects.all(),
                                              widget=forms.Select(attrs={'class':'form-control chosen-select',
                                                                     'disabled': 'true',
                                                                     'required':False}),
                                          label='Padrón: ')

      class Meta:
          model   = OrdenTrabajo
          fields  = ('ot_codigo','ot_fecha_pedido','fk_id_usuario','fk_id_empleado','fk_id_padron',)

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