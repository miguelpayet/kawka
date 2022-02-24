from django.db import models

from .producto import Producto


class ProductoOpcion(models.Model):
    idproducto_opcion = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='idproducto', blank=True, null=True)
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre if self.nombre else 'Opción # %s' % self.idproducto_opcion

    class Meta:
        db_table = 'producto_opcion'
        verbose_name = 'Opción de producto'
        verbose_name_plural = 'Opciones de producto'
