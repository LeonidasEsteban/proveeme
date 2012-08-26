# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from models import Producto, Empresa, Region
from django.utils import simplejson

def home(req):
	return render_to_response('website/home.html')

def buscar_producto(req):
	values = list()
	for p in Producto.objects.all():
		values.append({ 'key' : p.nombre , 'value': p.nombre })

	return HttpResponse(simplejson.dumps(values))