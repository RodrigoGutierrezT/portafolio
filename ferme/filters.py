import django_filters
from django_filters import CharFilter
from .models import *

class ProductoFilter(django_filters.FilterSet):
    codigo = CharFilter(field_name='cod_prod', lookup_expr='icontains')
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model = Producto
        fields = ('codigo','nombre', 'activo', 'categoria', 'marca')

class OrdenFilter(django_filters.FilterSet):

    class Meta:
        model = OrdenCompra
        fields = '__all__'
        exclude= ('productos_solicitados', 'empleado', 'fecha_recepcion', 'activo')