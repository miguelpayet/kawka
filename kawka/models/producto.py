from django.db import models


class Producto(models.Model):
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    idproducto = models.AutoField(primary_key=True)
    mostrar = models.BooleanField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    orden = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tipo = models.ForeignKey('Tipo', models.DO_NOTHING, db_column='idtipo', blank=False, null=False)

    def __str__(self):
        return self.nombre if self.nombre else ('Producto %s' % self.idproducto)

    def calcular_total(self, cantidad, variaciones):
        precio_base = self.precio
        for v in variaciones:
            precio_base += v.diferencia_precio
        return precio_base * int(cantidad)

    class Meta:
        managed = False
        db_table = 'producto'
