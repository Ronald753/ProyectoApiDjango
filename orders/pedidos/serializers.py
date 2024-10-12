from products.productos.models import Productos
from clients.usuarios.models import Usuarios
from rest_framework import serializers
from .models import Pedidos, DetallePedido

class PedidoSerializer(serializers.ModelSerializer):
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=Usuarios.objects.all())

    class Meta:
        model = Pedidos
        fields = '__all__'  # Incluimos todos los campos del pedido
    def get_id_usuario(self, obj):
        # Obtener el nombre del usuario desde la relación
        return obj.id_usuario.nombre if obj.id_usuario else None
        

class DetallePedidoSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.SerializerMethodField()
    precio_producto = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido
        fields = ['id_detalle_pedido', 'id_pedido', 'id_producto', 'cantidad', 'precio_unitario', 'subtotal', 'nombre_producto', 'precio_producto', 'fecha_creacion', 'estado']

    def get_nombre_producto(self, obj):
        try:
            producto = Productos.objects.get(id_producto=obj.id_producto.id_producto)
            return producto.nombre_producto
        except Productos.DoesNotExist:
            return None
        
    def get_precio_producto(self, obj):
        try:
            producto = Productos.objects.get(id_producto=obj.id_producto.id_producto)
            return producto.precio
        except Productos.DoesNotExist:
            return None
        
class PedidoEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = ['estado_pedido']  