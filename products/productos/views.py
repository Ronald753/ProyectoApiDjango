from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Productos
from products.ingredientes.models import Ingredientes 
from products.productos_ingredientes.models import ProductosIngredientes 
from .serializers import ProductoSerializer

from django.db.models import Prefetch
from django.shortcuts import render
from products.ingredientes.models import Ingredientes
from products.productos_ingredientes.models import ProductosIngredientes

class ProductoListActiveView(APIView):
    def get(self, request):
        productos = Productos.objects.filter(estado=True)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductoListDisabledView(APIView):
    def get(self, request):
        productos = Productos.objects.filter(estado=False)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductoDetailView(APIView):
    def get(self, request, id_producto):
        try:
            producto = Productos.objects.get(pk=id_producto)
            serializer = ProductoSerializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Productos.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class ProductoCreateView(APIView):
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            # Guardar el producto
            producto = serializer.save()
            
            # Manejo de los ingredientes
            ingredientes_ids = request.data.get('ingredientes', [])
            for ingrediente_id in ingredientes_ids:
                try:
                    ingrediente = Ingredientes.objects.get(id_ingrediente=ingrediente_id)
                    ProductosIngredientes.objects.create(
                        id_producto=producto,
                        id_ingrediente=ingrediente
                    )
                except Ingredientes.DoesNotExist:
                    return Response(
                        {"error": f"Ingrediente con ID {ingrediente_id} no encontrado."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoUpdateView(APIView):
    def put(self, request, id_producto):
        try:
            producto = Productos.objects.get(pk=id_producto)
            serializer = ProductoSerializer(producto, data=request.data)
            
            # Verificar si el nuevo nombre ya existe, excluyendo el producto actual
            if serializer.is_valid():
                if 'nombre_producto' in serializer.validated_data:
                    nuevo_nombre = serializer.validated_data['nombre_producto']
                    if Productos.objects.exclude(pk=id_producto).filter(nombre_producto=nuevo_nombre).exists():
                        return Response({'message': 'Ya existe un producto con este nombre.'}, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


class ProductoListActiveViewIn(APIView):
    def get(self, request):
        productos = Productos.objects.filter(estado=True).prefetch_related(
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
    

class ProductoUpdateWithIngredientsView(APIView):
    def put(self, request, id_producto):
        try:
            producto = Productos.objects.get(pk=id_producto)
            serializer = ProductoSerializer(producto, data=request.data)
            
            if serializer.is_valid():
                # Guardar el producto
                serializer.save()

                # Manejo de los ingredientes
                # Limpiar los ingredientes existentes
                ProductosIngredientes.objects.filter(id_producto=producto).delete()

                ingredientes_ids = request.data.get('ingredientes', [])
                for ingrediente_id in ingredientes_ids:
                    try:
                        ingrediente = Ingredientes.objects.get(id_ingrediente=ingrediente_id)
                        ProductosIngredientes.objects.create(
                            id_producto=producto,
                            id_ingrediente=ingrediente
                        )
                    except Ingredientes.DoesNotExist:
                        return Response(
                            {"error": f"Ingrediente con ID {ingrediente_id} no encontrado."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Productos.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)