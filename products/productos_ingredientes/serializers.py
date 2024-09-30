from rest_framework import serializers
from .models import ProductosIngredientes  # Asegúrate de importar correctamente el modelo intermedio

class ProductoIngredienteSerializer(serializers.ModelSerializer):
    producto = serializers.CharField(source='id_producto.nombre_producto', read_only=True)  # Mostrar el nombre del producto
    ingrediente = serializers.CharField(source='id_ingrediente.nombre_ingrediente', read_only=True)  # Mostrar el nombre del ingrediente

    class Meta:
        model = ProductosIngredientes
        fields = ['id_producto_ingrediente', 'producto', 'ingrediente', 'estado', 'fecha_creacion']
