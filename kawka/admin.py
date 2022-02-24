import nested_admin
from django.contrib import admin

from kawka.models.cliente import Cliente
from kawka.models.parametro import Parametro
from kawka.models.producto import Producto
from kawka.models.pedido import Pedido
from kawka.models.pedido_producto import PedidoProducto
from kawka.models.pedido_producto_variacion import PedidoProductoVariacion
from kawka.models.pedido_producto_opcion import PedidoProductoOpcion
from kawka.models.producto_variacion import ProductoVariacion
from kawka.models.producto_opcion import ProductoOpcion
from kawka.models.tipo import Tipo
from kawka.models.tipo_foto import TipoFoto


# cliente
class ClienteAdmin(admin.ModelAdmin):
    fields = ('nombre', 'direccion', 'telefono', 'email',)
    list_display = ('nombre', 'direccion', 'telefono', 'email',)


admin.site.register(Cliente, ClienteAdmin)


# pedido_producto_opcion
class PedidoProductoOpcionAdmin(nested_admin.NestedStackedInline):
    model = PedidoProductoOpcion
    extra = 0


# pedido_producto_variacion
class PedidoProductoVariacionAdmin(nested_admin.NestedStackedInline):
    model = PedidoProductoVariacion
    extra = 0


# pedido_producto
class PedidoProductoAdmin(nested_admin.NestedStackedInline):
    model = PedidoProducto
    inlines = [PedidoProductoOpcionAdmin, PedidoProductoVariacionAdmin]
    extra = 0


# pedido
class PedidoAdmin(nested_admin.NestedModelAdmin):
    fields = ('cliente', 'tipo_delivery', 'precio')
    list_display = ('idpedido', 'fecha_creacion', 'cliente', 'tipo_delivery')
    inlines = [PedidoProductoAdmin]
    ordering = ('-fecha_creacion',)


admin.site.register(Pedido, PedidoAdmin)


# producto variación
class ProductoVariacionAdmin(nested_admin.NestedStackedInline):
    model = ProductoVariacion
    extra = 0


# producto opcion
class ProductoOpcionAdmin(nested_admin.NestedStackedInline):
    model = ProductoOpcion
    extra = 0


# producto
class ProductoAdmin(nested_admin.NestedModelAdmin):
    fields = ('nombre', ('orden', 'mostrar',), 'tipo', 'descripcion', 'precio',)
    list_display = ('tipo', 'orden', 'nombre', 'mostrar',)
    ordering = ('tipo', 'orden', 'nombre',)
    inlines = [ProductoOpcionAdmin, ProductoVariacionAdmin]


admin.site.register(Producto, ProductoAdmin)


# tipo_foto
class TipoFotoAdmin(nested_admin.NestedStackedInline):
    model = TipoFoto
    extra = 0


# tipo
class TipoAdmin(nested_admin.NestedModelAdmin):
    fields = ('nombre', ('orden', 'mostrar',), 'imagenlista',)
    list_display = ('orden', 'nombre', 'mostrar',)
    inlines = [TipoFotoAdmin]
    ordering = ('orden', 'nombre',)


admin.site.register(Tipo, TipoAdmin)


# parametro
class ParametroAdmin(admin.ModelAdmin):
    fields = ('nombre', 'texto',)
    list_display = ('nombre', 'texto',)


admin.site.register(Parametro, ParametroAdmin)
