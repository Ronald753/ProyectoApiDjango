from django.urls import path
from .usuarios.views import (
    UsuarioListActiveView, 
    UsuarioListDisabledView, 
    UsuarioDetailView, 
    UsuarioCreateView, 
    UsuarioUpdateView, 
    UsuarioUpdateStateView
)

urlpatterns = [
    path('usuarios/actives/', UsuarioListActiveView.as_view(), name='usuarios_activos'),
    path('usuarios/desactives/', UsuarioListDisabledView.as_view(), name='usuarios_desactivados'),
    path('usuarios/<int:id_usuario>/', UsuarioDetailView.as_view(), name='detalle_usuario'),
    path('usuarios/add/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('usuarios/update/<int:id_usuario>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('usuarios/update_state/<int:id_usuario>/', UsuarioUpdateStateView.as_view(), name='actualizar_estado_usuario'),
]
