from django.urls import path
from orders.pedidos.views import (
    PedidoListView,
    PedidoCreateView, 
    PedidoUpdateEstadoView
)

urlpatterns = [
    path('pedidos/activepedidos/', PedidoListView.as_view(), name='pedido-list'),
    path('pedidos/', PedidoCreateView.as_view(), name='pedido-create'),
    path('pedidos/update_estado/<int:id_pedido>/', PedidoUpdateEstadoView.as_view(), name='pedido-update-estado'),
]
