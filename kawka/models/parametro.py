from django.db import models


class Parametro(models.Model):
    idparametro = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    texto = models.TextField(max_length=256)

    def __str__(self):
        return self.nombre if self.nombre else 'Parámatro # %s' % self.idparametro

    class Meta:
        managed = False
        db_table = 'parametro'
        unique_together = ('idparametro',)
