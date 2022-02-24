from django.views.generic import TemplateView

from kawka.models.pedido import Pedido


class PedidoMailView(TemplateView):
    template_name = 'pedido_mail.html'

    def get_context_data(self, **kwargs):
        context = {}
        if 'pedido' not in kwargs:
            raise Exception('no recibió número de pedido')
        try:
            pedido = Pedido.objects.get(idpedido=kwargs['pedido'])
            pedido.productos = pedido.pedidoproducto_set.all()
            for pp in pedido.productos:
                pp.variaciones = pp.pedidoproductovariacion_set.all()
                pp.opciones = pp.pedidoproductoopcion_set.all()
        except Pedido.DoesNotExist:
            raise Exception('pedido %s no existe' % kwargs['pedido'])
        context['pedido'] = pedido
        return context
