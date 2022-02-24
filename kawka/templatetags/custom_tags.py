from django import template
from django.contrib.auth import get_user_model
from django.template.loader import get_template

register = template.Library()

User = get_user_model()


def sumador(context, producto):
    return {'producto': producto}


sumador_template = get_template('producto.html')
register.inclusion_tag(sumador_template, takes_context=True)(sumador)


def titulador(context):
    return {}


titulador_template = get_template('titulador.html')
register.inclusion_tag(titulador_template, takes_context=True)(titulador)
