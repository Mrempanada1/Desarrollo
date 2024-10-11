# Generated by Django 5.1.1 on 2024-10-06 03:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dueño',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reparacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc_problema', models.TextField()),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('fecha_estimada_fin', models.DateTimeField()),
                ('estado_reparacion', models.CharField(max_length=100)),
                ('costo_estimado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_final', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('asignacion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('direccion', models.CharField(max_length=200)),
                ('disponibilidad', models.BooleanField(default=True)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('dueño', 'Dueño'), ('trabajador', 'Trabajador'), ('administrador', 'Administrador')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('estado_pago', models.CharField(max_length=100)),
                ('reparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.reparacion')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_servicio', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duracion_estimada', models.DurationField()),
                ('garantia', models.CharField(max_length=100)),
                ('reparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.reparacion')),
            ],
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fase_proceso', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('estado_proceso', models.CharField(max_length=100)),
                ('prioridad', models.CharField(max_length=50)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('notificaciones_id_notificacion', models.IntegerField()),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=10, unique=True)),
                ('marca', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('año', models.IntegerField()),
                ('color', models.CharField(max_length=50)),
                ('kilometraje', models.IntegerField()),
                ('tipo_combustible', models.CharField(max_length=50)),
                ('fecha_ultima_revision', models.DateField()),
                ('estado_vehiculo', models.CharField(max_length=100)),
                ('dueño', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='miapp.dueño')),
            ],
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_y_hora', models.DateTimeField()),
                ('motivo', models.TextField()),
                ('estado_cita', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=200)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.vehiculo')),
            ],
        ),
    ]
