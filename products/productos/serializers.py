from rest_framework import serializers
from .models import Productos
from products.ingredientes.serializers import IngredienteSerializer

class ProductoSerializer(serializers.ModelSerializer):
    ingredientes = IngredienteSerializer(many=True, read_only=True, source='get_ingredientes')  # Cambiar el nombre de la relación según corresponda

    class Meta:
        model = Productos
        fields = ['id_producto', 'id_categoria', 'nombre_producto', 'descripcion', 'precio', 'ingredientes']

    def validate_nombre_producto(self, value):
        if Productos.objects.filter(nombre_producto=value).exists():
            raise serializers.ValidationError("Ya existe un producto con ese nombre.")
        return value
