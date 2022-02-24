from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseServerError
from django.db.models import Q

from kawka.models.parametro import Parametro
from kawka.models.tipo import Tipo
from kawka.models.pedido import Pedido
from kawka.models.producto import Producto
from kawka.models.producto_variacion import ProductoVariacion
from kawka.models.producto_opcion import ProductoOpcion
from kawka.models.pedido_producto_variacion import PedidoProductoVariacion
from kawka.models.pedido_producto_opcion import PedidoProductoOpcion
from kawka.models.pedido_producto import PedidoProducto


class PedidoFormView(TemplateView):
    template_name = 'pedido.html'

    def __init__(self):
        super().__init__()
        self.pedido = {}

    def post(self, request):
        self.leer_pedido(request.POST)
        self.grabar_pedido()
        return HttpResponse("close one bro")

    def get_context_data(self, **kwargs):
        context = {}
        tipos = []
        p = Parametro.objects.get(nombre='introduccion')
        context['introduccion'] = p.texto
        for t in Tipo.objects.filter(mostrar=True).order_by('orden').all():
            productos = []
            for p in t.producto_set.filter(mostrar=True).order_by('orden').all():
                p.variaciones = p.productovariacion_set.all()
                p.opciones = p.productoopcion_set.all()
                productos.append(p)
            tipos.append({'tipo': t, 'productos': productos})
        context['tipos'] = tipos
        return context

    def grabar_pedido(self):
        pedido = Pedido()
        pedido.agregar_cliente(self.pedido['cliente']['email'], self.pedido['cliente']['telefono'], self.pedido['cliente']['direccion'])
        pedido.tipo_delivery = self.pedido['opciones_entrega']
        pedido.save()
        for p in self.pedido['productos']:
            try:
                pedido_producto = PedidoProducto(comentario=p['comentario'], producto=Producto.objects.get(idproducto=p['idproducto']),
                                                 cantidad=p['cantidad'])
                pedido_producto.agregar_a_pedido(pedido)
                criterio_producto = Q(producto_id=p['idproducto'])
                for v in p['variaciones']:
                    try:
                        pedido_producto_variacion = PedidoProductoVariacion(
                            variacion=ProductoVariacion.objects.get(criterio_producto & Q(idproducto_variacion=v)))
                        pedido_producto_variacion.agregar_a_pedido_producto(pedido_producto)
                    except ProductoVariacion.DoesNotExist:
                        return HttpResponseServerError('variación de producto no existe')
                if 'opcion' in p and p['opcion'] != '':
                    try:
                        pedido_producto_opcion = PedidoProductoOpcion(
                            opcion=ProductoOpcion.objects.get(criterio_producto & Q(idproducto_opcion=p['opcion'])))
                        pedido_producto_opcion.agregar_a_pedido_producto(pedido_producto)
                    except ProductoOpcion.DoesNotExist:
                        return HttpResponseServerError('opción de producto no existe')
                pedido_producto.save()
            except Producto.DoesNotExist:
                return HttpResponseServerError('producto no existe')
        pedido.save()
        pedido.enviar_mail()

    def leer_pedido(self, formdict):
        self.pedido['cliente'] = {'email': formdict['email'], 'telefono': formdict['telefono'], 'direccion': formdict['direccion']}
        self.pedido['opciones_entrega'] = formdict['opciones_entrega']
        productos = []
        for key, value in [x for x in formdict.items() if 'cantidad' in x[0] and int(x[1]) > 0]:
            producto = {'idproducto': key[key.find('-') + 1:], 'cantidad': int(value)}
            producto['comentario'] = formdict['comentarios-%s' % producto['idproducto']] if 'comentarios-%s' % producto[
                'idproducto'] in formdict else ''
            producto['variaciones'] = list(
                [x[0][x[0].find('variacion-') + 10:] for x in formdict.items() if ('producto-%s-variacion-' % producto['idproducto']) in x[0]])
            producto['opcion'] = formdict['opciones-producto-%s' % producto['idproducto']] if 'opciones-producto-%s' % producto[
                'idproducto'] in formdict else ''
            productos.append(producto)
        self.pedido['productos'] = productos
