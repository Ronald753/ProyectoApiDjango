from rest_framework import serializers
from .models import Categorias

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = ['id_categoria', 'nombre_categoria', 'estado']
        
    def validate_nombre_categoria(self, value):
        if Categorias.objects.filter(nombre_categoria=value).exists():
            raise serializers.ValidationError("Ya existe una categoría con este nombre.")
        return value