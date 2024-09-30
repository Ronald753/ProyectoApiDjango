from rest_framework import serializers
from .models import Productos  # Asegúrate de importar correctamente el modelo de productos

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['id_producto', 'id_categoria', 'nombre_producto', 'descripcion', 'precio', 'estado', 'fecha_creacion']
