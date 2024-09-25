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
    ProductoListActiveViewIn,
    ProductoUpdateWithIngredientsView
)
from .ingredientes.views import (
    IngredienteListActiveView,
    IngredienteListDisabledView,
    IngredienteDetailView,
    IngredienteCreateView,
    IngredienteUpdateView,
    IngredienteUpdateStateView,
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
    path('productos/listaproductos/', ProductoListActiveViewIn.as_view(), name='ProductoListActiveViewIn_state'),
    path('productos/actualizarproductos/<int:id_producto>/', ProductoUpdateWithIngredientsView.as_view(), name='ProductoUpdateWithIngredientsView_state'),

    # Rutas para Ingredientes
    path('ingredientes/actives/', IngredienteListActiveView.as_view(), name='active_ingredientes'),
    path('ingredientes/desactives/', IngredienteListDisabledView.as_view(), name='desactives_ingredientes'),
    path('ingredientes/<int:id_ingrediente>/', IngredienteDetailView.as_view(), name='ingrediente_detail'),
    path('ingredientes/add/', IngredienteCreateView.as_view(), name='add_ingrediente'),
    path('ingredientes/update/<int:id_ingrediente>/', IngredienteUpdateView.as_view(), name='update_ingrediente'),
    path('ingredientes/update_state/<int:id_ingrediente>/', IngredienteUpdateStateView.as_view(), name='update_ingrediente_state'),
]
