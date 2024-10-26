# Generated by Django 5.1.1 on 2024-10-17 06:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_users', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='tipo_examen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='dashboard_users.tipoexamen'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='enunciado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preguntas_relacionadas', to='dashboard_users.pregunta'),
        ),
    ]