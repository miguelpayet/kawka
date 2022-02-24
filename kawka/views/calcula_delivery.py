import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from kawka.models.producto import Producto

from kawka.models.parametro import Parametro


class CalculaDeliveryView(TemplateView):

    def __init(self):
        pass

    def get(self, request, *args, **kwargs):
        try:
            parametro = Parametro.objects.get(nombre='delivery')
            return HttpResponse(json.dumps({'delivery': parametro.texto}))
        except Parametro.DoesNotExist as ex:
            respuesta = HttpResponse(json.dumps({'error': ex.value}))
            respuesta.status_code = 400
            return respuesta
