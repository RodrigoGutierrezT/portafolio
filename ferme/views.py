import json
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.template.loader import get_template
from .models import (Categoria, Producto, Marca, OrdenCompra, DetalleOrden,
                     Proveedor, Empleado, Cliente, Compra, DetalleCompra, Boleta, Factura, NotaCredito)
from .carro import Carro
from .forms import (OrdenForm, ProductoForm, ClienteForm, OrdenModificarForm,
                    EmpleadoPerfilForm, ClientePerfilForm, ProveedorPerfilForm, EmpresaFacturaForm,
                    CompraBoletaForm, CompraFacturaForm, NotaForm)
from .decorators import allowed_users, is_cliente, is_empleado, is_proveedor, is_vendedor
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .filters import ProductoFilter, OrdenFilter, NotaCreditoFilter, BoletaFilter, FacturaFilter
# PayPal
from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient
# xhtml2pdf
from xhtml2pdf import pisa

# Create your views here.

#Home
def producto_all(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'ferme/home.html', {'productos': productos})


#Cambiar contraseña
@login_required(login_url='login')
def change_password(request):

    data = {
        'form': PasswordChangeForm(user=request.user)
    }

    if request.method == 'POST':
        formulario = PasswordChangeForm(data=request.POST, user=request.user)
        if formulario.is_valid():
            formulario.save()
            update_session_auth_hash(request, formulario.user)
            messages.success(request, "Contraseña actualizada correctamente!")
            return redirect(to='/')
        else:
            data["form"] = formulario
            data["mensaje"] = "Error al guardar"

    return render(request, 'ferme/usuario/change_password.html', data)

# Modificar perfil de usuario
@login_required(login_url='login')
def perfil_modificar(request):

    current_user = request.user
    form = ''
    data = {
        'form': form
    }
    cliente = ''
    empleado = ''
    proveedor = ''

    if is_cliente(current_user):
        cliente = Cliente.objects.filter(user=current_user.id).first()
        data = {
            'form': ClientePerfilForm(instance=cliente),
            'usuario': cliente
        }

    elif is_empleado(current_user):
        empleado = Empleado.objects.filter(user=current_user.id).first()
        data = {
            'form': EmpleadoPerfilForm(instance=empleado),
            'usuario': empleado
        }
    elif is_proveedor(current_user):
        proveedor = Proveedor.objects.filter(user=current_user.id).first()
        data = {
            'form': ProveedorPerfilForm(instance=proveedor),
            'usuario': proveedor
        }


    if request.method == 'POST':
        formulario = ''
        if is_cliente(current_user):
            formulario = ClientePerfilForm(data=request.POST)
            if formulario.is_valid():
                cliente.telefono = formulario.cleaned_data['telefono']
                cliente.save()
                messages.success(request, "Perfil actualizado correctamente!")
                return redirect(to="/perfil/")
        elif is_empleado(current_user):
            formulario = EmpleadoPerfilForm(data=request.POST)
            if formulario.is_valid():
                empleado.telefono = formulario.cleaned_data['telefono']
                empleado.save()
                messages.success(request, "Perfil actualizado correctamente!")
                return redirect(to="/perfil/")
        elif is_proveedor(current_user):
            formulario = ProveedorPerfilForm(data=request.POST)
            if formulario.is_valid():
                proveedor.telefono = formulario.cleaned_data['telefono']
                proveedor.save()
                messages.success(request, "Perfil actualizado correctamente!")
                return redirect(to="/perfil/")
        else:
            data["form"] = formulario
            data["mensaje"] = "Error al guardar"

    return render(request, 'ferme/usuario/perfil.html', data)


# Consular compras de usuario
@login_required(login_url='login')
@allowed_users(allowed_roles=['CLIENTE'])
def compra_listar(request):

    current_user = request.user
    compras = Compra.objects.filter(user=current_user).order_by('-fecha')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(compras, 10)
        compras= paginator.page(page)
    except:
        raise Http404


    data = {
        'entity': compras,
        'paginator': paginator,
    }

    return render(request, 'ferme/usuario/compras.html', data)




# Agregar producto
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def producto_agregar(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto agregado correctamente!")
            return redirect(to="/producto/listar/")
        else:
            data["form"] = formulario
            data["mensaje"] = "Error al guardar"

    return render(request, 'ferme/productos/agregar_producto.html', data)

# Listar producto
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def producto_listar(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)
    myFilter = ProductoFilter(request.GET, queryset=productos)
    productos = myFilter.qs

    try:
        paginator = Paginator(productos, 10)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator,
        'myFilter': myFilter
    }
    return render(request, 'ferme/productos/listar_producto.html', data)

# Modificar producto
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def producto_modificar(request, id):
    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto modificado correctamente!")
            return redirect(to="/producto/listar/")
        else:
            data["form"] = formulario
            data["mensaje"] = "Error al guardar"

    return render(request,'ferme/productos/modificar_producto.html', data)

# Eliminar producto
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def producto_eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente!")
    return redirect(to="/producto/listar/")


def producto_detalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    return render(request, 'ferme/productos/detalle.html', {'producto': producto})

# Agregar Orden
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def orden_agregar(request):
    form = OrdenForm()
    current_user = request.user
    empleado = Empleado.objects.filter(user=current_user.id).first()

    data = {
        'form':  OrdenForm()
    }

    if request.method == 'POST':
        formulario = OrdenForm(data=request.POST)
        if formulario.is_valid():
            orden = formulario.save(commit=False)
            orden.empleado = empleado
            orden.save()
            messages.success(request, "Seleccione los productos para la Orden ")
            return redirect(to="/orden/"+ str(orden.id) +"/agregar/" )
        else:
            data["form"] = formulario
            data["mensaje"] = "Error"
    
    return render(request, 'ferme/ordencompra/agregar_orden.html', data)

# Listar orden
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def orden_listar(request):
    orden= OrdenCompra.objects.all().order_by('-fecha_solicitud')
    page = request.GET.get('page', 1)
    myFilter = OrdenFilter(request.GET, queryset=orden)
    orden = myFilter.qs


    try:
        paginator = Paginator(orden, 10)
        orden = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': orden,
        'paginator': paginator,
        'myFilter': myFilter
    }
    return render(request, 'ferme/ordencompra/listar_orden.html', data)

# Modificar orden
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def orden_modificar(request, id):
    orden = get_object_or_404(OrdenCompra, id=id)

    data = {
        'form': OrdenModificarForm(instance=orden),
        'orden': orden
    }

    if request.method == 'POST':
        formulario = OrdenModificarForm(data=request.POST, instance=orden)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Orden de compra modificada correctamente!")
            return redirect(to="/orden/listar/")
        else:
            data["form"] = formulario
            data["mensaje"] = "Error al guardar"

    return render(request,'ferme/ordencompra/modificar_orden.html', data)

# Eliminar orden
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN','SUPERVISOR', 'VENDEDOR'])
def orden_eliminar(request, id):
    orden = get_object_or_404(OrdenCompra, id=id)
    orden.delete()
    messages.success(request, "Orden de compra eliminada correctamente!")
    return redirect(to="/orden/listar/")

# listar orden proveedor
@login_required(login_url='login')
@allowed_users(allowed_roles=['PROVEEDOR'])
def orden_listar_proveedor(request):
    current_user = request.user
    proveedor = Proveedor.objects.filter(user=current_user.id).first()
    orden= OrdenCompra.objects.filter(proveedor=proveedor.id)
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(orden, 10)
        orden = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': orden,
        'paginator': paginator
    }
    return render(request, 'ferme/ordencompra/listar_orden.html', data)

# consultar orden proveedor
@login_required(login_url='login')
@allowed_users(allowed_roles=['PROVEEDOR'])
def orden_consultar_proveedor(request, id):
    orden = get_object_or_404(OrdenCompra, id=id)
    if orden.proveedor.user != request.user:
        return HttpResponse('No tienes los privilegios para acceder a esta página')
    data = {
        'orden': orden
    }

    return render(request,'ferme/ordencompra/consultar_orden.html', data)

def categoria_lista(request, categoria_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    productos = Producto.objects.filter(categoria=categoria).filter(activo=True)  
    return render(request, 'ferme/productos/categoria.html', {'categoria': categoria, 'productos': productos})

#agregar productos a orden de compra
def ordendetalle_agregar(request, id):
    DetalleOrdenFormSet = inlineformset_factory(OrdenCompra, DetalleOrden, fields=('producto', 'cantidad'), extra=5)
    orden = get_object_or_404(OrdenCompra, id=id)
    formset = DetalleOrdenFormSet(instance=orden)

    if request.method == 'POST':
        formset = DetalleOrdenFormSet(request.POST, instance=orden) 
        if formset.is_valid():
            formset.save()
            messages.success(request, "Productos actualizados de forma exitosa en la orden")
            return redirect(to="/orden/modificar/"+id+"/")

    data = {
        'formset': formset
    }

    return render(request,'ferme/ordencompra/agregar_ordendetalle.html', data)


# Listar boletas
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def boleta_listar(request):
    boletas = Boleta.objects.all().order_by('-fecha')
    page = request.GET.get('page', 1)
    myFilter = BoletaFilter(request.GET, queryset=boletas)
    boletas = myFilter.qs


    try:
        paginator = Paginator(boletas, 10)
        boletas = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': boletas,
        'paginator': paginator,
        'myFilter': myFilter
    }
    return render(request, 'ferme/boleta/listar_boleta.html', data)

# Anular boleta
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def boleta_anular(request, id):
    boleta = get_object_or_404(Boleta, id=id)
    if boleta.estado == 'ANULADA':
        messages.error(request, "Esta boleta ya se encuentra anulada")
        return redirect(to="/boleta/listar/")

    boleta.estado = 'ANULADA'
    boleta.save()
    compra = boleta.compra
    
    detalles = DetalleCompra.objects.filter(compra=compra)
    for detalle in detalles:
        producto = detalle.producto
        cantidad = detalle.cantidad
        producto.stock_actual = int(producto.stock_actual) + int(cantidad)
        producto.save()

    messages.success(request, "boleta anulada exitosamente!")
    return redirect(to="/boleta/listar/")

# Listar facturas
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def factura_listar(request):
    facturas = Factura.objects.all().order_by('-fecha')
    page = request.GET.get('page', 1)
    myFilter = FacturaFilter(request.GET, queryset=facturas)
    facturas = myFilter.qs


    try:
        paginator = Paginator(facturas, 10)
        facturas = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': facturas,
        'paginator': paginator,
        'myFilter': myFilter
    }
    return render(request, 'ferme/factura/listar_factura.html', data)

# Anular factura
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def factura_anular(request, id):
    factura = get_object_or_404(Factura, id=id)
    if factura.estado == 'ANULADA':
        messages.error(request, "Esta factura ya se encuentra anulada")
        return redirect(to="/factura/listar/")

    factura.estado = 'ANULADA'
    factura.save()
    compra = factura.compra
    
    detalles = DetalleCompra.objects.filter(compra=compra)
    for detalle in detalles:
        producto = detalle.producto
        cantidad = detalle.cantidad
        producto.stock_actual = int(producto.stock_actual) + int(cantidad)
        producto.save()

    messages.success(request, "factura anulada exitosamente!")
    return redirect(to="/factura/listar/")




# Agregar Nota de crédito
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def nota_agregar(request):
    form = NotaForm()
    current_user = request.user
    empleado = Empleado.objects.filter(user=current_user.id).first()

    data = {
        'form':  NotaForm()
    }

    if request.method == 'POST':
        formulario = NotaForm(data=request.POST)
        if formulario.is_valid():
            nota = formulario.save(commit=False)
            nota.empleado = empleado
            compra = None

            if (nota.boleta): 
                print('nota de boleta')
                compra = nota.boleta.compra
                nota.total_devolucion = nota.boleta.total

            if (nota.factura):
                print('nota de factura')
                compra = nota.factura.compra
                nota.total_devolucion = nota.factura.total
    
            nota.save()
            detalles = DetalleCompra.objects.filter(compra=compra)
            for detalle in detalles:
                producto = detalle.producto
                cantidad = detalle.cantidad
                producto.stock_actual = int(producto.stock_actual) + int(cantidad)
                producto.save()
            messages.success(request, "Nota de crédito generada exitosamente!")
            return redirect(to="/nota/listar/")
        else:
            data["form"] = formulario
    
    return render(request, 'ferme/notacredito/agregar_nota.html', data)

# Listar nota de crédito
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def nota_listar(request):
    notas = NotaCredito.objects.all().order_by('-fecha')
    page = request.GET.get('page', 1)
    myFilter = NotaCreditoFilter(request.GET, queryset=notas)
    notas = myFilter.qs


    try:
        paginator = Paginator(notas, 10)
        notas = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': notas,
        'paginator': paginator,
        'myFilter': myFilter
    }
    return render(request, 'ferme/notacredito/listar_nota.html', data)

# Anular nota de crédito
@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def nota_anular(request, id):
    nota = get_object_or_404(NotaCredito, id=id)
    if nota.estado == 'ANULADA':
        messages.error(request, "Esta nota de crédito ya se encuentra anulada")
        return redirect(to="/nota/listar/")

    nota.estado = 'ANULADA'
    nota.save()
    compra = None

    if (nota.boleta): 
        compra = nota.boleta.compra

    if (nota.factura):
        compra = nota.factura.compra
    
    detalles = DetalleCompra.objects.filter(compra=compra)
    for detalle in detalles:
        producto = detalle.producto
        cantidad = detalle.cantidad
        producto.stock_actual = int(producto.stock_actual) - int(cantidad)
        producto.save()

    messages.success(request, "Nota de crédito anulada exitosamente!")
    return redirect(to="/nota/listar/")


# Registrar cliente

def registro(request):

    data = {
        'form': ClienteForm()
    }

    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente registrado correctamente! Nombre de Usuario corresponde a email y Contraseña temporal corresponde a los 6 primeros digitos del rut + 3 primeras letras del nombre")
            return redirect(to="login")
        else:
            data["form"] = formulario
            data["mensaje"] = "Error al guardar"

    return render(request, 'registration/registro.html', data)


# Carro

def carro_resumen(request):
    carro = Carro(request)
    return render(request, 'ferme/carro/resumen.html', {'carro': carro})

def carro_agregar(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('productoid'))
        producto_cantidad = int(request.POST.get('productocantidad'))
        producto = get_object_or_404(Producto, id=producto_id)
        carro.agregar(producto=producto, cantidad=producto_cantidad)

        carro_cantidad = carro.__len__()
        response = JsonResponse({'cantidad': carro_cantidad})
        
        return response

def carro_eliminar(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('productoid'))
        carro.eliminar(producto=producto_id)

        carro_cantidad = carro.__len__()
        carrototal = carro.get_total_precio()
        response = JsonResponse({'cantidad': carro_cantidad, 'subtotal': carrototal})
        
        return response

def carro_actualizar(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('productoid'))
        producto_cantidad = int(request.POST.get('productocantidad'))
        carro.actualizar(producto=producto_id, cantidad=producto_cantidad)


        carro_cantidad = carro.__len__()
        carrototal = carro.get_total_precio()
        response = JsonResponse({'cantidad': carro_cantidad, 'subtotal': carrototal})
        
        return response



# compra

@login_required
@allowed_users(allowed_roles=['CLIENTE'])
def pago_seleccion(request, tipo):

    session = request.session
    form = EmpresaFacturaForm()

    data = {
        'tipo': tipo,
        'form': EmpresaFacturaForm(),
        'empresa': {
            'nombre_empresa': '',
            'rut_empresa': '',
            'telefono': ''
        }
    }

    if request.method == 'POST':
        formulario = EmpresaFacturaForm(data=request.POST)
        if formulario.is_valid():
            nombre_empresa = formulario.cleaned_data['nombre_empresa']
            rut_empresa = formulario.cleaned_data['rut_empresa']
            telefono = formulario.cleaned_data['telefono']
            data['empresa']['nombre_empresa'] = nombre_empresa
            data['empresa']['rut_empresa'] = rut_empresa
            data['empresa']['telefono'] = telefono
            data["form"] = formulario
        else:
            data["form"] = formulario
            data["mensaje"] = "Error"

    return render(request, "ferme/checkout/pago_seleccion.html", data)


@login_required
@allowed_users(allowed_roles=['VENDEDOR'])
def pago_seleccion_venta(request, tipo):

    current_user = request.user
    vendedor = Empleado.objects.filter(user=current_user.id).first()
    
    session = request.session
    form = ''

    if(tipo == "boleta"):
        form = CompraBoletaForm()
    if(tipo == "factura"):
        form = CompraFacturaForm()

    data = {
        'tipo': tipo,
        'form': form,
        'empresa': {
            'nombre_empresa': '',
            'rut_empresa': '',
            'telefono': ''
        }
    }

    if request.method == 'POST':
        carro = Carro(request)
        if(tipo == "boleta"):
            formulario = CompraBoletaForm(data=request.POST)
            if formulario.is_valid():
                compra = formulario.save(commit = False)
                compra.total = carro.get_total_precio()
                compra.empleado = vendedor
                compra.save()
                session["rut_cliente"] = formulario.cleaned_data['rut_cliente']
                data["form"] = formulario
                return redirect(to="/checkout/validar_venta/boleta/"+str(compra.id)+"/" )
            else:
                data["form"] = formulario
                data["mensaje"] = "Error"
        
        if(tipo == "factura"):
            formulario = CompraFacturaForm(data=request.POST)
            if formulario.is_valid():
                compra = formulario.save(commit = False)
                compra.total = carro.get_total_precio_factura()
                compra.empleado = vendedor
                compra.save()
                session["nombre_empresa"] = formulario.cleaned_data['nombre_empresa']
                session["rut_empresa"] = formulario.cleaned_data['rut_empresa']
                session["telefono"] = formulario.cleaned_data['telefono']
                data["form"] = formulario
                return redirect(to="/checkout/validar_venta/factura/"+str(compra.id)+"/" )
            else:
                data["form"] = formulario
                data["mensaje"] = "Error"

    return render(request, "ferme/checkout/pago_seleccion_venta.html", data)

@login_required
@allowed_users(allowed_roles=['VENDEDOR'])
def validar_venta(request, tipo, compra):
    compra = Compra.objects.filter(id=compra).first()
    rut_cliente = ""
    nombre_empresa = ""
    rut_empresa = ""
    telefono = ""

    if(tipo == 'boleta'):
        rut_cliente = request.session["rut_cliente"]
    if(tipo == 'factura'):
        nombre_empresa = request.session["nombre_empresa"]
        rut_empresa = request.session["rut_empresa"]
        telefono = request.session["telefono"]

    data = {
        'compra': compra,
        'tipo': tipo
    }

    if request.method == 'POST':
        carro = Carro(request)
        compra.pagado = True
        compra.save()

        for item in carro:
            DetalleCompra.objects.create(compra=compra, producto=item["producto"], precio=item["precio"], cantidad=item["cantidad"])
            producto = item["producto"]
            cantidad = item["cantidad"]
            producto.stock_actual = int(producto.stock_actual) - int(cantidad)
            if (producto.stock_actual == 0):
                producto.activo = False
            producto.save()

        documento = ''
        if(tipo == 'boleta'):
            documento = Boleta.objects.create(
                rut_cliente=rut_cliente,
                total=compra.total,
                compra=compra,
            )
        
        if(tipo == 'factura'):
            documento = Factura.objects.create(
                nombre_empresa = nombre_empresa,
                rut_empresa = rut_empresa,
                telefono = telefono,
                total = compra.total,
                compra = compra,
            )
        
        return JsonResponse('Pago Exitoso', safe=False)
    
    if request.method == 'DELETE':
        compra.delete()
        return JsonResponse('Venta cancelada exitosamente', safe=False)


    return render(request, "ferme/checkout/validar_venta.html", data)


@login_required
@allowed_users(allowed_roles=['VENDEDOR'])
def venta_exitosa(request, compra):
    carro = Carro(request)
    carro.clear()

    data = {
        'compra': compra
    }

    return render(request, "ferme/checkout/venta_exitosa.html", data)


@login_required
def pago_completo(request, tipo):
    PPClient = PayPalClient()

    body =  json.loads(request.body)
    data = body["orderID"]
    nombre_empresa = body["nombre_empresa"]
    rut_empresa = body["rut_empresa"]
    telefono = body["telefono"]
    user_id = request.user.id
    cliente = None
    if is_cliente(request.user):
        cliente = Cliente.objects.filter(user=user_id).first()

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder) 

    total_pagado = response.result.purchase_units[0].amount.value
    
    carro = Carro(request)
    compra = Compra.objects.create(
        user_id=user_id,
        nombre=cliente.nombre,
        apellido_paterno=cliente.apellido_paterno,
        email=cliente.email,
        total=int(float(response.result.purchase_units[0].amount.value)),
        order_key=response.result.id,
        medio_pago="PayPal",
        pagado=True,
    )

    for item in carro:
        DetalleCompra.objects.create(compra=compra, producto=item["producto"], precio=item["precio"], cantidad=item["cantidad"])
        producto = item["producto"]
        cantidad = item["cantidad"]
        producto.stock_actual = int(producto.stock_actual) - int(cantidad)
        if (producto.stock_actual == 0):
            producto.activo = False
        producto.save()

    documento = ''
    
    if(tipo == 'boleta'):
        documento = Boleta.objects.create(
            rut_cliente=cliente.rut,
            total=compra.total,
            compra=compra,
        )
    
    if(tipo == 'factura'):
        documento = Factura.objects.create(
            nombre_empresa = nombre_empresa,
            rut_empresa = rut_empresa,
            telefono = telefono,
            total = compra.total,
            compra = compra,
        )
    
    JsonResponse({'documento_id': documento.id, 'tipo': tipo})
        
    return JsonResponse('Pago Exitoso', safe=False)

@login_required
def pago_exitoso(request):

    carro = Carro(request)
    carro.clear()
    return render(request, "ferme/checkout/pago_exitoso.html", {})


# Generar informes

# informe de stock

@login_required(login_url='login')
@allowed_users(allowed_roles=['VENDEDOR', 'SUPERVISOR' ,'ADMIN'])
def informe_stock(request):
    productos = Producto.objects.all().order_by('-stock_actual')

    data = {
        'productos': productos
    }

    return render(request, "ferme/informe/informe_stock.html", data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def informe_boleta_ganancia(request):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio']
    totales = []

    for i in range(1, 8):
        total_mes = Boleta.objects.filter(fecha__year='2021',fecha__month=i,estado='GENERADA').aggregate(Sum('total'))
        if total_mes['total__sum'] == None:
           totales.append(0)
           continue 
        totales.append(total_mes['total__sum'])

    data = {
        'meses': meses,
        'totales': totales
    }

    return render(request, "ferme/informe/informe_boleta_ganancia.html", data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['ADMIN'])
def informe_factura_ganancia(request):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio']
    totales = []

    for i in range(1, 8):
        total_mes = Factura.objects.filter(fecha__year='2021',fecha__month=i,estado='GENERADA').aggregate(Sum('total'))
        if total_mes['total__sum'] == None:
           totales.append(0)
           continue 
        totales.append(total_mes['total__sum'])

    data = {
        'meses': meses,
        'totales': totales
    }

    return render(request, "ferme/informe/informe_factura_ganancia.html", data)


# generar pdfs

@login_required
@allowed_users(allowed_roles=['VENDEDOR','CLIENTE'])
def comprobante_compra_view(request, compra_id):
    compra = Compra.objects.filter(id = compra_id).first()
    boleta = None
    factura = None
    iva = ""

    boleta = Boleta.objects.filter(compra = compra).first()
    factura = Factura.objects.filter(compra = compra).first()

    detalles = DetalleCompra.objects.filter(compra = compra)

    if factura:
        iva = str(round((factura.total * 19) / 81))

    template_path = 'ferme/comprobante/pdf1.html'
    context = {
        'compra': compra,
        'boleta': boleta,
        'factura': factura,
        'detalles': detalles,
        'iva': iva
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="comprobante.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
@allowed_users(allowed_roles=['ADMIN'])
def comprobante_nota_view(request, nota_id):
    nota = NotaCredito.objects.filter(id = nota_id).first()
    boleta = None
    factura = None
    compra = None
    iva = ""

    boleta = nota.boleta
    factura = nota.factura

    if boleta:
        compra = boleta.compra

    if factura:
        compra = factura.compra
        iva = str(round((factura.total * 19) / 81))

    detalles = DetalleCompra.objects.filter(compra = compra)
    
    template_path = 'ferme/comprobante/pdf2.html'
    context = {
        'compra': compra,
        'boleta': boleta,
        'factura': factura,
        'detalles': detalles,
        'nota': nota,
        'iva': iva
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="comprobante.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
@allowed_users(allowed_roles=['ADMIN'])
def comprobante_boleta_view(request, boleta_id):
    boleta= Boleta.objects.filter(id = boleta_id).first()
    compra = boleta.compra

    detalles = DetalleCompra.objects.filter(compra = compra)
    
    template_path = 'ferme/comprobante/pdf3.html'
    context = {
        'compra': compra,
        'boleta': boleta,
        'detalles': detalles
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="comprobante.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
@allowed_users(allowed_roles=['ADMIN'])
def comprobante_factura_view(request, factura_id):
    factura = Factura.objects.filter(id = factura_id).first()
    compra = factura.compra

    detalles = DetalleCompra.objects.filter(compra = compra)
    iva = str(round((factura.total * 19) / 81))
    
    template_path = 'ferme/comprobante/pdf4.html'
    context = {
        'compra': compra,
        'factura': factura,
        'detalles': detalles,
        'iva': iva
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    response['Content-Disposition'] = 'filename="comprobante.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

