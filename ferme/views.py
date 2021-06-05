from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.forms import inlineformset_factory
from .models import Categoria, Producto, Marca, OrdenCompra, DetalleOrden, Proveedor, Empleado
from .carro import Carro
from .forms import OrdenForm, ProductoForm, ClienteForm, OrdenModificarForm
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from .filters import ProductoFilter, OrdenFilter

# Create your views here.

#Home
def producto_all(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'ferme/home.html', {'productos': productos})


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
    orden= OrdenCompra.objects.all()
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