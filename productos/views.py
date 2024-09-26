# productos/views.py
from django.shortcuts import render

def menu(request):
    # Lógica para la vista del menú
    return render(request, 'productos/menu.html')
