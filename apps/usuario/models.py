from django.db import models

#Registro de empleado-------------------------------------------------------------------------------------
class Empleado(models.Model):
    emp_nombre		=	models.CharField(max_length=45)
    emp_apellido	=	models.CharField(max_length=45)
    def __str__(self):
    	return self.emp_nombre+' '+self.emp_apellido
#Registro de usuario--------------------------------------------------------------------------------------
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#Se crea una clase que define los campos heredados del Form de usuario por defecto de Django
class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff,
                     is_superuser, **extra_fields):
        if not email:
            raise  ValueError('El email es obligatorio')
        email   = self.normalize_email(email)
        user    = self.model(username=username, email=email, is_active=True,
                         is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,username,email,password=None,**extra_fields):
        return self._create_user(username,email,password,False,False,**extra_fields)
    def create_superuser(self,username,email,password,**extra_fields):
        return self._create_user(username,email,password,True,True,**extra_fields)
        
class Usuario(AbstractBaseUser, PermissionsMixin):
   
    cellphone   		=   models.CharField('Celular', max_length=15, blank=True, null=True)
    email       	=   models.EmailField(max_length=30)
    first_name 			=   models.CharField('Nombres', max_length=100)
    last_name   	=   models.CharField('Apellidos', max_length=100)
    username    	=   models.CharField(max_length=30, unique=True)

    is_active   	=   models.BooleanField(default=True)
    is_staff    	=   models.BooleanField(default=False)
    is_jefe_taller  =   models.BooleanField(default=False)
    is_jefe_alm   	=   models.BooleanField(default=False)
    is_operario_alm =   models.BooleanField(default=False)

    objects     =   UserManager()
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']
    def get_short_name(self):
        return self.username
        
    def get_full_name(self):
    	return self.first_name+' '+self.last_name

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'