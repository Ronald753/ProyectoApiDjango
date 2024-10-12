# menu/serializers.py
from rest_framework import serializers
from .models import Menus, Menu_Producto
from products.productos.models import Productos

class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'

class MenuProductoSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.SerializerMethodField()
    precio_producto = serializers.SerializerMethodField()

    class Meta:
        model = Menu_Producto
        fields = ['id_menu_producto', 'fecha_creacion', 'estado', 'id_menu', 'id_producto', 'nombre_producto', 'precio_producto']

    def get_nombre_producto(self, obj):
        # Obtener el producto relacionado
        try:
            producto = Productos.objects.get(id_producto=obj.id_producto.id_producto)  # Asumiendo que id_producto es la FK
            return producto.nombre_producto
        except Productos.DoesNotExist:
            return None  # Retorna None si no se encuentra el producto
        
    def get_precio_producto(self, obj):
        try:
            producto = Productos.objects.get(id_producto=obj.id_producto.id_producto)
            return producto.precio  # Retornar el precio del producto
        except Productos.DoesNotExist:
            return None