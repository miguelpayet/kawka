from django.db import models

from .pedido import Pedido


class PedidoProducto(models.Model):
    idpedido_producto = models.AutoField(primary_key=True, db_column='idpedido_producto')
    cantidad = models.IntegerField(blank=True, null=True)
    comentario = models.CharField(max_length=128, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, models.DO_NOTHING, db_column='idpedido')
    producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='idproducto')
    precio = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s (pedido %s)' % (self.producto.nombre, self.pedido.idpedido)

    def agregar_a_pedido(self, pedido):
        self.pedido = pedido
        self.save()

    def calcular_total(self):
        v = list([x.variacion for x in self.pedidoproductovariacion_set.all()])
        self.precio = self.producto.calcular_total(self.cantidad, v)

    def save(self, *args, **kwargs):
        self.calcular_total()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'pedido_producto'
        verbose_name = 'Producto del pedido'
        verbose_name_plural = 'Productos del pedido'
