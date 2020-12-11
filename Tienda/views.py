from django.shortcuts import render, redirect
#importamos httpResponse
from django.http import HttpResponse
#importamos las clases de models
from .models import *
#importamos el formulario del archivo forms.py
from .forms import formProductos, createUserForm
#importamos flash message para enviar un mensaje a una url
from django.contrib import messages
#importaremos las herramientas para hacer la autenticacion de usuario
#para poder trabajar con el login, logout
from django.contrib.auth import authenticate, login, logout
#importamos groups para asignarle el rol al usuario que
#se registre en esta pagina usando el formulario de registro
from django.contrib.auth.models import Group
#impotamos decoradores para restringir el acceso a ciertas paginas que no queremos
#que cualquiera vea
from django.contrib.auth.decorators import login_required
#importamos nuestros decoradores de decorators.py
from .decorators import unauthenticated_user, allowed_users

#rest_framework
from rest_framework import viewsets
from .serializers import ProductosSerializer

# Create your views here.
def home(request):
    deporte = Deporte.objects.all()
    context = {'deporte':deporte}
    return render(request, 'vistas/home.html', context)

def about(request):
    return render(request, 'vistas/about.html')

def products(request, id):
    productos = Productos.objects.filter(tipoDeporte = id)
    deporte = Deporte.objects.get(pk = id)
    context = {'pro':productos, 'dep':deporte}
    return render(request, 'vistas/products.html', context)

@login_required(login_url='home')
@allowed_users(allowed_roles=['administrador'])
def createProduct(request):
    form = formProductos()
    if request.method == 'POST':
        form = formProductos(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('warehouse')
    context = {'form':form, 'title':'Crear Producto'}
    return render(request, 'vistas/product_create.html', context)

@login_required(login_url='home')
@allowed_users(allowed_roles=['administrador'])
def editProduct(request, pk):
    producto = Productos.objects.get(id=pk)
    form = formProductos(instance=producto)
    if request.method == 'POST':
        form = formProductos(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('warehouse')
    context = {'form':form, 'title':'Editar Producto'}
    return render(request, 'vistas/product_create.html', context)

@login_required(login_url='home')
@allowed_users(allowed_roles=['administrador'])
def deleteProduct(request, pk):
    producto = Productos.objects.get(id=pk)
    if request.method == "POST":
        producto.delete()
        return redirect('warehouse')
    context = {'item':producto}
    return render(request, 'vistas/product_delete.html', context)

@login_required(login_url='home')
@allowed_users(allowed_roles=['administrador'])
def warehouse(request):
    productos = Productos.objects.all()
    return render(request, 'vistas/warehouse.html', {'productos': productos})

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'El nombre de usuario o contraseña no coincide')
    context = {}
    return render(request, 'vistas/user_login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='cliente')
            user.groups.add(group)
            messages.success(request, '¡Felicidades! {} su cuenta ha sido creada'.format(username))
            return redirect('login')

    context = {'form': form}
    return render(request, 'vistas/user_register.html', context)


class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer