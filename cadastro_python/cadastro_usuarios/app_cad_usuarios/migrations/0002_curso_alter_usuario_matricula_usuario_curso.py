# Generated by Django 5.1.7 on 2025-04-08 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cad_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_curso', models.CharField(max_length=255)),
                ('nome_professor', models.CharField(max_length=100)),
                ('sala', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='usuario',
            name='matricula',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='curso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_cad_usuarios.curso'),
        ),
    ]
