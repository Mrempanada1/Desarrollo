# Generated by Django 5.1.1 on 2024-10-13 19:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Aceptada', 'Aceptada'), ('Rechazada', 'Rechazada')], default='Pendiente', max_length=10)),
                ('total_estimado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('monto_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_servicio', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duracion_estimada', models.IntegerField()),
                ('garantia', models.CharField(max_length=50)),
            ],
        ),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('dueño', 'Dueño'), ('trabajador', 'Trabajador'), ('administrador', 'Administrador')], default='Cliente', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('notificaciones', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='procesos_relacionados', to='miapp.notificacion')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('estado_pago', models.CharField(max_length=100)),
                ('proceso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.proceso')),
            ],
        ),
        migrations.AddField(
            model_name='notificacion',
            name='proceso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_proceso', to='miapp.proceso'),
        ),
        migrations.CreateModel(
            name='DetalleCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costo_servicio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='miapp.cotizacion')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id_trabajador', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.CharField(max_length=12)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('direccion', models.TextField()),
                ('disponibilidad', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=20)),
                ('asignacion', models.CharField(max_length=50)),
                ('rol', models.CharField(blank=True, max_length=50, null=True)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trabajadores', to='miapp.perfil')),
            ],
        ),
        migrations.AddField(
            model_name='proceso',
            name='trabajador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.trabajador'),
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
                ('estado_vehiculo', models.CharField(choices=[('disponible', 'Disponible'), ('en_reparacion', 'En Reparación'), ('no_disponible', 'No Disponible')], max_length=100)),
                ('dueño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.dueño')),
            ],
            options={
                'unique_together': {('patente', 'dueño')},
            },
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.vehiculo'),
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
