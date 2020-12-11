from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from Productos.models import Productos

class GenreListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_producto = 10

        for producto_id in range(number_of_producto):
            Productos.objects.create(
                nombre=f'Accion {producto_id}',
                descripcion=f'Prueba {producto_id}',
            )
           
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/Tienda/Productos/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('Productos'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('Productos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Vistas/products.html')
        
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('Productos'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['products']) == 10)

    def test_lists_all_genres(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('Productos')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['products']) == 3)