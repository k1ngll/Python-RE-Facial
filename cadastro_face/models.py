from django.db import models
from gestor.models import Curso


# Tabela de usuários
class Usuario(models.Model):
    TIPO_USUARIO = [
        ('aluno', 'Aluno'),
        ('funcionario', 'Funcionário'),
    ]

    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='aluno')
    matricula = models.CharField(max_length=12, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
