# Generated by Django 5.1.7 on 2025-05-26 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro_face', '0003_curso_alter_usuario_curso'),
        ('gestor', '0002_curso_gradehoraria_curso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradehoraria',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro_face.curso'),
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
    ]
