import datetime
from datetime import timedelta
from datetime import date, time
from schema_efetivos import db, Voluntario, Plantao
from pytz import HOUR, timezone, utc
import pandas as pd

tz = timezone('America/Sao_Paulo')

dia_sys = datetime.datetime.now(tz) - timedelta(hours=24)
ontem = dia_sys.strftime('%Y-%m-%d')
date_mask = '%Y-%m-%d'
time_mask = '%H:%M:%S'
sod = ' 00:00:00'
eod = ' 23:59:59'

nome = []
evento = []
dia = []
inicio = []
pausa = []
retorno = []
fim = []
comentario = []

plantoes = (Plantao.select(
            Voluntario.nome,
            Plantao.tipo,
            Plantao.inicio,
            Plantao.pausa,
            Plantao.retorno,
            Plantao.fim,
            Plantao.comentario,
        )
        .join(Voluntario, on=(Plantao.voluntario_id == Voluntario.id).alias('voluntario'))
        .where((Plantao.inicio >= ontem + sod) & (Plantao.inicio <= ontem + eod)))

for row in plantoes:
    # coloca no array plantoes pra buscar CADA NOME encontrado na DB
    nome.append(row.voluntario.nome)
    evento.append(row.tipo)
    dia.append(row.inicio.strftime(date_mask))
    inicio.append(row.inicio.strftime(time_mask))
    pausa.append(row.pausa.strftime(time_mask) if row.pausa != None else '')
    retorno.append(row.retorno.strftime(time_mask) if row.retorno != None else '')
    fim.append(row.fim.strftime(time_mask))
    comentario.append(row.comentario)

df = pd.DataFrame({
    'Nome': nome,
    'Evento': evento,
    'Dia': dia,
    'Inicio': inicio,
    'Pausa': pausa,
    'Retorno': retorno,
    'Fim': fim,
    'Comentário': comentario,
})

df.to_excel('./relatorios/Relatorio_Diario_Efetivos.xlsx', index_label=False, index=False, header=True)
