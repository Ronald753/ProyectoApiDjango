from rest_framework import serializers
from .models import Ingredientes

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredientes
        fields = ['id_ingrediente', 'nombre_ingrediente', 'descripcion_ingrediente', 'estado']

    def validate_nombre_ingrediente(self, value):
        if Ingredientes.objects.filter(nombre_ingrediente=value).exists():
            raise serializers.ValidationError("Ya existe un ingrediente con ese nombre.")
        return value



