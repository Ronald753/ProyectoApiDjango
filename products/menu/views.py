# menu/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Menus, Menu_Producto
from .serializers import MenusSerializer, MenuProductoSerializer

class MenusListView(APIView):
    def get(self, request):
        # Obtener todos los menús activos
        menus = Menus.objects.filter(estado=True)

        # Crear una lista para almacenar los datos de los menús con sus productos
        menus_data = []
        
        for menu in menus:
            serializer = MenusSerializer(menu)  # Serializar el menú actual

            # Obtener los productos relacionados
            productos = Menu_Producto.objects.filter(id_menu=menu, estado=True)
            productos_serializer = MenuProductoSerializer(productos, many=True)  # Serializar los productos
            
            # Combinar los datos del menú con los productos
            menu_data = {
                'menu': serializer.data,
                'productos': productos_serializer.data
            }
            menus_data.append(menu_data)  # Agregar el menú con sus productos a la lista

        return Response(menus_data, status=status.HTTP_200_OK)


class MenusDetailView(APIView):
    def get(self, request, id_menu):
        try:
            menu = Menus.objects.get(pk=id_menu)
            serializer = MenusSerializer(menu)
            # Obtener productos relacionados
            productos = Menu_Producto.objects.filter(id_menu=menu, estado=True)
            productos_serializer = MenuProductoSerializer(productos, many=True)
            data = {
                'menu': serializer.data,
                'productos': productos_serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Menus.DoesNotExist:
            return Response({'message': 'Menú no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
class MenusUpdateView(APIView):
    def put(self, request, id_menu):
        try:
            menu = Menus.objects.get(pk=id_menu)
            serializer = MenusSerializer(menu, data=request.data, partial=True)
            if serializer.is_valid():
                menu = serializer.save()

                # Obtener los IDs de productos enviados en la solicitud
                productos_ids = request.data.get('productos', [])

                # Desactivar todos los productos actuales en el menú
                Menu_Producto.objects.filter(id_menu=menu).update(estado=False)

                # Añadir o actualizar productos seleccionados
                for producto_id in productos_ids:
                    Menu_Producto.objects.update_or_create(
                        id_menu=menu,
                        id_producto_id=producto_id,
                        defaults={'estado': True}  # Asegurarse de que estén activos
                    )
                
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Menus.DoesNotExist:
            return Response({'message': 'Menú no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class MenuProductoCreateView(APIView):
    def post(self, request):
        serializer = MenuProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuProductoDeleteView(APIView):
    def delete(self, request, id_menu_producto):
        try:
            menu_producto = Menu_Producto.objects.get(pk=id_menu_producto)
            menu_producto.estado = False  # Cambiar el estado a False en lugar de eliminar
            menu_producto.save()
            return Response({'message': 'Producto eliminado del menú'}, status=status.HTTP_204_NO_CONTENT)
        except Menu_Producto.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
