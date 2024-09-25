from rest_framework import serializers
from .models import ProductosIngredientes

class ProductosIngredientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosIngredientes
        fields = ['id_producto_ingrediente', 'id_producto', 'id_ingrediente', 'estado']
