from django.db import models


class Curso(models.Model):
    nome_curso = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_curso



#Tabela para armazenar a grade de horario via csv
class GradeHoraria(models.Model):
    curso= models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    disciplina = models.CharField(max_length=100)
    dia_semana = models.CharField(max_length=20)
    horario = models.CharField(max_length=5)
    sala = models.CharField(max_length=20)
    data_criacao = models.DateTimeField(auto_now_add=True)

#Tabela para registrar a entrada das pessoas pela catraca
class RegistroAcesso(models.Model):
    usuario = models.ForeignKey('cadastro_face.Usuario', on_delete=models.CASCADE)
    sala = models.CharField(max_length=20)
    horario_entrada = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) 

    def __str__(self):
        return f'{self.nome} - {self.sala}'
