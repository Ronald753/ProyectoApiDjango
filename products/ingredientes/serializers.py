from rest_framework import serializers
from .models import Ingredientes

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredientes
        fields = ['id_ingrediente', 'nombre_ingrediente', 'descripcion_ingrediente', 'estado']

     # Validar nombre del ingrediente para evitar duplicados, excluyendo el actual
    def validate_nombre_ingrediente(self, value):
        # Acceder al ID del ingrediente actual si existe
        id_ingrediente = self.instance.id_ingrediente if self.instance else None
        
        # Comprobar si ya existe un ingrediente con este nombre, excluyendo el ingrediente actual
        if Ingredientes.objects.filter(nombre_ingrediente=value).exclude(pk=id_ingrediente).exists():
            raise serializers.ValidationError("Ya existe un ingrediente con ese nombre.")
        
        return value
