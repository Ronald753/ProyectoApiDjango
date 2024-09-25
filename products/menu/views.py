from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Menu, MenuProducto
from .serializers import MenuSerializer, MenuProductoSerializer

# Obtener la lista de menús con sus productos
class MenuListView(APIView):
    def get(self, request):
        menus = Menu.objects.filter(estado=True)  # Obtener solo menús activos
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Obtener un menú específico junto con sus productos
class MenuDetailView(APIView):
    def get(self, request, id_menu):
        try:
            menu = Menu.objects.get(pk=id_menu)
            serializer = MenuSerializer(menu)
            productos = MenuProducto.objects.filter(menu=menu)  # Filtrar productos por menú
            productos_serializer = MenuProductoSerializer(productos, many=True)
            return Response({
                'menu': serializer.data,
                'productos': productos_serializer.data
            }, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({'message': 'Menú no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Editar los productos de un menú específico
class MenuUpdateProductsView(APIView):
    def put(self, request, id_menu):
        try:
            menu = Menu.objects.get(pk=id_menu)
            productos_ids = request.data.get('productos_ids', [])

            # Actualizar productos del menú
            menu_productos = MenuProducto.objects.filter(menu=menu)
            menu_productos.delete() 

            for producto_id in productos_ids:
                MenuProducto.objects.create(menu=menu, producto_id=producto_id)

            return Response({'message': 'Productos del menú actualizados correctamente'}, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({'message': 'Menú no encontrado'}, status=status.HTTP_404_NOT_FOUND)
