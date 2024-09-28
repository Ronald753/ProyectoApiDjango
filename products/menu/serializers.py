# menu/serializers.py
from rest_framework import serializers
from .models import Menus, Menu_Producto
from products.productos.models import Productos

class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'

class MenuProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_Producto
        fields = '__all__'
