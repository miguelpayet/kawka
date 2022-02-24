from django.db import models

from .pedido_producto import PedidoProducto
from .producto_opcion import ProductoOpcion


class PedidoProductoOpcion(models.Model):
    idpedido_producto_opcion = models.AutoField(primary_key=True)
    pedido_producto = models.ForeignKey(PedidoProducto, models.DO_NOTHING, db_column='idpedido_producto')
    opcion = models.ForeignKey(ProductoOpcion, models.DO_NOTHING, db_column='idproducto_opcion')

    def __str__(self):
        return '%s (pedido %s)' % (self.opcion.nombre, self.pedido_producto.pedido.idpedido)

    def agregar_a_pedido_producto(self, pedido_producto):
        self.pedido_producto = pedido_producto
        self.save()

    class Meta:
        managed = False
        db_table = 'pedido_producto_opcion'
        verbose_name = 'Opción del producto'
        verbose_name_plural = 'Opciones del producto'
