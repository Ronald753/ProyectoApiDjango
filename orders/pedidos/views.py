from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.pedidos.models import Pedidos
from .serializers import PedidoSerializer, DetallePedidoSerializer, PedidoEstadoSerializer
from products.productos.models import Productos

class PedidoListView(APIView):
    def get(self, request):
        pedidos = Pedidos.objects.all()  # Obtiene todos los pedidos
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PedidoCreateView(APIView):
    def post(self, request):
        print("Datos recibidos:", request.data)

        pedido_serializer = PedidoSerializer(data=request.data)
        
        if pedido_serializer.is_valid():
            pedido = pedido_serializer.save()

            # Obtener y procesar detalles del pedido
            detalles = request.data.get('detalles', [])
            
            for detalle in detalles:
                detalle['id_pedido'] = pedido.id_pedido  # Asignar el ID del pedido recién creado
                detalle_serializer = DetallePedidoSerializer(data=detalle)
                if detalle_serializer.is_valid():
                    detalle_serializer.save()
                else:
                    print("Errores de validación:", pedido_serializer.errors)
                    return Response(detalle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(pedido_serializer.data, status=status.HTTP_201_CREATED)

        return Response(pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PedidoUpdateEstadoView(APIView):
    def put(self, request, id_pedido):
        try:
            pedido = Pedidos.objects.get(id_pedido=id_pedido)
        except Pedidos.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Usamos el serializador para validar y actualizar solo el estado_pedido
        estado_serializer = PedidoEstadoSerializer(pedido, data=request.data)

        if estado_serializer.is_valid():
            estado_serializer.save()  # Guarda los cambios
            return Response(estado_serializer.data, status=status.HTTP_200_OK)

        return Response(estado_serializer.errors, status=status.HTTP_400_BAD_REQUEST)