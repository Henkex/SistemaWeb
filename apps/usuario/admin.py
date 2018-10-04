from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# Register your models here.
admin.site.register(Empleado)

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Usuario.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username',)

@admin.register(Usuario)
class UserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    formfield_overrides = {models.ForeignKey: {'empty_label': None},}
    fieldsets = (
        ('Usuario',{'fields': ('username','password')}),
        ('Informacion Personal', {'fields': ('first_name',
                                             'last_name',
                                             'email',
                                             'cellphone')}),
        ('Permisos',{'fields':('is_active',
                               'is_staff',
                               'is_superuser',
                               'is_jefe_taller',
                               'is_jefe_alm',
                               'is_operario_alm',
                               'groups',
                               'user_permissions')}),
    )
    add_fieldsets = (
        ('Usuario', {
            'classes': ('wide',),
            'fields': ('username',
                       'password1',
                       'password2',)
        }),

        ('Informacion Personal', {
            'classes': ('wide',),
            'fields': ('first_name',
                       'last_name',
                       'email',
                       'cellphone',
                       )
        }))