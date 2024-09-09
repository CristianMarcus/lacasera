from django.shortcuts import render


def index(request):
    return render(request, 'promoOfertas/index.html')  # Asegúrate de que el template 'index.html' exista
