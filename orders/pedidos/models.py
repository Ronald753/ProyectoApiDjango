from django.db import models
from clients.usuarios.models import Usuarios  # Asegúrate de tener el modelo de usuarios
from products.productos.models import Productos  # Asegúrate de tener el modelo de productos
from orders.cupones.models import Cupones  # Asegúrate de tener el modelo de cupones

class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario')
    fecha_pedido = models.DateTimeField()
    tipo_pedido = models.CharField(max_length=50)
    id_cupon = models.ForeignKey(Cupones, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_cupon')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    estado_pedido = models.CharField(max_length=50, default='enviado')

    class Meta:
        db_table = 'pedidos'


class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, db_column='id_producto')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'detalles_pedido'
