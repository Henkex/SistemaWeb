# Generated by Django 2.1.2 on 2018-10-03 20:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LineaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lp_nombre', models.CharField(max_length=30, unique=True, verbose_name='Linea')),
                ('lp_nombre_corto', models.CharField(max_length=4, unique=True, verbose_name='Nombre Corto')),
            ],
            options={
                'verbose_name': 'Linea de Producto',
                'verbose_name_plural': 'Lineas de Productos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_codigo', models.CharField(max_length=15, unique=True, verbose_name='Código')),
                ('p_nombre', models.CharField(max_length=45, unique=True, verbose_name='Nombre Producto')),
                ('p_descripcion', models.CharField(max_length=120, verbose_name='Descripción')),
                ('p_unidad_de_medida', models.CharField(choices=[('UND', 'UNIDAD'), ('JGO', 'JUEGO'), ('LTS', 'LITROS'), ('MTS', 'METROS'), ('CMS', 'CENTIMETROS')], max_length=3, verbose_name='Unidad de medida')),
                ('p_stock_minimo', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('fk_id_linea_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.LineaProducto', verbose_name='Línea de producto')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
    ]