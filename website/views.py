#-*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from models import Producto, Empresa, Region, Solicitud
from django.template import RequestContext
import utils

def home(req):
	return render_to_response('website/home.html', RequestContext(req))

def entrar(req):
	if req.method == 'POST':
		user 	 = req.POST.get('user')
		passwd 	 = req.POST.get('passwd')

		if user and passwd:
			user = authenticate(username=user, password=passwd)

			if user is not None:
				if user.is_active:
					login(req, user)

					return redirect('website.views.solicitudes')

	return render_to_response('website/entrar.html', RequestContext(req))

def registro(req):
	if req.method == 'POST':
		nombre = req.POST.get('nombre')
		email  = req.POST.get('email')
		tel    = req.POST.get('telefono')
		prods   = req.POST.getlist('producto[]')

		if nombre and email and tel:

			user = User.objects.create_user(username=utils.generate_username(nombre), email=email)
			user.save()

			empresa = user.get_profile()
			empresa.telefono = tel
			empresa.nombre = nombre

			if prods: empresa.publico = True

			empresa.save()

			if prods:
				for p in prods:
					# TODO: checar si el producto ya existe, si ya existe no volverlo a crear
					producto = Producto(nombre=p)
					producto.save()

					empresa.productos.add(producto)

			return HttpResponse('<legend>Gracias por registrarte.</legend><p>Revisa tu correo y haz click en el link que te enviamos para completar tu registro.</p>')

	return render_to_response('website/registro.html', RequestContext(req))

@login_required(login_url='/entrar')
def cotiza(req):
	if req.method == 'POST':
		prods = req.POST.getlist('producto[]')

		if prods:
			count = 0
			for p in prods:
				producto = Producto.objects.filter(nombre=p)

				if producto.exists():
					producto = producto[0]

					for e in Empresa.objects.filter(productos=producto):
						sol = Solicitud(solicitante=req.user.get_profile(), solicitado=e, producto=producto)
						sol.save()
						count = count + 1 

			return HttpResponse('<legend>¡Listo!</legend><p>Tu solicitud se ha enviado a <strong>%s empresas</strong>. Ahora solo debes esperar. Te notificaremos cuando lleguen cotizaciones.</p>' % count)

	return render_to_response('website/cotiza.html', RequestContext(req))

@login_required(login_url='/entrar')
def solicitudes(req):

	if req.method == 'POST':
		solicitud = req.POST.get('solicitud_id')
		precio    = req.POST.get('precio')

		if solicitud and precio:
			solicitud = Solicitud.objects.get(pk=solicitud)
			solicitud.cotizacion = precio
			solicitud.save()


	return render_to_response('website/solicitudes.html', RequestContext(req))

@login_required(login_url='/entrar')
def cotizaciones(req):
	return render_to_response('website/cotizaciones.html', RequestContext(req))

@login_required(login_url='/entrar')
def salir(req):
	logout(req)

	return redirect('website.views.entrar')


# serach engine
def buscar_producto(req):
	if req.GET.get('term'):
		productos = Producto.objects.filter(nombre__startswith=req.GET.get('term'))
	else:
		productos = Producto.objects.all()


	values = list()
	for p in productos:
		values.append({ 'key' : p.nombre , 'value': p.nombre })

	return HttpResponse(simplejson.dumps(values))

def buscar_region(req):
	if req.GET.get('term'):
		regiones = Region.objects.filter(nombre__startswith=req.GET.get('term'))
	else:
		regiones = Region.objects.all()


	values = list()
	for r in regiones:
		values.append({ 'key' : r.nombre , 'value': r.nombre })

	return HttpResponse(simplejson.dumps(values))


def buscar_empresas(req):
	count = 0

	if req.GET.get('productos'):
		prods = req.GET.get('productos').split(',')

		q = None
		for p in prods:
			if q is None:
				q = Q(productos__nombre=p)
			else:
				q = q | Q(productos__nombre=p)

		count = Empresa.objects.filter(q).count()

	#if req.GET.get('regiones'):

	msg = '<p><strong>%d</strong> empresas concuerdan con estas características.</p>' % count

	if count == 0:
		msg = '<p>Ninguna empresas concuerdan con estas características.</p>'

	return HttpResponse(msg)