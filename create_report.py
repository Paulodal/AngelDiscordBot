import datetime
from datetime import timedelta
from datetime import date, time
from schema_efetivos import db, Voluntario, Plantao
from pytz import HOUR, timezone, utc
import pandas as pd

tz = timezone('America/Sao_Paulo')

dia_sys = datetime.datetime.now(tz) - timedelta(hours=24)
ontem = dia_sys.strftime('%Y-%m-%d')

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
    ).join(Voluntario, on=(Plantao.voluntario_id == Voluntario.id).alias('voluntario')).where(Plantao.dia == ontem))

print(plantoes)

for row in plantoes:
    print(row.voluntario.nome, row.tipo, row.hora, row.dia)
    nome.append(row.voluntario.nome)
    evento.append(row.tipo)
    hora.append(row.hora)
    comentario.append(row.comentario)
    dia.append(row.dia)

df = pd.DataFrame({
    'Nome':nome,
    'Evento':evento,
    'Hora':hora,
    'Comentário':comentario,
    'Dia':dia
})

df.to_excel('./relatorios/Relatorio_Diario_Efetivos.xlsx', index_label=False, index=False, header=True)
