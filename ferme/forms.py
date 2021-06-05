from django.forms import ModelForm, ValidationError, SelectDateWidget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Proveedor, Empleado, Producto, Categoria, OrdenCompra

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
