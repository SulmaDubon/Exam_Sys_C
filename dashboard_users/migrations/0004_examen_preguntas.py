# Generated by Django 5.1.1 on 2024-10-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_users', '0003_pregunta_tipo_examen_alter_pregunta_enunciado'),
    ]

    operations = [
        migrations.AddField(
            model_name='examen',
            name='preguntas',
            field=models.ManyToManyField(blank=True, related_name='examenes', to='dashboard_users.pregunta', verbose_name='Preguntas del examen'),
        ),
    ]
