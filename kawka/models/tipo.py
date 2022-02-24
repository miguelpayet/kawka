from django.db import models


class Tipo(models.Model):
    idtipo = models.AutoField(primary_key=True)
    imagenlista = models.ImageField(db_column='imagenLista', max_length=250, blank=True, null=True)
    imagentipo = models.CharField(db_column='imagenTipo', max_length=250, blank=True, null=True)
    mostrar = models.BooleanField()
    nombre = models.CharField(max_length=50, blank=True, null=True)
    orden = models.IntegerField(unique=True)

    def __str__(self):
        return self.nombre if self.nombre else ('Tipo %s' % self.idtipo)

    class Meta:
        managed = False
        db_table = 'tipo'
