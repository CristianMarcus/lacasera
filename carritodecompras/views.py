from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Carrito, LineaCarrito
from .forms import CarritoForm, LineaCarritoForm


# Listado de carritos
class CarritoListView(ListView):
    model = Carrito
    template_name = 'carritodecompras/carrito_list.html'
    context_object_name = 'carritos'

# Detalle de un carrito
class CarritoDetailView(DetailView):
    model = Carrito
    template_name = 'carritodecompras/carrito_detail.html'
    context_object_name = 'carrito'

# Crear un carrito
class CarritoCreateView(CreateView):
    model = Carrito
    form_class = CarritoForm
    template_name = 'carritodecompras/carrito_form.html'
    success_url = '/carritos/'

# Editar un carrito
class CarritoUpdateView(UpdateView):
    model = Carrito
    form_class = CarritoForm
    template_name = 'carritodecompras/carrito_form.html'
    success_url = '/carritos/'

# Listado de líneas de carrito
class LineaCarritoListView(ListView):
    model = LineaCarrito
    template_name = 'carritodecompras/linea_carrito_list.html'
    context_object_name = 'lineas_carrito'

# Detalle de una línea de carrito
class LineaCarritoDetailView(DetailView):
    model = LineaCarrito
    template_name = 'carritodecompras/linea_carrito_detail.html'
    context_object_name = 'linea_carrito'

# Crear una línea de carrito
class LineaCarritoCreateView(CreateView):
    model = LineaCarrito
    form_class = LineaCarritoForm
    template_name = 'carritodecompras/linea_carrito_form.html'
    success_url = '/lineas-carrito/'

# Editar una línea de carrito
class LineaCarritoUpdateView(UpdateView):
    model = LineaCarrito
    form_class = LineaCarritoForm
    template_name = 'carritodecompras/linea_carrito_form.html'
    success_url = '/lineas-carrito/'
