from django.shortcuts import render

# Create your views here.
# Definir la vista 'index'
def index(request):
    return render(request, 'productos/index.html')