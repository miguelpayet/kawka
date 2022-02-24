from django.db import models

from .tipo import Tipo


class TipoFoto(models.Model):
    idfototipo = models.AutoField(primary_key=True)
    idtipo = models.ForeignKey(Tipo, models.DO_NOTHING, db_column='idtipo')
    foto = models.ImageField(max_length=256)

    class Meta:
        managed = False
        db_table = 'tipo_foto'
        verbose_name = 'Foto de Tipo'
        verbose_name_plural = 'Fotos de Tipo'
