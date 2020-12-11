from django.urls import path, include
from Tienda import views
from .views import ProductosViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Productos', ProductosViewSet)

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('products/<str:id>/', views.products, name="products"),
    path('warehouse/', views.warehouse, name="warehouse"),
    path('warehouse/create/', views.createProduct, name="createP"),
    path('warehouse/edit/<str:pk>/', views.editProduct, name="editP"),
    path('warehouse/delete/<str:pk>/', views.deleteProduct, name="deleteP"),
    path('user/login/', views.loginPage, name="login"),
    path('user/logout/', views.logoutPage, name="logout"),
    path('user/register/', views.registerPage, name="register"),
    path('api/', include(router.urls)),
]