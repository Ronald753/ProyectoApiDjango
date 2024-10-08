from django.db import models
from products.productos.models import Productos
from products.ingredientes.models import Ingredientes

class ProductosIngredientes(models.Model):
    id_producto_ingrediente = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, db_column='id_producto')
    id_ingrediente = models.ForeignKey(Ingredientes, on_delete=models.CASCADE, db_column='id_ingrediente')
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos_ingredientes'