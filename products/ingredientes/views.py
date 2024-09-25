from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ingredientes
from .serializers import IngredienteSerializer
        
class IngredienteListActiveView(APIView):
    def get(self, request):
        ingredientes = Ingredientes.objects.filter(estado=True)
        serializer = IngredienteSerializer(ingredientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class IngredienteListDisabledView(APIView):
    def get(self, request):
        ingredientes = Ingredientes.objects.filter(estado=False)
        serializer = IngredienteSerializer(ingredientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IngredienteDetailView(APIView):
    def get(self, request, id_ingrediente):
        try:
            ingrediente = Ingredientes.objects.get(pk=id_ingrediente)
            serializer = IngredienteSerializer(ingrediente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ingredientes.DoesNotExist:
            return Response({'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class IngredienteCreateView(APIView):
    def post(self, request):
        serializer = IngredienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IngredienteUpdateView(APIView):
    def put(self, request, id_ingrediente):
        try:
            ingrediente = Ingredientes.objects.get(pk=id_ingrediente)
            serializer = IngredienteSerializer(ingrediente, data=request.data)
            
            # Verificar si el nuevo nombre ya existe, excluyendo el ingrediente actual
            if serializer.is_valid():
                if 'nombre_ingrediente' in serializer.validated_data:
                    nuevo_nombre = serializer.validated_data['nombre_ingrediente']
                    if Ingredientes.objects.exclude(pk=id_ingrediente).filter(nombre_ingrediente=nuevo_nombre).exists():
                        return Response({'message': 'Ya existe un ingrediente con este nombre.'}, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ingredientes.DoesNotExist:
            return Response({'message': 'Ingrediente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class IngredienteUpdateStateView(APIView):
    def put(self, request, id_ingrediente):
        try:
            ingrediente = Ingredientes.objects.get(pk=id_ingrediente)
            estado = request.data.get('estado')
            if isinstance(estado, bool):
                ingrediente.estado = estado
                ingrediente.save()
                return Response({'message': 'Estado del ingrediente actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response({'message': 'Valor de estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        except Ingredientes.DoesNotExist:
            return Response({'message': 'Ingrediente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
