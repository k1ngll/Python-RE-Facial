# Generated by Django 5.1.7 on 2025-05-27 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0007_alter_gradehoraria_disciplina_delete_disciplina'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gradehoraria',
            old_name='curso',
            new_name='curso_id',
        ),
    ]
