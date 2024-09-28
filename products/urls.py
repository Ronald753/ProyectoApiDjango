from django.urls import path
from .categorias.views import (
    CategoriaListActiveView,
    CategoriaListDisabledView,
    CategoriaDetailView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaUpdateStateView,
)
from .productos.views import (
    ProductoListActiveView,
    ProductoListDisabledView,
    ProductoDetailView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoUpdateStateView,
)
from .ingredientes.views import (
    IngredienteListActiveView,
    IngredienteListDisabledView,
    IngredienteDetailView,
    IngredienteCreateView,
    IngredienteUpdateView,
    IngredienteUpdateStateView,
)

from .menu.views import (
    MenusListView, 
    MenusDetailView, 
    MenusUpdateView,
    MenuProductoCreateView, 
    MenuProductoDeleteView
)

urlpatterns = [
    # Rutas para Categorías
    path('categorias/actives/', CategoriaListActiveView.as_view(), name='actives_categorias'),
    path('categorias/desactives/', CategoriaListDisabledView.as_view(), name='desactives_categorias'),
    path('categorias/<int:id_categoria>/', CategoriaDetailView.as_view(), name='categoria_detail'),
    path('categorias/add/', CategoriaCreateView.as_view(), name='add_categoria'),
    path('categorias/update/<int:id_categoria>/', CategoriaUpdateView.as_view(), name='update_categoria'),
    path('categorias/update_state/<int:id_categoria>/', CategoriaUpdateStateView.as_view(), name='update_categoria_state'),

    # Rutas para Productos
    path('productos/actives/', ProductoListActiveView.as_view(), name='active_productos'),
    path('productos/desactives/', ProductoListDisabledView.as_view(), name='desactives_productos'),
    path('productos/<int:id_producto>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/add/', ProductoCreateView.as_view(), name='add_producto'),
    path('productos/update/<int:id_producto>/', ProductoUpdateView.as_view(), name='update_producto'),
    path('productos/update_state/<int:id_producto>/', ProductoUpdateStateView.as_view(), name='update_producto_state'),

    # Rutas para Ingredientes
    path('ingredientes/actives/', IngredienteListActiveView.as_view(), name='active_ingredientes'),
    path('ingredientes/desactives/', IngredienteListDisabledView.as_view(), name='desactives_ingredientes'),
    path('ingredientes/<int:id_ingrediente>/', IngredienteDetailView.as_view(), name='ingrediente_detail'),
    path('ingredientes/add/', IngredienteCreateView.as_view(), name='add_ingrediente'),
    path('ingredientes/update/<int:id_ingrediente>/', IngredienteUpdateView.as_view(), name='update_ingrediente'),
    path('ingredientes/update_state/<int:id_ingrediente>/', IngredienteUpdateStateView.as_view(), name='update_ingrediente_state'),

    # Rutas para Productos en Menús
    path('menu/menus/', MenusListView.as_view(), name='menus-list'),
    path('menu/menus/<int:id_menu>/', MenusDetailView.as_view(), name='menus-detail'),
    path('menu/menus/<int:id_menu>/update/', MenusUpdateView.as_view(), name='menus-update'),
    path('menu/menu-producto/', MenuProductoCreateView.as_view(), name='menu-producto-create'),
    path('menu/menu-producto/<int:id_menu_producto>/', MenuProductoDeleteView.as_view(), name='menu-producto-delete')
]
