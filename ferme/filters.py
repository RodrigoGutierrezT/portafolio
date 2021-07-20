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

class NotaCreditoFilter(django_filters.FilterSet):
    rut = CharFilter(field_name='rut', lookup_expr='icontains')

    class Meta:
        model = NotaCredito
        fields = ('rut', 'fecha', 'estado')

class BoletaFilter(django_filters.FilterSet):
    rut = CharFilter(field_name='rut_cliente', lookup_expr='icontains')

    class Meta:
        model = Boleta
        fields = ('rut', 'fecha', 'estado')

class FacturaFilter(django_filters.FilterSet):
    rut = CharFilter(field_name='rut_empresa', lookup_expr='icontains')
    nombre = CharFilter(field_name='nombre_empresa', lookup_expr='icontains')

    class Meta:
        model = Factura
        fields = ('rut', 'nombre' ,'fecha', 'estado')