from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Producto(models.Model):
	nombre = models.TextField()

	def __unicode__(self):
		return self.nombre

class Region(models.Model):
	nombre = models.TextField()

	def __unicode__(self):
		return self.nombre


# Create your models here.
class Empresa(models.Model):
	user 	  = models.OneToOneField(User)
	nombre	  = models.TextField()
	telefono  = models.CharField(max_length=100)
	publico   = models.BooleanField(default=False)
	productos = models.ManyToManyField(Producto, blank=True)
	regiones  = models.ManyToManyField(Region, blank=True)

	def solicitudes(self):
		return Solicitud.objects.filter(solicitado=self)

	def cotizaciones(self):
		return Solicitud.objects.filter(solicitante=self)

	def __unicode__(self):
		if not self.nombre: return self.user.username
		
		return self.nombre

class Solicitud(models.Model):
	producto 	= models.ForeignKey(Producto)

	solicitante = models.ForeignKey(Empresa, related_name='solicitante')
	solicitado  = models.ForeignKey(Empresa, related_name='solicitado')

	cotizacion  = models.CharField(max_length=300, blank=True)
	adjunto     = models.FileField(blank=True, upload_to='adjuntos')



def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Empresa.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)