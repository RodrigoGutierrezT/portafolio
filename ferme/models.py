from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.urls import reverse
from datetime import datetime
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name_plural = 'categorias'

    def get_absolute_url(self):
        return reverse('ferme:categoria_lista', args=[self.slug])

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name_plural = 'marcas'
    
    def get_absolute_url(self):
        return reverse('ferme:marca_lista', args=[self.slug])


    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = 'tipos'

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    rut = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    telefono = models.CharField(max_length=9)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'clientes'

    def __str__(self):
        return self.nombre + ' ' + self.apellido_paterno


class Proveedor(models.Model):
    rut = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    telefono = models.CharField(max_length=9)
    rubro = models.CharField(max_length=40)
    empresa = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'proveedores'

    def __str__(self):
        return self.nombre + ' ' + self.apellido_paterno


class Empleado(models.Model):
    cargo_opciones = (
        ('VENDEDOR', 'VENDEDOR'),
        ('SUPERVISOR', 'SUPERVISOR'),
        ('ADMIN', 'ADMIN')
    )

    rut = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    telefono = models.CharField(max_length=9)
    cargo = models.CharField(max_length=25, choices=cargo_opciones, default=cargo_opciones[0][0])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'empleados'

    def __str__(self):
        return self.nombre + ' ' + self.apellido_paterno + ' ' + str(self.cargo)


class Producto(models.Model):
    cod_prod = models.CharField(max_length=17,unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=400)
    precio = models.PositiveIntegerField()
    stock_actual = models.PositiveIntegerField()
    stock_critico = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to='images/', default='images/default.jpg')
    slug = models.SlugField(max_length=80)
    activo = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, related_name='producto_categoria', on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, related_name='producto_marca', on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, related_name='producto_proveedor', on_delete=models.PROTECT)
    tipo = models.ForeignKey(Tipo, related_name='producto_tipo', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'productos'

    def get_absolute_url(self):
        return reverse('ferme:producto_detalle', args=[self.slug])

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    estado_opciones = (
        ('GENERADA', 'GENERADA'),
        ('RECIBIDA', 'RECIBIDA'),
        ('ANULADA', 'ANULADA')
    )

    fecha_solicitud = models.DateField(default=datetime.now)
    productos_solicitados = models.TextField(max_length=400, null=True, blank=True) 
    fecha_recepcion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    estado_orden = models.CharField(max_length=15, choices=estado_opciones, default=estado_opciones[0][0])
    empleado = models.ForeignKey(Empleado, related_name='ordencompra_empleado', on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, related_name='ordencompra_proveedor', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'ordenes de compra'

    def __str__(self):
        return str(self.fecha_solicitud) + ' ' +str(self.proveedor) + ' ' + self.estado_orden


class DetalleOrden(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, related_name='detalleorden_ordencompra', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='detalleorden_producto', on_delete=models.PROTECT) 
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'detalle de ordenes'

    def __str__(self):
        return str(self.orden_compra.id) + ' ' + str(self.producto.nombre) + ' ' + str(self.cantidad)


class Factura(models.Model):
    estado_opciones = (
        ('GENERADA', 'GENERADA'),
        ('ANULADA', 'ANULADA')
    )
    fecha = models.DateField(default=datetime.now)
    nombre_empresa = models.CharField(max_length=50)
    rut_empresa = models.CharField(max_length=9)  
    telefono = models.CharField(max_length=9)
    total = models.PositiveIntegerField()
    estado = models.CharField(max_length=15, choices=estado_opciones, default=estado_opciones[0][0])

    class Meta:
        verbose_name_plural = 'facturas'

    def __str__(self):
        return str(self.id)


class Boleta(models.Model):
    estado_opciones = (
        ('GENERADA', 'GENERADA'),
        ('ANULADA', 'ANULADA')
    )
    fecha = models.DateField(default=datetime.now)
    rut_cliente = models.CharField(max_length=9)  
    total = models.PositiveIntegerField()
    estado = models.CharField(max_length=15, choices=estado_opciones, default=estado_opciones[0][0])

    class Meta:
        verbose_name_plural = 'boletas'

    def __str__(self):
        return str(self.id)


class Compra(models.Model):
    fecha = models.DateField(default=datetime.now)
    cliente = models.ForeignKey(Cliente, related_name='compra_cliente', on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, related_name='compra_empleado', on_delete=models.PROTECT, null=True, blank=True)
    total = models.PositiveIntegerField()
    boleta = models.OneToOneField(Boleta, on_delete=models.CASCADE, null=True, blank=True)
    factura = models.OneToOneField(Factura, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'compras'

    def __str__(self):
        return str(self.cliente) + ' ' + str(self.fecha) + ' ' + str(self.total)


class NotaCredito(models.Model):
    estado_opciones = (
        ('GENERADA', 'GENERADA'),
        ('ANULADA', 'ANULADA')
    )
    nombre_cliente = models.CharField(max_length=20)
    apellido_cliente = models.CharField(max_length=20)
    rut = models.CharField(max_length=9)  
    fecha = models.DateField(default=datetime.now)
    total_devolucion = models.PositiveIntegerField()
    estado = models.CharField(max_length=15, choices=estado_opciones, default=estado_opciones[0][0])
    boleta = models.OneToOneField(Boleta, on_delete=models.CASCADE, null=True, blank=True)
    factura = models.OneToOneField(Factura, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, related_name='notacredito_empleado', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'notas de credito'

    def __str__(self):
        return self.nombre_cliente + ' ' + self.apellido_cliente + ' ' + str(self.fecha) + ' ' + str(self.total_devolucion)


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='detallecompra_compra', on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, related_name='detallecompra_producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'detalle de compras'

    def __str__(self):
        return str(self.compra.id) + ' ' + str(self.producto.nombre) + ' ' + str(self.cantidad)



# eventos 

# generar codigo de producto de manera autómatica al momento  de creación
@receiver(post_save, sender=Producto)
def set_cod_producto(sender, instance, created, **kwargs):
    if created:
        producto = Producto.objects.get(pk=instance.id)
        proveedor = str(producto.proveedor.id)
        categoria = str(producto.categoria.id)
        fecha = producto.fecha_vencimiento
        tipo = str(producto.tipo.id)
        while(len(proveedor) < 3):
            proveedor = '0' + proveedor
        while(len(categoria) < 3):
            categoria = '0' + categoria
        while(len(tipo) < 3):
            tipo = '0' + tipo
        if not fecha:
            fecha = '00000000'
        else:
            fecha = str(fecha).replace("-","")
            
        producto.cod_prod = proveedor + categoria + fecha + tipo
        producto.save()

@receiver(pre_save, sender=Producto)
def crear_slug_producto(sender, instance, **kwargs):
    instance.slug = orig = slugify(instance.nombre)

# asignar empleados a su grupo correspondiente
@receiver(post_save, sender=Empleado)
def asignar_grupo_emp(sender, instance, **kwargs):
    empleado = Empleado.objects.get(pk=instance.id)
    cargo = empleado.cargo
    grupo = Group.objects.get(name=cargo)
    empleado.user.groups.set([grupo])
    if cargo == 'ADMIN':
        empleado.user.is_superuser = True
        empleado.user.is_staff = True
        empleado.user.save()
    elif cargo == 'VENDEDOR' or cargo == 'SUPERVISOR':
        empleado.user.is_superuser = False
        empleado.user.is_staff = True
        empleado.user.save()

@receiver(pre_save, sender=Empleado)
def empleado_usuario_creacion(sender, instance, **kwargs):
    empleado = Empleado.objects.filter(pk=instance.id).first()
    if empleado:
        print('empleado ya existe')
        pass
    else:
        #nombre de usario será el mail
        #la contraseña será los primeros 6 digitos del rut seguido de las primeras 3 letras del nombre
        print('usuario nuevo')
        username = instance.email
        password = (str(instance.rut))[0:6] + (str(instance.nombre))[0:3].lower() 
        first_name = instance.nombre
        instance.user = User.objects.create_user(username=username, password=password, first_name=first_name)

@receiver(post_delete, sender=Empleado)
def empleado_usuario_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

# asignar clientes a su grupo correspondiente
@receiver(post_save, sender=Cliente)
def asignar_grupo_cli(sender, instance, **kwargs):
    cliente = Cliente.objects.filter(pk=instance.id).first()
    grupo = Group.objects.get(name='CLIENTE')
    cliente.user.groups.set([grupo])
    cliente.user.save()

@receiver(pre_save, sender=Cliente)
def cliente_usuario_creacion(sender, instance, **kwargs):
    cliente = Cliente.objects.filter(pk=instance.id).first()
    if cliente:
        print('cliente ya existe')
        pass
    else:
        #nombre de usario será el mail
        #la contraseña será los primeros 6 digitos del rut seguido de las primeras 3 letras del nombre
        print('usuario nuevo')
        username = instance.email
        password = (str(instance.rut))[0:6] + (str(instance.nombre))[0:3].lower() 
        first_name = instance.nombre
        instance.user = User.objects.create_user(username=username, password=password, first_name=first_name)

@receiver(post_delete, sender=Cliente)
def cliente_usuario_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

# asignar proveedores a su grupo correspondiente
@receiver(post_save, sender=Proveedor)
def asignar_grupo_pro(sender, instance, **kwargs):
    proveedor = Proveedor.objects.get(pk=instance.id)
    grupo = Group.objects.get(name='PROVEEDOR')
    proveedor.user.groups.set([grupo])
    proveedor.user.save()

@receiver(pre_save, sender=Proveedor)
def proveedor_usuario_creacion(sender, instance, **kwargs):
    proveedor = Proveedor.objects.filter(pk=instance.id).first()
    if proveedor:
        print('proveedor ya existe')
        pass
    else:
        #nombre de usario será el mail
        #la contraseña será los primeros 6 digitos del rut seguido de las primeras 3 letras del nombre
        print('usuario nuevo')
        username = instance.email
        password = (str(instance.rut))[0:6] + (str(instance.nombre))[0:3].lower() 
        first_name = instance.nombre
        instance.user = User.objects.create_user(username=username, password=password, first_name=first_name)

@receiver(post_delete, sender=Proveedor)
def empleado_usuario_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

# rellenar descripción de orden de compra en base a detalle de orden
@receiver(post_save, sender=DetalleOrden)
def desc_orden_crear(sender, instance, **kwargs):
    orden = OrdenCompra.objects.get(pk=instance.orden_compra.id)
    detalles = DetalleOrden.objects.filter(orden_compra=orden.id)
    orden.productos_solicitados = ''
    for detalle in detalles:
        orden.productos_solicitados += str(detalle.producto) + ' x ' + str(detalle.cantidad) + '\n'
    orden.save()
    
@receiver(post_delete, sender=DetalleOrden)
def desc_orden_actualizar(sender, instance, **kwargs):
    orden = OrdenCompra.objects.get(pk=instance.orden_compra.id)
    detalles = DetalleOrden.objects.filter(orden_compra=orden.id)
    orden.productos_solicitados = ''
    for detalle in detalles:
        orden.productos_solicitados += str(detalle.producto) + ' x ' + str(detalle.cantidad) + '\n'
    orden.save()



# agregar stock de productos recepcionados en orden de compra
@receiver(post_save, sender=OrdenCompra)
def asignar_stock_orden(sender, instance, created, **kwargs):
    orden = instance
    if created:
        orden.estado_orden = 'GENERADA'
        orden.save()
    if orden.estado_orden == 'RECIBIDA' and orden.activo == True:
        detalles = DetalleOrden.objects.filter(orden_compra=orden.id)
        for detalle in detalles:
            detalle.producto.stock_actual += detalle.cantidad
            detalle.producto.save()
        orden.activo = False
        orden.save()
    
