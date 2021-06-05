from django.contrib import admin
import re
from . import models
from .forms import ClienteAdminForm, ProveedorAdminForm,  EmpleadoAdminForm

# Register your models here.

@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre']

@admin.register(models.Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre']

@admin.register(models.Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id','cod_prod','nombre','stock_actual','stock_critico','fecha_vencimiento','activo','get_precio']
    list_editable = ['stock_actual']
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ['nombre', 'cod_prod']
    list_filter = ['categoria', 'marca', 'activo']
    list_per_page = 20
    exclude = ('cod_prod',)

    def get_precio(self, obj):
        result = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(obj.precio))
        return '$' + str(result)
    get_precio.admin_order_field  = 'precio'  #Allows column order sorting
    get_precio.short_description = 'Precio'  #Renames column head

@admin.register(models.Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(models.Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    form = ProveedorAdminForm
    list_display = ['rut','nombre','apellido_paterno','rubro','empresa','email']
    list_editable = []
    search_fields = ['rut', 'nombre','apellido_paterno']
    list_filter = ['rubro']
    exclude = ('user',)

@admin.register(models.OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id','fecha_solicitud','fecha_recepcion','empleado','proveedor','estado_orden','activo']
    list_editable = ['fecha_recepcion', 'estado_orden',]
    search_fields = ['id', 'proveedor']
    list_filter = ['estado_orden','empleado']
    exclude = ('activo','fecha_solicitud')

@admin.register(models.DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ['get_id','orden_compra','producto','cantidad']
    list_editable = []

    def get_id(self, obj):
        return obj.orden_compra.id
    get_id.admin_order_field  = 'orden_compra'  #Allows column order sorting
    get_id.short_description = 'Orden Compra ID'  #Renames column head

@admin.register(models.Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id','nombre_empresa','rut_empresa','fecha','get_total','estado']
    list_editable = ['estado']

    def get_total(self, obj):
        result = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(obj.total))
        return '$' + str(result)
    get_total.admin_order_field  = 'total'  #Allows column order sorting
    get_total.short_description = 'Total'  #Renames column head

@admin.register(models.Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ['id','rut_cliente','fecha','get_total','estado']
    list_editable = ['estado']

    def get_total(self, obj):
        result = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(obj.total))
        return '$' + str(result)
    get_total.admin_order_field  = 'total'  #Allows column order sorting
    get_total.short_description = 'Total'  #Renames column head

@admin.register(models.Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id','cliente','fecha','get_total']

    def get_total(self, obj):
        result = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(obj.total))
        return '$' + str(result)
    get_total.admin_order_field  = 'total'  #Allows column order sorting
    get_total.short_description = 'Total'  #Renames column head
    
@admin.register(models.NotaCredito)
class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = ['fecha','rut','get_total']
    list_editable = []

    def get_total(self, obj):
        result = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(obj.total_devolucion))
        return '$' + str(result)
    get_total.admin_order_field  = 'total devolución'  #Allows column order sorting
    get_total.short_description = 'Total Devolución'  #Renames column head

@admin.register(models.DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ['get_id','producto','cantidad','get_precio']
    list_editable = []

    def get_id(self, obj):
        return obj.compra.id
    get_id.admin_order_field  = 'compra'  #Allows column order sorting
    get_id.short_description = 'Compra ID'  #Renames column head

    def get_precio(self, obj):
        result = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(obj.precio))
        return '$' + str(result)
    get_precio.admin_order_field  = 'precio'  #Allows column order sorting
    get_precio.short_description = 'Precio'  #Renames column head

@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm
    list_display = ['rut','nombre','apellido_paterno','email','telefono']
    list_editable = ['telefono']
    search_fields = ['rut', 'nombre','apellido_paterno']
    exclude = ('user',)

@admin.register(models.Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    form = EmpleadoAdminForm
    list_display = ['rut','nombre','apellido_paterno','email','telefono','cargo']
    list_editable = ['telefono']
    search_fields = ['rut', 'nombre','apellido_paterno']
    list_filter = ['cargo']
    exclude = ('user',)
