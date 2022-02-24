from django.db import models

from .producto import Producto


class ProductoVariacion(models.Model):
    idproducto_variacion = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='idproducto', blank=True, null=True)
    diferencia_precio = models.IntegerField(db_column='delta_precio')
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre if self.nombre else 'Variación ' + self.idproducto_variacion

    class Meta:
        db_table = 'producto_variacion'
        verbose_name = 'Variación de producto'
        verbose_name_plural = 'Variaciones de producto'
