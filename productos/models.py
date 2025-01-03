from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0, message="El precio no puede ser negativo.")]
    )  # Validación directa
    descripcion = models.TextField()
    disponible = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0, message="El stock no puede ser negativo.")]
    )  # Evitar valores negativos
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='productos', 
        null=True, 
        blank=True
    )
    imagen = models.ImageField(upload_to='media/productos/', blank=True, null=True)  # Cambiar a "media/"

    def clean(self):
        """Validaciones adicionales."""
        if self.precio < 0:
            raise ValidationError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")

    def __str__(self):
        return self.nombre

