from enum import unique
from peewee import AutoField, BaseTable, BooleanField, CharField, DateTimeField, ForeignKeyField, PrimaryKeyField, SqliteDatabase, Model, TextField, DateField, IntegerField, TimeField

db = SqliteDatabase('registros_efetivos.db')

class BaseTable(Model):
    class Meta:
        database = db


class Voluntario(BaseTable):
    id = PrimaryKeyField(null=False)
    discord_id = TextField(null=False)
    nome = TextField(null=False)


class Plantao(BaseTable):
    voluntario_id = ForeignKeyField(Voluntario)
    tipo = TextField (null=False)
    inicio = DateTimeField(null=False)
    pausa = DateTimeField(null=True)
    retorno = DateTimeField(null=True)
    fim = DateTimeField(null=True)
    comentario = TextField (null=True)