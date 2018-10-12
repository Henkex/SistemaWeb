from django import forms
from .models import *

#Linea de Producto Form --------------------------------------------------------------------------------
class LineaProductoForm(forms.ModelForm):
    lp_nombre           =   forms.CharField(widget=forms.TextInput(
                                        attrs={'class':'form-control',
                                                'placeholder':'Linea',
                                                'required':True}),
                                        label="Nombre de Linea")

    lp_nombre_corto     =   forms.CharField(widget=forms.TextInput(
                                        attrs={'class':'form-control',
                                                'placeholder':'Nombre Corto',
                                                'required':True}),
                                        label="Linea Nombre Corto")
    class Meta:
        model   = LineaProducto
        fields  = ('lp_nombre','lp_nombre_corto')
# Producto Forms----------------------------------------------------------------------------------------
class ProductoForm(forms.ModelForm):
    p_codigo               =  forms.CharField(widget=forms.TextInput(
                                                attrs={'class':'form-control',
                                                'placeholder':'Código del producto',
                                                'required':True}),
                                                label="Código")

    p_descripcion          =    forms.CharField(widget=forms.TextInput(
                                                attrs={'class':'form-control',
                                                'placeholder':'Descripción',
                                                'required':True}),
                                                label="Nombre de producto")
    p_unidad_de_medida     =    forms.Select(attrs={'class':'form-control chosen-select',
                                                    'required':True}),

    p_stock_minimo         =    forms.DecimalField(max_digits=11,decimal_places=2,
                                                    widget=forms.NumberInput(
                                                    attrs={'class':'form-control',
                                                            'placeholder':'Stock Minimo'}),
                                                    label="Stock Minimo")

    p_precio_dolar         =   forms.DecimalField(max_digits=11,decimal_places=2,
                                                    widget=forms.NumberInput(
                                                    attrs={'class':'form-control',
                                                            'placeholder':'Valor $/.'}),
                                                    label="Valor en Dolares")
    p_precio_soles	       =    forms.DecimalField(max_digits=11,decimal_places=2,
                                                    widget=forms.NumberInput(
                                                    attrs={'class':'form-control',
                                                            'placeholder':'Valor S/.'}),
                                                    label="Valor en Soles")

    fk_id_linea_producto   =   forms.ModelChoiceField(queryset=LineaProducto.objects.all(),
                                                        empty_label="Selecciona Linea",
                                                        widget=forms.Select(
                                                        attrs={'class':'form-control chosen-select',
                                                                    'required':True}),
                                                        label="Linea de producto")
    class Meta:
        model = Producto
        fields  = ('__all__')
