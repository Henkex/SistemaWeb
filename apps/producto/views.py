from django.shortcuts import render
from django.views.generic import View, ListView, DeleteView, CreateView,UpdateView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from apps.usuario.views import LoginRequiredMixin

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
""" ---------------------------------------------------
    Productos
----------------------------------------------------- """
# CRUD Productos
#Linea de Producto --------------------------------------------------------------------------------
class ListaLinea(LoginRequiredMixin,ListView):
	model  			=	LineaProducto
	template_name	=	'productos/lista_linea_de_productos.html'

class CrearLinea(LoginRequiredMixin,AjaxableResponseMixin,CreateView):
	form_class		=	LineaProductoForm
	template_name	=	'productos/crear_editar_linea_de_productos.html'
	success_url		=	reverse_lazy('productos:list_linea')

class ActualizarLinea(LoginRequiredMixin,UpdateView):
	model 			= 	LineaProducto
	form_class		=	LineaProductoForm
	template_name	=	'productos/crear_editar_linea_de_productos.html'
	success_url		=	reverse_lazy('productos:list_linea')

class EliminarLinea(LoginRequiredMixin,DeleteView):
	model 			=	LineaProducto
	success_url		=	reverse_lazy('configuracion:list_empresa')
	template_name	=	'productos/borrar_linea_de_producto.html'

#Producto --------------------------------------------------------------------------------
class ListaProducto(LoginRequiredMixin,ListView):
	model  			=	Producto
	template_name	=	'productos/lista_productos.html'

class CrearProducto(LoginRequiredMixin,AjaxableResponseMixin,CreateView):
	form_class		=	ProductoForm
	template_name	=	'productos/crear_editar_producto.html'
	success_url		=	reverse_lazy('productos:list_producto')

class ActualizarProducto(LoginRequiredMixin,UpdateView):
	model 			= 	Producto
	form_class		=	ProductoForm
	template_name	=	'productos/crear_editar_producto.html'
	success_url		=	reverse_lazy('productos:list_producto')

class EliminarProducto(LoginRequiredMixin,DeleteView):
	model 			=	Producto
	success_url		=	reverse_lazy('productos:list_producto')
	template_name	=	'productos/borrar_producto.html'
