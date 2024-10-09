from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Usuarios
from .serializers import UsuariosSerializer

# Listar usuarios activos
class UsuarioListActiveView(APIView):
    def get(self, request):
        usuarios = Usuarios.objects.filter(estado=True)
        serializer = UsuariosSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Listar usuarios desactivados
class UsuarioListDisabledView(APIView):
    def get(self, request):
        usuarios = Usuarios.objects.filter(estado=False)
        serializer = UsuariosSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Detalles de un usuario
class UsuarioDetailView(APIView):
    def get(self, request, id_usuario):
        try:
            usuario = Usuarios.objects.get(pk=id_usuario)
            serializer = UsuariosSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuarios.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class UsuarioCreateView(APIView):
    def post(self, request):
        serializer = UsuariosSerializer(data=request.data)
        
        # Verificar si el correo electrónico ya existe
        if Usuarios.objects.filter(email=request.data.get('email')).exists():
            return Response({'message': 'Este correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el número de teléfono ya existe
        if Usuarios.objects.filter(telefono=request.data.get('telefono')).exists():
            return Response({'message': 'Este número de teléfono ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Actualizar la información de un usuario con validaciones
class UsuarioUpdateView(APIView):
    def put(self, request, id_usuario):
        try:
            usuario = Usuarios.objects.get(pk=id_usuario)
            serializer = UsuariosSerializer(usuario, data=request.data)

            # Verificar si el correo electrónico ya existe para otro usuario
            if 'email' in request.data:
                email = request.data.get('email')
                if Usuarios.objects.exclude(pk=id_usuario).filter(email=email).exists():
                    return Response({'message': 'Este correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si el número de teléfono ya existe para otro usuario
            if 'telefono' in request.data:
                telefono = request.data.get('telefono')
                if Usuarios.objects.exclude(pk=id_usuario).filter(telefono=telefono).exists():
                    return Response({'message': 'Este número de teléfono ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usuarios.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Cambiar el estado de un usuario (borrado lógico)
class UsuarioUpdateStateView(APIView):
    def put(self, request, id_usuario):
        try:
            usuario = Usuarios.objects.get(pk=id_usuario)
            estado = request.data.get('estado')
            if isinstance(estado, bool):
                usuario.estado = estado
                usuario.save()
                return Response({'message': 'Estado del usuario actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response({'message': 'Valor de estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        except Usuarios.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
