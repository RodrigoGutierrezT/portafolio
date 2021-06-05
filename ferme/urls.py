from django.urls import path
from . import views

app_name = 'ferme'

urlpatterns = [
    path('', views.producto_all, name='producto_all'),
    path('producto/agregar/', views.producto_agregar, name='producto_agregar'),
    path('producto/listar/', views.producto_listar, name='producto_listar'),
    path('producto/modificar/<id>/', views.producto_modificar, name='producto_modificar'),
    path('producto/eliminar/<id>/', views.producto_eliminar, name='producto_eliminar'),
    path('<slug:slug>', views.producto_detalle, name='producto_detalle'),
    path('orden/agregar/', views.orden_agregar, name='orden_agregar'),
    path('orden/listar/', views.orden_listar, name='orden_listar'),
    path('orden/listar/proveedor/', views.orden_listar_proveedor, name='orden_listar_proveedor'),
    path('orden/proveedor/<id>/', views.orden_consultar_proveedor, name='orden_consultar_proveedor'),
    path('orden/modificar/<id>/', views.orden_modificar, name='orden_modificar'),
    path('orden/eliminar/<id>/', views.orden_eliminar, name='orden_eliminar'),
    path('categoria/<slug:categoria_slug>', views.categoria_lista, name='categoria_lista'),
    path('orden/<id>/agregar/', views.ordendetalle_agregar, name='ordendetalle_agregar'),
    path('carro/', views.carro_resumen, name='carro_resumen'),
    path('carro/agregar/', views.carro_agregar, name='carro_agregar'),
    path('carro/eliminar/', views.carro_eliminar, name='carro_eliminar'),
    path('carro/actualizar/', views.carro_actualizar, name='carro_actualizar'),
    path('registro/', views.registro, name='registro'),
]