from django.forms import ModelForm
from .models import Productos
#importamos las funciones de registro de usuarios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class formProductos(ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'

class createUserForm(UserCreationForm):
    error_messages = {
            'password_mismatch': '¡Las contraseñas no coinciden!'
        }
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder':'Nombre de usuario',
            }), 
            'email': forms.EmailInput(attrs={
                'placeholder':'Laura98@MiCorreo.com',
            })
        }
        error_messages = {
            'username': {
                'unique': '¡El nombre de usuario ya existe!',
            }
        }