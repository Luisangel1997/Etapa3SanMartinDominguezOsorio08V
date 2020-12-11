from django.test import TestCase
from Tienda.forms import formProductos
from Tienda.models import Productos
from django.core.files.uploadedfile import SimpleUploadedFile

class formProductosTest(TestCase):
    def test_valid_form(self):
        j = Productos.objects.create(nombre='pelota de tenis', descripcion='es buena')
        data = {'nombre': j.nombre, 'descripcion': j.descripcion,}
        form = formProductos(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        j = Productos.objects.create(nombre='pelota de tenis', descripcion='es buena')
        data = {'nombre': j.nombre, 'descripcion': j.descripcion,}
        form = formProductos(data=data)
        self.assertTrue(form.is_valid())