from django.db import models
from products.productos.models import Productos

class Menus(models.Model):
    id_menu = models.AutoField(primary_key=True)
    tipo_menu = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Esta línea debe existir
    estado = models.BooleanField(default=True)
    class Meta:
        db_table = 'menus'


class Menu_Producto(models.Model):
    id_menu_producto = models.AutoField(primary_key=True)
    id_menu = models.ForeignKey(Menus, on_delete=models.CASCADE, db_column='id_menu')
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, db_column='id_producto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'menu_producto'
        unique_together = ('id_menu', 'id_producto')