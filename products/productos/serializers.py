from rest_framework import serializers
from .models import Productos
from products.productos_ingredientes.models import ProductosIngredientes
from products.ingredientes.models import Ingredientes

class ProductoSerializer(serializers.ModelSerializer):
    ingredientes = serializers.ListField(write_only=True)  # Acepta una lista de IDs de ingredientes

    class Meta:
        model = Productos
        fields = ['id_producto', 'id_categoria', 'nombre_producto', 'descripcion', 'precio', 'ingredientes']

    def create(self, validated_data):
        ingredientes_ids = validated_data.pop('ingredientes', [])
        producto = Productos.objects.create(**validated_data)

        for ingrediente_id in ingredientes_ids:
            try:
                ingrediente = Ingredientes.objects.get(id_ingrediente=ingrediente_id)
                ProductosIngredientes.objects.create(id_producto=producto, id_ingrediente=ingrediente)
            except Ingredientes.DoesNotExist:
                raise serializers.ValidationError(f"Ingrediente con ID {ingrediente_id} no encontrado.")

        return producto
