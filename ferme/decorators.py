from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('No tienes los privilegios para acceder a esta página')
		return wrapper_func
	return decorator

def is_cliente(user):
    return user.groups.filter(name='CLIENTE').exists()

def is_empleado(user):
	valor = False
	if user.groups.filter(name='SUPERVISOR').exists():
		valor = True
	elif user.groups.filter(name='VENDEDOR').exists():
		valor = True
	elif user.groups.filter(name='ADMIN').exists():
		valor = True
	
	return valor

def is_vendedor(user):
	return user.groups.filter(name='VENDEDOR').exists()

def is_proveedor(user):
    return user.groups.filter(name='PROVEEDOR').exists()

