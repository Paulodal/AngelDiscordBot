 # coding=utf-8

from os import error
import discord
from peewee import *
from discord.ext import commands, tasks
import datetime
from datetime import timedelta
from datetime import date, time
import json
import pandas as pd
# import smtplib
# import mimetypes
from email.message import EmailMessage
from pytz import HOUR, timezone, utc
from schema_efetivos import db, Voluntario, Plantao

Client = discord.Client()
client = commands.Bot(command_prefix = ["!"], case_insensitive=True)
ft = open('./token_efet.JSON')
token = json.load(ft)
bot_token = token

# Criando as tabelas de Sqlite
db.create_tables([Voluntario])
db.create_tables([Plantao])

## A partir daqui, o bot está apenas mostrando que está conectado com uma mensagem printada diretamente no terminal.

AVISO = ""; # esse aviso é alterado com o comando "!alteraaviso", e apenas admins podem usar esse comando

TextoAjuda = ("!"
			"\nPara usar Angel você pode escrever:\n"
			"\n**Para Plantões**:"
			"\n**!regular** para iniciar um plantão regular;"
			"\n**!extra**, para iniciar um plantão extra;"
			"\n**!reposição**, para iniciar um plantão de reposição;"
			"\n**!substituindo [NOME] [NÚMERO CVV]** (por exemplo: !substituindo João 12345) para substituir outro voluntário\n"
			"\n**Durante o seu plantão**:"
			"\n**!pausa** para iniciar sua pausa;"
			"\n**!voltei** para voltar de sua pausa; e"
			"\n**!terminei** para terminar seu plantão.\n"
			"\n**E para eu lhe ajudar com outros assuntos**: "
			"\n**!doação** para eu te ajudar a utilizar tempo de doações de outro voluntário"
			"\n**!problema**, para eu te ajudar com problemas técnicos"
			"\n**!falha** para eu te ajudar com falhas técnicas no sistema de ramais");

TextoFim = (", seu plantão terminou. Não se esqueça de preencher o seu **diário de plantão**. É bem rapidinho. "
			"Olha o link aqui: https://bit.ly/2Tr59q4 . Gratidão!\n\n");

TextoDoacao = ("! Entendi que você está fazendo uma doação. "
			"Para isso, por favor preencha o diário de plantão, aqui: https://bit.ly/2Tr59q4 "
			"para **registrar os dados de sua doação**. Gratidão!");

TextoFalha = (". Entendi que você está com uma falha técnica no sistema de ramais. Vamos resolver! "
			"Em primeiro lugar, por favor, "
			"(1) abra um ticket com a TI aqui: https://cvv-virtual.tomticket.com/ e, depois, "
			"(2) preencha seu diário de plantão para avisar sobre essa **falha técnica**, aqui: https://bit.ly/2Tr59q4")

TextoProblema = (". Entendi que você está com problemas técnicos em seu computador. "
			"Por favor, preencha seu diário de plantão para avisar sobre esse **problema técnico** aqui: https://bit.ly/2Tr59q4 . "
			"Além disso, peço que você leia o Regimento interno (página 7) aqui: https://bit.ly/2SDslBD");

TextoNoDM = (":octagonal_sign: Não posso registrar comandos por DM. "
			"Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")

tz = timezone('America/Sao_Paulo')


def busca_voluntario(ctx):
	discord_id = ctx.message.author.id

	try:
		voluntario = Voluntario.get(Voluntario.discord_id == discord_id)
	except Exception as e:
		voluntario = Voluntario.create(
		discord_id = discord_id,
		nome = ctx.message.author.display_name)

	return voluntario


def is_admin(ctx):
	f = open('./admins.JSON', 'r+')
	data = json.load(f)
	if ctx.author.id in data:
		return True
	else:
		return False


@client.event
async def on_ready():
	for guild in client.guilds:
		print ("O robô está conectado no servidor: {}".format(guild))
	print("------")


## A partir daqui, o Bot está ouvindo comandos e adicionando os dados no dataframe que foi criado lá em cima.
## NOTA: alguns comandos estão repetidos para facilitar o envio de comandos pelos voluntários. Um exemplo é o comando "ajuda" e "Ajuda". Basta alterar um e copiar integralmente a alteração para o mesmo.


@client.command()
async def ajuda(ctx):
	await ctx.send("Oi, " + str(ctx.message.author.mention) + TextoAjuda)


@client.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandNotFound):
        await message.send("Desculpa, " + str(message.author.mention) + ". Não entendi seu comando... Se precisar da lista de comandos, por favor digite **!ajuda** :)")


@client.command()
async def regular(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz) #fixed a bug
	discord_id = ctx.message.author.id

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'inicio regular',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
	)

	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + "! Seu plantão **regular** começou. Gratidão!")


@client.command()
async def extra(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz) #fixed a bug

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'inicio extra',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
	)

	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + "! Seu plantão **extra** começou. Gratidão!")


@client.command()
async def reposição(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz)

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'inicio reposição',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
	)

	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + "! Seu plantão **de reposição** começou. Gratidão!")


@client.command()
async def pausa(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz)

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'inicio pausa',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
	)

	await ctx.message.author.send("Vamos começar sua pausa, " + str(ctx.message.author.name) + "! Lembre-se do limite de 10 minutos de pausa (para voluntários de 3h) e 5 minutos (para voluntários de 1h30min) :)")


@client.command()
async def voltei(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz)

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'retorno pausa',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
	)

	await ctx.message.author.send("Ok, " + str(ctx.message.author.name) + ". Já anotei seu retorno.")


@client.command()
async def terminei(ctx):
	global tz, AVISO
	hour_sys = datetime.datetime.now(tz)

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'fim de plantão',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
	)

	await ctx.message.author.send(str(ctx.message.author.name) + TextoFim + "\n" + AVISO)


@client.command()
async def substituindo(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz)
	nome_subs = str(ctx.message.content).strip("!substituindo ")

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'inicio substituicao',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
		comentario = nome_subs
	)

	await ctx.message.author.send(
		str(ctx.message.author.name) + ", entendi que você está substituindo " +
		nome_subs + " e estou anotando essa substituição. Gratidão!")


@client.command()
async def apoio(ctx):
	global tz
	hour_sys = datetime.datetime.now(tz)
	software = str(ctx.message.content).strip("!substituindo ")

	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(TextoNoDM)
		return

	voluntario = busca_voluntario(ctx)

	Plantao.create(
		voluntario_id = voluntario.id,
		tipo = 'retorno pausa',
		dia = hour_sys.strftime('%Y-%m-%d'),
		hora = hour_sys.strftime("%H:%M:%S"),
		comentario = software
	)

	await ctx.message.author.send(
		str(ctx.message.author.name) + ", entendi que você está fazendo um apoio usando o software " +
		software + " e estou anotando esse apoio. Gratidão!")


@client.command()
async def doação(ctx):
	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + TextoDoacao)
@client.command()
async def doacão(ctx):
	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + TextoDoacao)
@client.command()
async def doaçao(ctx):
	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + TextoDoacao)
@client.command()
async def doacao(ctx):
	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + TextoDoacao)


@client.command()
async def falha(ctx):
	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + TextoFalha)


@client.command()
async def Problema(ctx):
	await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + TextoProblema)


@client.command()
async def adicionaadmin(ctx):
	if not is_admin(ctx):
		await ctx.send(
			str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para adicionar admins. " +
			"Por favor contate a equipe de Desenvolvimento de TI")
		return

	f = open('./admins.JSON', 'r+')
	data = json.load(f)
	data.append(int(str(ctx.message.content).strip("!adicionaadmin ")))
	with open('./admins.json', 'w') as output:
		json.dump(data, output)
	return await ctx.send(str(ctx.message.author.mention) + " Ok! Adicionei um admin")


@client.command()
async def alteraaviso(ctx):
	if not is_admin(ctx):
		await ctx.send(
			str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para mudar avisos no fim dos plantões. " +
			"Por favor contate a equipe de Desenvolvimento de TI");
		return

	global AVISO
	AVISO = str(ctx.message.content).strip("!alteraaviso ")
	return await ctx.send(str(ctx.message.author.mention) + " Ok! Adicionei um aviso para os voluntários quando eles terminarem seus plantões :)");


@client.command()
async def RelatorioHoje(ctx):
	global tz

	if not is_admin(ctx):
		await ctx.send(
			str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para solicitar relatórios. " +
			"Por favor contate a equipe de Desenvolvimento de TI")
		return

	hoje = datetime.datetime.now(tz).strftime('%Y-%m-%d')

	nome = []
	evento = []
	hora = []
	comentario = []
	dia = []

	plantoes = Plantao.select(
			Voluntario.nome,
			Plantao.tipo,
			Plantao.hora,
			Plantao.dia
		).join(Voluntario, on=(Plantao.voluntario_id == Voluntario.id).alias('voluntario')).where(Plantao.dia == hoje)

	for row in plantoes:
		# coloca no array plantoes pra buscar CADA NOME encontrado na DB
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
	file = discord.File('./relatorios/Relatorio_Diario_Efetivos.xlsx')

	await ctx.message.author.send(str(ctx.message.author.mention) + ": aqui está o relatório de plantões diário")
	await ctx.message.author.send(file=file)


@client.command()
async def RelatorioOntem(ctx):
	global tz

	if not is_admin(ctx):
		await ctx.send(
			str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para solicitar relatórios. " +
			"Por favor contate a equipe de Desenvolvimento de TI")
		return

	dia_sys = datetime.datetime.now(tz) - timedelta(hours=24)
	ontem = dia_sys.strftime('%Y-%m-%d')

	nome = []
	evento = []
	hora = []
	comentario = []
	dia = []

	plantoes = Plantao.select(
			Voluntario.nome,
			Plantao.tipo,
			Plantao.hora,
			Plantao.dia
		).join(Voluntario, on=(Plantao.voluntario_id == Voluntario.id).alias('voluntario')).where(Plantao.dia == ontem)

	for row in plantoes:
		# coloca no array plantoes pra buscar CADA NOME encontrado na DB
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

	df.to_excel('./relatorios/Relatorio_Ontem_Efetivos.xlsx', index_label=False, index=False, header=True)
	file = discord.File('./relatorios/Relatorio_Ontem_Efetivos.xlsx')

	await ctx.message.author.send(str(ctx.message.author.mention) + ": aqui está o relatório de plantões de **ontem**!")
	await ctx.message.author.send(file=file)


@client.command()
async def RelatorioSemanal(ctx):
	global tz

	if not is_admin(ctx):
		await ctx.send(
			str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para solicitar relatórios. " +
			"Por favor contate a equipe de Desenvolvimento de TI")
		return

	semana_sys = datetime.datetime.now(timezone('America/Sao_Paulo')) - timedelta(days=7)
	semana = semana_sys.strftime('%Y-%m-%d')

	nome = []
	evento = []
	hora = []
	comentario = []
	dia = []

	plantoes = Plantao.select(
			Voluntario.nome,
			Plantao.tipo,
			Plantao.hora,
			Plantao.dia
		).join(Voluntario, on=(Plantao.voluntario_id == Voluntario.id).alias('voluntario')).where(Plantao.dia > semana)

	for row in plantoes:
		# coloca no array plantoes pra buscar CADA NOME encontrado na DB
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

	df.to_excel('./relatorios/Relatorio_Semanal_Efetivos.xlsx', index_label=False, index=False, header=True)
	file = discord.File('./relatorios/Relatorio_Semanal_Efetivos.xlsx')

	await ctx.message.author.send(str(ctx.message.author.mention) + ": aqui está o relatório de plantões semanal!")
	await ctx.message.author.send(file=file)

client.run(bot_token)