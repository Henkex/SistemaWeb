from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Stock)
admin.site.register(Inventario)
admin.site.register(DetalleInventario)
admin.site.register(Movimiento)
admin.site.register(DetalleMovimiento)
admin.site.register(Padron)
admin.site.register(OrdenTrabajo)
admin.site.register(ParteIngreso)
admin.site.register(GuiaRemision)