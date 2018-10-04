from django.db import models
from django.core.validators import MinLengthValidator,RegexValidator
# Create your models here.
class Proveedor(models.Model):
    ruc 			= models.CharField(max_length=11,validators=[MinLengthValidator(11)])
    razon_social	= models.CharField(max_length=150)
    rep_legal		= models.CharField(max_length=150)
    telf_regex		= RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El numero telefonico debe tener el formato: '+999999999'. hasta 12 digitos.")
    telefono	 	= models.CharField(validators=[telf_regex], max_length=12, blank=True) # validators should be a list 
    direccion 		= models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.razon_social