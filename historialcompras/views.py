from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ver_historial(request):
    # Lógica para obtener el historial del usuario
    return render(request, 'historialcompras/ver_historial.html')
