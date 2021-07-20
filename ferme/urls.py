from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('boleta/listar/', views.boleta_listar, name='boleta_listar'),
    path('boleta/anular/<id>/', views.boleta_anular, name='boleta_anular'),
    path('factura/listar/', views.factura_listar, name='factura_listar'),
    path('factura/anular/<id>/', views.factura_anular, name='factura_anular'),
    path('nota/agregar/', views.nota_agregar, name='nota_agregar'),
    path('nota/listar/', views.nota_listar, name='nota_listar'),
    path('nota/anular/<id>/', views.nota_anular, name='nota_anular'),
    path('carro/', views.carro_resumen, name='carro_resumen'),
    path('carro/agregar/', views.carro_agregar, name='carro_agregar'),
    path('carro/eliminar/', views.carro_eliminar, name='carro_eliminar'),
    path('carro/actualizar/', views.carro_actualizar, name='carro_actualizar'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_modificar, name='perfil_modificar'),
    path('compras/', views.compra_listar, name='compra_listar'),
    path('change-password/', views.change_password, name='change_password'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="ferme/usuario/password_reset.html"),
     name="reset_password"),

    path('accounts/password_reset/done/',
     auth_views.PasswordResetDoneView.as_view(template_name="ferme/usuario/password_reset_sent.html"),
     name="password_reset_done"),

    path('accounts/reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="ferme/usuario/password_reset_form.html"),
     name="password_reset_confirm"),

    path('accounts/reset/done/',
     auth_views.PasswordResetCompleteView.as_view(template_name="ferme/usuario/password_reset_done.html"),
     name="password_reset_complete"),

    # path('compra_agregar/', views.compra_agregar, name='compra_agregar'),
    path('checkout/pago_seleccion/<tipo>/', views.pago_seleccion, name='pago_seleccion'),
    path('checkout/pago_seleccion_venta/<tipo>/', views.pago_seleccion_venta, name='pago_seleccion_venta'),
    path('checkout/validar_venta/<tipo>/<compra>/', views.validar_venta, name='validar_venta'),
    path('checkout/venta_exitosa/<compra>/', views.venta_exitosa, name='venta_exitosa'),
    path('checkout/pago_completo/<tipo>/', views.pago_completo, name='pago_completo'),
    path('checkout/pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('comprobante/<compra_id>', views.comprobante_compra_view, name='comprobante_compra_view'),
    path('nota/comprobante/<nota_id>', views.comprobante_nota_view, name='comprobante_nota_view'),
    path('boleta/comprobante/<boleta_id>', views.comprobante_boleta_view, name='comprobante_boleta_view'),
    path('factura/comprobante/<factura_id>', views.comprobante_factura_view, name='comprobante_factura_view'),
    path('informe/stock/', views.informe_stock, name='informe_stock'),
    path('informe/boleta/', views.informe_boleta_ganancia, name='informe_boleta_ganancia'),
    path('informe/factura/', views.informe_factura_ganancia, name='informe_factura_ganancia'),
]