#-*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.utils import simplejson
from models import Producto, Empresa, Region

def home(req):
	return render_to_response('website/home.html')

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

