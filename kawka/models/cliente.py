from django.core.validators import EmailValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.TextField(max_length=256, blank=True, null=True)
    telefono = PhoneNumberField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True, validators=[EmailValidator])

    def __str__(self):
        return self.nombre if self.nombre else self.email if self.email else ('cliente # %s' % self.idcliente)

    class Meta:
        managed = False
        db_table = 'cliente'
