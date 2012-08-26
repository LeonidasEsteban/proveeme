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

	def __unicode__(self):
		if not self.nombre: return self.user.username
		
		return self.nombre

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Empresa.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)