import datetime
from datetime import timedelta
from datetime import date, time
from schema_efetivos import db, Voluntario, Plantao
from pytz import HOUR, timezone, utc

tz = timezone('America/Sao_Paulo')

hoje = datetime.datetime.now(tz).strftime('%Y-%m-%d')

nome = []
evento = []
hora = []
comentario = []
dia = []

plantoes = (Plantao.select(
        Voluntario.nome,
        Plantao.tipo,
        Plantao.hora,
        Plantao.dia
    ).join(Voluntario, on=(Plantao.voluntario_id == Voluntario.id).alias('voluntario')).where(Plantao.dia == hoje))

print(plantoes)

for row in plantoes:
    print(row.voluntario.nome, row.tipo, row.hora, row.dia)