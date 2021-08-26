from enum import unique
from peewee import AutoField, BaseTable, CharField, ForeignKeyField, PrimaryKeyField, SqliteDatabase, Model, TextField, DateField, IntegerField, TimeField

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
    dia = DateField(null=False)
    hora = TimeField(null=False)
    comentario = TextField (null=True)