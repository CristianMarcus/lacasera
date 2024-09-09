from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'pagos/index.html')  # Asegúrate de que el template 'index.html' exista
