from django.forms import ModelForm, ValidationError, SelectDateWidget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Proveedor, Empleado, Producto, Categoria, OrdenCompra, Factura, Compra, NotaCredito

class ClienteAdminForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_rut(self):
        try:
            rut = self.cleaned_data['rut']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
    
    def clean_telefono(self):
        try:
            telefono = self.cleaned_data['telefono']
            if len(telefono) < 8:
                raise ValidationError()
            if telefono.isnumeric():
                return self.cleaned_data['telefono']
            else:
                raise ValidationError()
        except:
            msg = 'Teléfono incorrecto, debe ingresar sólo números con un largo de 8 ó 9 carácteres'
            raise ValidationError(msg)


class ProveedorAdminForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def clean_rut(self):
        try:
            rut = self.cleaned_data['rut']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
        
    def clean_telefono(self):
        try:
            telefono = self.cleaned_data['telefono']
            if len(telefono) < 8:
                raise ValidationError()
            if telefono.isnumeric():
                return self.cleaned_data['telefono']
            else:
                raise ValidationError()
        except:
            msg = 'Teléfono incorrecto, debe ingresar sólo números con un largo de 8 ó 9 carácteres'
            raise ValidationError(msg)


class EmpleadoAdminForm(ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

    def clean_rut(self):
        try:
            rut = self.cleaned_data['rut']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
    
    def clean_telefono(self):
        try:
            telefono = self.cleaned_data['telefono']
            if len(telefono) < 8:
                raise ValidationError()
            if telefono.isnumeric():
                return self.cleaned_data['telefono']
            else:
                raise ValidationError()
        except:
            msg = 'Teléfono incorrecto, debe ingresar sólo números con un largo de 8 ó 9 carácteres'
            raise ValidationError(msg)

class OrdenForm(ModelForm):

    class Meta:
        model = OrdenCompra
        fields = '__all__'
        exclude = ('productos_solicitados' ,'fecha_solicitud', 'activo', 'fecha_recepcion', 'empleado')

class OrdenModificarForm(ModelForm):

    class Meta:
        model = OrdenCompra
        fields = '__all__'
        exclude = ('fecha_solicitud', 'activo', 'fecha_recepcion')

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ('cod_prod', 'slug')

        widgets = {
            "fecha_vencimiento": SelectDateWidget(years=range(2021, 2042))
        }

class ClienteForm(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ('user',)

        widgets = {
            "fecha_nacimiento": SelectDateWidget(years=range(1920, 2022))
        }


    def clean_rut(self):
        try:
            rut = self.cleaned_data['rut']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
    
    def clean_telefono(self):
        try:
            telefono = self.cleaned_data['telefono']
            if len(telefono) < 8:
                raise ValidationError()
            if telefono.isnumeric():
                return self.cleaned_data['telefono']
            else:
                raise ValidationError()
        except:
            msg = 'Teléfono incorrecto, debe ingresar sólo números con un largo de 8 ó 9 carácteres'
            raise ValidationError(msg)


class ClientePerfilForm(ModelForm):

    class Meta:
        model = Cliente
        fields = ('telefono',)

class EmpleadoPerfilForm(ModelForm):

    class Meta:
        model = Empleado
        fields = ('telefono',)

class ProveedorPerfilForm(ModelForm):

    class Meta:
        model = Proveedor
        fields = ('telefono',)

class EmpresaFacturaForm(ModelForm):

    class Meta:
        model = Factura
        fields = ('nombre_empresa','rut_empresa','telefono')
    
    def clean_rut_empresa(self):
        try:
            rut = self.cleaned_data['rut_empresa']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut_empresa']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
    
    def clean_telefono(self):
        try:
            telefono = self.cleaned_data['telefono']
            if len(telefono) < 8:
                raise ValidationError()
            if telefono.isnumeric():
                return self.cleaned_data['telefono']
            else:
                raise ValidationError()
        except:
            msg = 'Teléfono incorrecto, debe ingresar sólo números con un largo de 8 ó 9 carácteres'
            raise ValidationError(msg)
    
    def clean_nombre_empresa(self):
        try:
            nombre_empresa = self.cleaned_data['nombre_empresa']
            if len(nombre_empresa) < 4:
                raise ValidationError()
            else:
                return self.cleaned_data['nombre_empresa']
        except:
            msg = 'El nombre de empresa debe tener como mínimo 5 caracteres'
            raise ValidationError(msg)

class CompraBoletaForm(ModelForm):
    rut_cliente = forms.CharField(max_length=9)

    class Meta:
        model = Compra
        fields = ('rut_cliente',) + ('nombre', 'apellido_paterno', 'medio_pago')
        # exclude = ('user', 'email', 'fecha', 'order_key', 'pagado','empleado')
    
    def clean_rut_cliente(self):
        try:
            rut = self.cleaned_data['rut_cliente']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut_cliente']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)

    def clean_nombre(self):
        try:
            nombre = self.cleaned_data['nombre']
            if len(nombre) < 3:
                raise ValidationError()
            else:
                return self.cleaned_data['nombre']
        except:
            msg = 'El nombre debe tener como mínimo 3 caracteres'
            raise ValidationError(msg)
    
    def clean_apellido_paterno(self):
        try:
            apellido_paterno = self.cleaned_data['apellido_paterno']
            if len(apellido_paterno) < 2:
                raise ValidationError()
            else:
                return self.cleaned_data['apellido_paterno']
        except:
            msg = 'El apellido debe tener como mínimo 2 caracteres'
            raise ValidationError(msg)

class CompraFacturaForm(ModelForm):
    rut_empresa = forms.CharField(max_length=9)
    telefono = forms.CharField(max_length=9)
    nombre_empresa = forms.CharField(max_length=50)

    class Meta:
        model = Compra
        fields = ('nombre', 'apellido_paterno', 'medio_pago') +  ('nombre_empresa','rut_empresa','telefono')
    
    def clean_nombre(self):
        try:
            nombre = self.cleaned_data['nombre']
            if len(nombre) < 3:
                raise ValidationError()
            else:
                return self.cleaned_data['nombre']
        except:
            msg = 'El nombre debe tener como mínimo 3 caracteres'
            raise ValidationError(msg)
    
    def clean_apellido_paterno(self):
        try:
            apellido_paterno = self.cleaned_data['apellido_paterno']
            if len(apellido_paterno) < 2:
                raise ValidationError()
            else:
                return self.cleaned_data['apellido_paterno']
        except:
            msg = 'El apellido debe tener como mínimo 2 caracteres'
            raise ValidationError(msg)
    
    def clean_rut_empresa(self):
        try:
            rut = self.cleaned_data['rut_empresa']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut_empresa']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
    
    def clean_telefono(self):
        try:
            telefono = self.cleaned_data['telefono']
            if len(telefono) < 8:
                raise ValidationError()
            if telefono.isnumeric():
                return self.cleaned_data['telefono']
            else:
                raise ValidationError()
        except:
            msg = 'Teléfono incorrecto, debe ingresar sólo números con un largo de 8 ó 9 carácteres'
            raise ValidationError(msg)
    
    def clean_nombre_empresa(self):
        try:
            nombre_empresa = self.cleaned_data['nombre_empresa']
            if len(nombre_empresa) < 4:
                raise ValidationError()
            else:
                return self.cleaned_data['nombre_empresa']
        except:
            msg = 'El nombre de empresa debe tener como mínimo 5 caracteres'
            raise ValidationError(msg)

class NotaForm(ModelForm):

    class Meta:
        model = NotaCredito
        fields = "__all__"
        exclude = ('total_devolucion', 'empleado', 'estado')
    
    def clean(self):
        if self.cleaned_data['boleta'] is not None and self.cleaned_data['factura'] is not None:
            raise ValidationError('No puede generar una nota de crédito para boleta y factura al mismo tiempo. Por favor seleccione sólo una opción')
        
        if self.cleaned_data['boleta'] is None and self.cleaned_data['factura'] is None:
            raise ValidationError('Debe seleccionar una boleta o una factura para generar la nota de crédito')
        
        if self.cleaned_data['boleta'] is not None and  NotaCredito.objects.filter(boleta = self.cleaned_data['boleta']).filter(estado = 'GENERADA').exists():
            raise ValidationError('Ya existe una nota de crédito activa para esta boleta')
        elif self.cleaned_data['factura'] is not None and NotaCredito.objects.filter(factura = self.cleaned_data['factura']).filter(estado = 'GENERADA').exists():
            raise ValidationError('Ya existe una nota de crédito activa para esta factura')
    
    def clean_nombre_cliente(self):
        try:
            nombre = self.cleaned_data['nombre_cliente']
            if len(nombre) < 3:
                raise ValidationError()
            else:
                return self.cleaned_data['nombre_cliente']
        except:
            msg = 'El nombre debe tener como mínimo 3 caracteres'
            raise ValidationError(msg)
    
    def clean_apellido_cliente(self):
        try:
            apellido_cliente = self.cleaned_data['apellido_cliente']
            if len(apellido_cliente) < 2:
                raise ValidationError()
            else:
                return self.cleaned_data['apellido_cliente']
        except:
            msg = 'El apellido debe tener como mínimo 2 caracteres'
            raise ValidationError(msg)
    
    def clean_rut(self):
        try:
            rut = self.cleaned_data['rut']
            if len(rut) < 8:
                raise ValidationError()
            verificador = rut[-1]
            rut = rut[:-1]
            if rut.isnumeric() and (verificador.isnumeric() or verificador.upper() == 'K'):
                return self.cleaned_data['rut']
            else:
                raise ValidationError()
        except:
            msg = 'Rut incorrecto, debe ingresarlo sin puntos ni guión'
            raise ValidationError(msg)
