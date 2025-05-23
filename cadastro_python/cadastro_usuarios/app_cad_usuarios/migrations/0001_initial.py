# Generated by Django 5.1.7 on 2025-03-31 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('tipo', models.CharField(choices=[('aluno', 'Aluno'), ('funcionario', 'Funcionário')], max_length=15)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/')),
            ],
        ),
    ]
