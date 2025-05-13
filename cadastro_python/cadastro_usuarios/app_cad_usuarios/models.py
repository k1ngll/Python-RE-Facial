from django.db import models

# Create your models here.

#Cria uma tabela no banco chamado Curso.
class Curso(models.Model):
    nome_curso = models.CharField(max_length=255)
    nome_matéria = models.CharField(max_length=80, null=True, blank=True)
    nome_professor = models.CharField(max_length=100)
    sala = models.CharField(max_length=10)

    def __str__(self):
        return self.nome_curso



#Cria a tabela Usuario no banco de dados.
class Usuario(models.Model):
    TIPO_USUARIO = [
        ('aluno', 'Aluno'),
        ('funcionario', 'Funcionário'),
    ]

    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=12, unique=True)
    curso = models.ForeignKey('Curso', on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)

    def __str__(self):
        return self.nome
