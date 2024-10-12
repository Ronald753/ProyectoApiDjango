from django.db import models

class Cupones(models.Model):
    id_cupon = models.AutoField(primary_key=True)
    cupon = models.CharField(max_length=10)
    porcentaje_descuento = models.IntegerField()
    usos_maximos = models.IntegerField()
    usos_disponibles = models.IntegerField()
    estado = models.BooleanField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cupones'