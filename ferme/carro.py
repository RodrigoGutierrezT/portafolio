from django.conf import settings
from .models import Producto

class Carro():

    def __init__(self, request):

        self.session = request.session
        carro = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            carro = self.session[settings.BASKET_SESSION_ID] = {}
        self.carro = carro
    

    def agregar(self, producto, cantidad):

        producto_id = str(producto.id)

        if producto_id in self.carro:
            self.carro[producto_id]['cantidad'] = cantidad
        else:
            self.carro[producto_id] = {'precio': int(producto.precio), 'cantidad': int(cantidad)}

        self.guardar()

    def __iter__(self):

        producto_ids = self.carro.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        carro = self.carro.copy()

        for producto in productos:
            carro[str(producto.id)]['producto'] = producto

        for item in carro.values():
            item['total_precio'] = item['precio'] * item['cantidad']
            yield item


    def __len__(self):
        return sum(item['cantidad'] for item in self.carro.values())

    def get_total_precio(self):
        return sum(item['precio'] * item['cantidad'] for item in self.carro.values())

    def get_total_precio_factura(self):
        total_factura = self.get_total_precio() * 0.81
        return round(total_factura)
    
    def get_iva(self):
        total_iva = self.get_total_precio() * 0.19
        return round(total_iva)

    def eliminar(self, producto):
        """
        Eliminar item de los datos de session
        """

        producto_id = str(producto)

        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar()
            
    
    def actualizar(self, producto, cantidad):
        """
        Actualizar valores de los datos de session
        """
        producto_id = str(producto)

        if producto_id in self.carro:
            self.carro[producto_id]['cantidad'] = cantidad
        
        self.guardar()
    
    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        # del self.session["address"]
        # del self.session["purchase"]
        self.guardar()

    

    def guardar(self):
        self.session.modified = True

          