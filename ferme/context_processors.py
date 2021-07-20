from .models import Categoria
from .carro import Carro

def categorias(request):
    return {
        'categorias': Categoria.objects.all()
    }

def carro(request):
    return {'carro': Carro(request)}