# core/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')  # Renderiza la plantilla index.html
