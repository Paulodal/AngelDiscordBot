from enum import unique
from peewee import AutoField, BaseTable, CharField, ForeignKeyField, PrimaryKeyField, SqliteDatabase, Model, TextField, DateField, IntegerField, TimeField

db = SqliteDatabase('registros_efetivos.db')

class BaseTable(Model):
    class Meta:
        database = db

class Voluntario(BaseTable):
    id = PrimaryKeyField(null=False, index=True)
    id_vol = TextField(null=False, index=True)
    nome = TextField(null=False, index=True)

class Plantao(BaseTable):
    id_vol = ForeignKeyField(Voluntario, backref='vol_id')
    tipo = TextField (null=False, index=True)
    dia = DateField(null=False, index=True)
    hora = TimeField(null=False, index=True)
    comentario = TextField (null=True, index=True)