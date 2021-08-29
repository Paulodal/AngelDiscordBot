import datetime
from datetime import timedelta
from datetime import date, time
from schema_efetivos import db, Voluntario, Plantao
from pytz import HOUR, timezone, utc
from peewee import *

tz = timezone('America/Sao_Paulo')
date_mask = '%Y-%m-%d'
sod = ' 00:00:00'
eod = ' 23:59:59'

hoje = datetime.datetime.now(tz).strftime(date_mask)
dia_sys = datetime.datetime.now(tz) - timedelta(hours=24)
ontem = dia_sys.strftime(date_mask)

try:
    plantao = (Plantao
            .select()
            .where(
                (Plantao.voluntario_id == 1) &
                (Plantao.inicio >= ontem + sod) &
                (Plantao.inicio <= hoje + eod)
            )
            .order_by(Plantao.inicio.desc())
            .get())
    print(plantao.inicio)
except Exception as e:
    print('Not found')


