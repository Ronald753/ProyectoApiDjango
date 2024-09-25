from django.db import models
from products.productos.models import Productos

class Menu(models.Model):
    tipo_menu = models.CharField(max_length=10, choices=[('almuerzo', 'Almuerzo'), ('cena', 'Cena')])
    fecha = models.DateField()
    estado = models.BooleanField(default=True)

class MenuProducto(models.Model):
    menu = models.ForeignKey(Menu, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('menu', 'producto')