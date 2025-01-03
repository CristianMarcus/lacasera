from django.db import models
from django.utils.timezone import now
from productos.models import Producto
from usuarios.models import Usuario
from django.core.exceptions import ValidationError


class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, choices=ESTADOS_PEDIDO, default='Pendiente')
    fecha_pedido = models.DateTimeField(default=now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Calculado automáticamente
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def clean(self):
        """Validar que dirección y teléfono estén presentes."""
        if not self.direccion:
            if not self.cliente.address:
                raise ValidationError("El pedido debe tener una dirección válida.")
            self.direccion = self.cliente.address

        if not self.telefono:
            if not self.cliente.phone_number:
                raise ValidationError("El pedido debe tener un número de teléfono válido.")
            self.telefono = self.cliente.phone_number
    

    def calcular_total(self):
        """
        Calcula el total del pedido sumando los subtotales de las líneas.
        """
        self.total = sum(linea.get_subtotal() for linea in self.lineas.all())
        self.save()
        
    def guardar_datos_cliente(self):
        """
        Guarda dirección y teléfono desde el cliente si no están definidos.
        """
        if not self.direccion:
            self.direccion = self.cliente.address or "Dirección no especificada"
        if not self.telefono:
            self.telefono = self.cliente.phone_number or "Teléfono no especificado"    
        

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"


class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="lineas", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        """Calcula el subtotal de la línea."""
        return self.cantidad * self.precio_unitario

   
