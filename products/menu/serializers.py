from rest_framework import serializers
from .models import Menu, MenuProducto

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuProducto
        fields = '__all__'
