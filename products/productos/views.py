from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Productos
from products.ingredientes.models import Ingredientes 
from products.productos_ingredientes.models import ProductosIngredientes 
from .serializers import ProductoSerializer
from products.ingredientes.serializers import IngredienteSerializer

from django.db.models import Prefetch
from django.shortcuts import render
from products.ingredientes.models import Ingredientes
from products.productos_ingredientes.models import ProductosIngredientes

class ProductoListActiveView(APIView):
    def get(self, request):
        productos = Productos.objects.filter(estado=True).prefetch_related(
            Prefetch(
                'productosingredientes_set',  # Nombre de la relación inversa en el modelo ProductosIngredientes
                queryset=ProductosIngredientes.objects.filter(estado=True).select_related('id_ingrediente'),  # Filtrar ingredientes activos
                to_attr='ingredientes_relacionados'
            )
        )
        
        # Crear una lista de productos con los ingredientes correspondientes
        productos_data = []
        for producto in productos:
            ingredientes = [pi.id_ingrediente.nombre_ingrediente for pi in producto.ingredientes_relacionados]
            productos_data.append({
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'estado': producto.estado,
                'ingredientes': ', '.join(ingredientes)
            })
        
        return Response(productos_data, status=status.HTTP_200_OK)


class ProductoListDisabledView(APIView):
    def get(self, request):
        productos = Productos.objects.filter(estado=False).prefetch_related(
            Prefetch(
                'productosingredientes_set',  # Nombre de la relación inversa en el modelo ProductosIngredientes
                queryset=ProductosIngredientes.objects.select_related('id_ingrediente'),
                to_attr='ingredientes_relacionados'
            )
        )
        
        # Crear una lista de productos con los ingredientes correspondientes
        productos_data = []
        for producto in productos:
            ingredientes = [pi.id_ingrediente.nombre_ingrediente for pi in producto.ingredientes_relacionados]
            productos_data.append({
                'id_producto': producto.id_producto,
                'nombre_producto': producto.nombre_producto,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'estado': producto.estado,
                'ingredientes': ', '.join(ingredientes)
            })
        
        return Response(productos_data, status=status.HTTP_200_OK)

class ProductoDetailView(APIView):
    def get(self, request, id_producto):
        try:
            # Obtener el producto por su ID
            producto = Productos.objects.get(pk=id_producto)
            producto_serializer = ProductoSerializer(producto)

            # Obtener los ingredientes asociados a través de la tabla intermedia
            productos_ingredientes = ProductosIngredientes.objects.filter(id_producto=producto, estado=True)
            ingredientes = [pi.id_ingrediente for pi in productos_ingredientes]  # Extraer los objetos de ingredientes

            # Serializar los ingredientes
            ingredientes_serializer = IngredienteSerializer(ingredientes, many=True)

            # Preparar los datos de respuesta
            data = {
                **producto_serializer.data,
                'ingredientes': ingredientes_serializer.data  # Añadir los ingredientes a la respuesta
            }

            return Response(data, status=status.HTTP_200_OK)
        except Productos.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)



class ProductoCreateView(APIView):
    def post(self, request):
        # Verificar que no exista otro producto con el mismo nombre
        nombre_producto = request.data.get('nombre_producto')
        if Productos.objects.filter(nombre_producto=nombre_producto).exists():
            return Response({'message': 'Ya existe un producto con ese nombre'}, status=status.HTTP_400_BAD_REQUEST)

        # Primero validamos los datos del producto
        producto_serializer = ProductoSerializer(data=request.data)
        if producto_serializer.is_valid():
            # Guardamos el producto
            producto = producto_serializer.save()

            # Ahora manejamos los ingredientes
            ingredientes_ids = request.data.get('ingredientes', [])  # Esperamos una lista de IDs de ingredientes
            for id_ingrediente in ingredientes_ids:
                try:
                    ingrediente = Ingredientes.objects.get(pk=id_ingrediente)
                    ProductosIngredientes.objects.create(id_producto=producto, id_ingrediente=ingrediente)
                except Ingredientes.DoesNotExist:
                    return Response({'message': f'Ingrediente con id {id_ingrediente} no existe'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(producto_serializer.data, status=status.HTTP_201_CREATED)

        return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoUpdateView(APIView):
    def put(self, request, id_producto):
        try:
            # Obtener el producto
            producto = Productos.objects.get(pk=id_producto)

            # Verificar que no exista otro producto con el mismo nombre
            nombre_producto = request.data.get('nombre_producto')
            if Productos.objects.filter(nombre_producto=nombre_producto).exclude(pk=id_producto).exists():
                return Response({'message': 'Ya existe un producto con ese nombre'}, status=status.HTTP_400_BAD_REQUEST)

            producto_serializer = ProductoSerializer(producto, data=request.data)

            if producto_serializer.is_valid():
                producto_serializer.save()

                # Obtener los nuevos ingredientes enviados en la solicitud
                nuevos_ingredientes_ids = request.data.get('ingredientes', [])

                # Desactivar los ingredientes antiguos que no estén en la nueva lista
                ProductosIngredientes.objects.filter(id_producto=producto).exclude(id_ingrediente__in=nuevos_ingredientes_ids).update(estado=False)

                # Añadir o reactivar los nuevos ingredientes
                for id_ingrediente in nuevos_ingredientes_ids:
                    ProductosIngredientes.objects.update_or_create(
                        id_producto=producto,
                        id_ingrediente_id=id_ingrediente,
                        defaults={'estado': True}  # Reactivar si estaba desactivado
                    )

                return Response(producto_serializer.data, status=status.HTTP_200_OK)

            return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Productos.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ProductoUpdateStateView(APIView):
    def put(self, request, id_producto):
        try:
            producto = Productos.objects.get(pk=id_producto)
            estado = request.data.get('estado')
            if isinstance(estado, bool):
                producto.estado = estado
                producto.save()
                return Response({'message': 'Estado del producto actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response({'message': 'Valor de estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        except Productos.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
