from django.db import models
from PIL import Image
from django.utils.deconstruct import deconstructible
import datetime

# Create your models here.
#funcion para renombrar imagen
@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        fecha = datetime.datetime.now()
        # set filename as random string
        filename = '{}-{}.{}'.format(instance.nombre, fecha.strftime("%x%X").replace("/", "").replace(":", ""), ext)
        # return the whole path to the file
        return self.path + filename

class Deporte(models.Model):
    nombre=models.CharField(max_length=20)

    path_and_rename = PathAndRename("imgCategory/")

    foto = models.ImageField(upload_to=path_and_rename, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Productos(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=200, null=True, blank=True)
    precio=models.IntegerField()
    tipoDeporte=models.ForeignKey(Deporte, null=True, on_delete= models.SET_NULL)

    path_and_rename = PathAndRename("imgProductos/")

    foto = models.ImageField(upload_to=path_and_rename, null=True, blank=True)

    def __str__(self):
        return self.nombre