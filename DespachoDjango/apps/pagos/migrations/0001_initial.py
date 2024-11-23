# Generated by Django 5.1.2 on 2024-11-04 12:30

import django.core.validators
import django.db.models.deletion
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero_venta', models.CharField(editable=False, max_length=10, unique=True, verbose_name='Número de Venta')),
                ('rut_cliente', models.CharField(blank=True, max_length=12, verbose_name='RUT Cliente')),
                ('metodo_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), ('otro', 'Otro')], default='efectivo', max_length=20, verbose_name='Método de Pago')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Subtotal')),
                ('impuestos', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Impuestos')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Total')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('completada', 'Completada'), ('cancelada', 'Cancelada')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('notas', models.TextField(blank=True, verbose_name='Notas')),
                ('fecha_venta', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Venta')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('cliente', models.ForeignKey(blank=True, limit_choices_to={'role': 'client'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='compras', to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('vendedor', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.PROTECT, related_name='ventas_realizadas', to=settings.AUTH_USER_MODEL, verbose_name='Vendedor')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'ventas',
                'ordering': ['-fecha_venta'],
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad')),
                ('precio_unitario', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Precio Unitario')),
                ('descuento', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Descuento')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10, verbose_name='Subtotal')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ventas', to='inventario.product', verbose_name='Producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.venta', verbose_name='Venta')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalles de Venta',
                'db_table': 'detalles_venta',
                'unique_together': {('venta', 'producto')},
            },
        ),
    ]