# Generated by Django 5.1.7 on 2025-05-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0008_rename_curso_gradehoraria_curso_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gradehoraria',
            old_name='curso_id',
            new_name='curso',
        ),
        migrations.AlterField(
            model_name='gradehoraria',
            name='horario',
            field=models.CharField(max_length=5),
        ),
    ]
