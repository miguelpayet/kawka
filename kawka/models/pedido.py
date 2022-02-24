from django.db import models
from functools import reduce

from .cliente import Cliente
from django.template.loader import render_to_string
from django.core.mail import send_mail


class Pedido(models.Model):
    idpedido = models.AutoField(primary_key=True, db_column='idpedido')
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='idcliente')
    tipo_delivery = models.CharField(max_length=45)
    fecha_creacion = models.DateTimeField(editable=False, auto_now_add=True)
    precio = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return "Pedido %s" % self.idpedido

    def agregar_cliente(self, email, telefono, direccion):
        cliente = None
        try:
            cliente = Cliente.objects.get(telefono=telefono)
        except Cliente.DoesNotExist:
            pass
        if not cliente:
            try:
                cliente = Cliente.objects.get(email=telefono.lower())
            except Cliente.DoesNotExist:
                pass
        if not cliente:
            cliente = Cliente(telefono=telefono, email=email, direccion=direccion)
            cliente.save()
        else:
            if not cliente.direccion and direccion:
                cliente.direccion = direccion
                cliente.save()
        self.cliente = cliente

    def calcular_total(self):
        precio = reduce(lambda x, y: x + y, [x.precio for x in self.pedidoproducto_set.all()], 0)
        self.precio = precio

    def enviar_mail(self):
        context = {}
        self.productos = self.pedidoproducto_set.all()
        for pp in self.productos:
            pp.variaciones = pp.pedidoproductovariacion_set.all()
            pp.opciones = pp.pedidoproductoopcion_set.all()
        context['pedido'] = self
        t = render_to_string('pedido_mail.html')
        send_mail('Order details', t, 'kawka@kawkabread.com', [self.cliente.email], fail_silently=False, )

    def save(self, *args, **kwargs):
        self.calcular_total()
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'pedido'
        unique_together = (('idpedido', 'cliente'),)
