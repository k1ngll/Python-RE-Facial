from django import forms
from .models import Usuario
from django.db import models

#Cria o Formulário Html.
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome','email','matricula', 'curso']
        
        #Serve para estilizar os campos de texto e select no formulário.
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'curso' : forms.Select(attrs={'class': 'form-control'}),
        }