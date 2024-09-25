from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Categorias
from .serializers import CategoriaSerializer

class CategoriaListActiveView(APIView):
    def get(self, request):
        categorias = Categorias.objects.filter(estado=True)
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoriaListDisabledView(APIView):
    def get(self, request):
        categorias = Categorias.objects.filter(estado=False)
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoriaDetailView(APIView):
    def get(self, request, id_categoria):
        try:
            categoria = Categorias.objects.get(pk=id_categoria)
            serializer = CategoriaSerializer(categoria)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Categorias.DoesNotExist:
            return Response({'message': 'Categoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class CategoriaCreateView(APIView):
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaUpdateView(APIView):
    def put(self, request, id_categoria):
        try:
            categoria = Categorias.objects.get(pk=id_categoria)
            serializer = CategoriaSerializer(categoria, data=request.data)
            
            # Verificar si el nuevo nombre ya existe, excluyendo la categoría actual
            if serializer.is_valid():
                if 'nombre_categoria' in serializer.validated_data:
                    nuevo_nombre = serializer.validated_data['nombre_categoria']
                    if Categorias.objects.exclude(pk=id_categoria).filter(nombre_categoria=nuevo_nombre).exists():
                        return Response({'message': 'Ya existe una categoría con este nombre.'}, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Categorias.DoesNotExist:
            return Response({'message': 'Categoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)

class CategoriaUpdateStateView(APIView):
    def put(self, request, id_categoria):
        try:
            categoria = Categorias.objects.get(pk=id_categoria)
            estado = request.data.get('estado')
            if isinstance(estado, bool):
                categoria.estado = estado
                categoria.save()
                return Response({'message': 'Estado de la categoria actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response({'message': 'Valor de estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        except Categorias.DoesNotExist:
            return Response({'message': 'Categoria no encontrada'}, status=status.HTTP_404_NOT_FOUND)
