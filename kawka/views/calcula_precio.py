import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from kawka.models.producto import Producto


class ParametroException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SumaView(TemplateView):

    def __init(self):
        pass

    def get(self, request, *args, **kwargs):
        try:
            if 'producto' not in request.GET:
                raise ParametroException('no se puede calcular precio sin producto')
            if 'cantidad' not in request.GET:
                raise ParametroException('no se puede calcular precio sin cantidadd')
        except ParametroException as ex:
            respuesta = HttpResponse(json.dumps({'error': ex.value}))
            respuesta.status_code = 400
            return respuesta
        producto = Producto.objects.get(idproducto=request.GET['producto'])
        variaciones = []
        if 'variacion' in request.GET:
            for v in request.GET['variacion'].split(','):
                variaciones.append(producto.productovariacion_set.get(idproducto_variacion=v))
        total = producto.calcular_total(request.GET['cantidad'], variaciones)
        return HttpResponse(json.dumps({'precio': str(total)}))
