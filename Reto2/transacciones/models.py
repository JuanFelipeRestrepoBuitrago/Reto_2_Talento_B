from django.db import models


# Create your models here.
class Titulares(models.Model):
    id_titular = models.AutoField(primary_key=True)
    documento_identidad = models.BigIntegerField()
    tipo_documento = models.CharField(max_length=2)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    class Meta:
        managed = False
        db_table = 'titulares'
        unique_together = (('documento_identidad', 'tipo_documento'),)


class Cuentas(models.Model):
    numero_cuenta = models.PositiveBigIntegerField(primary_key=True)
    password = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=9)
    saldo = models.FloatField()
    id_titular = models.ForeignKey('Titulares', models.DO_NOTHING, db_column='id_titular')

    def __str__(self):
        return str(self.numero_cuenta)

    class Meta:
        managed = False
        db_table = 'cuentas'
        unique_together = (('id_titular', 'tipo_cuenta'),)


class TipoTransaccion(models.Model):
    id_tipo_transaccion = models.AutoField(primary_key=True)
    nombre_transaccion = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_transaccion

    class Meta:
        managed = False
        db_table = 'tipo_transaccion'


class Movimientos(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    valor = models.FloatField()
    fecha_transaccion = models.DateTimeField()
    numero_cuenta_salida = models.ForeignKey(Cuentas, models.DO_NOTHING, db_column='numero_cuenta_salida')
    numero_cuenta_entrada = models.ForeignKey(Cuentas, models.DO_NOTHING, db_column='numero_cuenta_entrada', related_name='movimientos_numero_cuenta_entrada_set', blank=True, null=True)
    id_tipo_transaccion = models.ForeignKey('TipoTransaccion', models.DO_NOTHING, db_column='id_tipo_transaccion')

    class Meta:
        managed = False
        db_table = 'movimientos'
