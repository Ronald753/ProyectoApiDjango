# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categorias(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categorias'


class Cupones(models.Model):
    id_cupon = models.AutoField(primary_key=True)
    cupon = models.CharField(max_length=10)
    porcentaje_descuento = models.IntegerField()
    usos_maximos = models.IntegerField()
    usos_disponibles = models.IntegerField()
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cupones'


class DetallesPedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido')
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'detalles_pedido'


class Ingredientes(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre_ingrediente = models.CharField(max_length=100)
    descripcion_ingrediente = models.CharField(max_length=200)
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ingredientes'


class MenuProducto(models.Model):
    id_menu_producto = models.AutoField(primary_key=True)
    id_menu = models.ForeignKey('Menus', models.DO_NOTHING, db_column='id_menu')
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    fecha_creacion = models.DateTimeField()
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_producto'
        unique_together = (('id_menu', 'id_producto'),)


class Menus(models.Model):
    id_menu = models.AutoField(primary_key=True)
    tipo_menu = models.CharField(max_length=10, blank=True, null=True)
    fecha_creacion = models.DateTimeField()
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menus'


class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    fecha_pedido = models.DateTimeField()
    tipo_pedido = models.CharField(max_length=50)
    id_cupon = models.ForeignKey(Cupones, models.DO_NOTHING, db_column='id_cupon', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField()
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pedidos'


class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='id_categoria')
    nombre_producto = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'productos'


class ProductosIngredientes(models.Model):
    id_producto_ingrediente = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='id_producto')
    id_ingrediente = models.ForeignKey(Ingredientes, models.DO_NOTHING, db_column='id_ingrediente')
    fecha_creacion = models.DateTimeField()
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'productos_ingredientes'


class Sugerencias(models.Model):
    id_sugerencia = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    sugerencia = models.CharField(max_length=500)
    fecha_sugerencia = models.DateTimeField()
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sugerencias'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=300)
    apellido = models.CharField(max_length=300)
    telefono = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    contrasenia = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField()
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'usuarios'


class ValoracionProducto(models.Model):
    id_valoracion_producto = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='id_producto')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario')
    valoracion = models.IntegerField()
    comentario = models.CharField(max_length=500)
    fecha_valoracion = models.DateTimeField()
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'valoracion_producto'
