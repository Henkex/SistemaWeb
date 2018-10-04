from django import forms
from .models import Usuario

class LoginForm(forms.ModelForm):

    username = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control '}),label= "Usuario")
    password = forms.CharField(widget= forms.PasswordInput(attrs={'class':' form-control '}),label= "Contraseña")


    class Meta:
        model = Usuario
        fields = ['username', 'password']