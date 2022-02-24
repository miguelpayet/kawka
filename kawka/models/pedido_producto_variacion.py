from django.db import models

from .pedido_producto import PedidoProducto
from .producto_variacion import ProductoVariacion


class PedidoProductoVariacion(models.Model):
    idpedido_producto_variacion = models.AutoField(primary_key=True)
    pedido_producto = models.ForeignKey(PedidoProducto, models.DO_NOTHING, db_column='idpedido_producto')
    variacion = models.ForeignKey(ProductoVariacion, models.DO_NOTHING, db_column='idproducto_variacion')

    def __str__(self):
        return '%s (pedido %s)' % (self.variacion.nombre, self.pedido_producto.pedido.idpedido)

    def agregar_a_pedido_producto(self, pedido_producto):
        self.pedido_producto = pedido_producto
        self.save()

    class Meta:
        managed = False
        db_table = 'pedido_producto_variacion'
        verbose_name = 'Variación del producto'
        verbose_name_plural = 'Variaciones del producto'
