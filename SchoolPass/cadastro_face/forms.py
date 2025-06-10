from django import forms
from .models import Usuario
from django.db import models
import re

#Gera o formulário para a pagina de cadastro
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome','email','tipo','matricula', 'curso']
        
        #Serve para estilizar os campos de texto e select no formulário.
        widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'matricula': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+', 'title': 'Apenas números'}),
        'curso' : forms.Select(attrs={'class': 'form-control'}),
        'tipo': forms.Select(attrs={'class': 'form-control'}),
        }


    def __str__(self):
        return self.nome

    #supostamente impede o usuario de digitar uma matricula com letras
    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if not matricula.isdigit():
            raise forms.ValidationError("A matrícula deve conter apenas números.")
        if len(matricula) < 6:
            raise forms.ValidationError("A matrícula deve ter pelo menos 6 dígitos.")
        return matricula

    #verifica se o email já existe
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    #verifica se o campo de nome contem apenas letras
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome):
            raise forms.ValidationError("O nome deve conter apenas letras.")
        return nome