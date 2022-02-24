from django.views.generic import TemplateView

from kawka.models.parametro import Parametro
from kawka.models.tipo import Tipo


class PedidoView(TemplateView):
    template_name = 'pedido.html'

    def get_context_data(self, **kwargs):
        context = {}
        tipos = []
        p = Parametro.objects.first()
        context['introduccion'] = p.texto
        for t in Tipo.objects.filter(mostrar=True).order_by('orden').all():
            productos = []
            for p in t.producto_set.filter(mostrar=True).order_by('orden').all():
                p.variaciones = p.productovariacion_set.all()
                productos.append(p)
            tipos.append({'tipo': t, 'productos': productos})
        context['tipos'] = tipos
        return context
