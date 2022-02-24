from django.db import models

from producto import Producto


class ProductoFoto(models.Model):
    idfotoproducto = models.AutoField(primary_key=True)
    imagen = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='idproducto', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto_foto'
