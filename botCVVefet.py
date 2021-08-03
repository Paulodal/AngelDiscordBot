 # coding=utf-8

from os import error
from re import split
import discord
from discord.ext import commands, tasks
import datetime
from datetime import timedelta
import json
import pandas as pd
from pymongo import collection
from pymongo.message import insert, update
from pytz import HOUR, timezone, utc

def get_database():
	from pymongo import MongoClient
	fm = open('./mongostring.JSON')
	token = json.load(fm)
	CONNECTION_STRING = token
	client = MongoClient(CONNECTION_STRING)
	return client ['cvv_plantoes']

if __name__ == "__main__":
	CVV = get_database();

Client = discord.Client()
client = commands.Bot(command_prefix = ["!"], case_insensitive=True)
ft = open('./token.JSON')
token = json.load(ft)
bot_token = token

AVISO = "";

TextoAjuda = ("!" + "\nPara usar Angel você pode escrever:" + "\n " + "\n**Para Plantões**:" + "\n**!regular** para iniciar um plantão regular;" + "\n**!extra**, para iniciar um plantão extra;" + "\n**!reposição**, para iniciar um plantão de reposição;" + "\n**!substituindo [NOME] [NÚMERO CVV]** (por exemplo: !substituindo João 12345) para substituir outro voluntário" + "\n " + "\n**Durante o seu plantão**:" + "\n**!pausa** para iniciar sua pausa;" + "\n**!voltei** para voltar de sua pausa; e" + "\n**!terminei** para terminar seu plantão." + "\n " + "\n**E para eu lhe ajudar com outros assuntos**: " + "\n**!doação** para eu te ajudar a utilizar tempo de doações de outro voluntário" + "\n**!problema**, para eu te ajudar com problemas técnicos" + "\n**!falha** para eu te ajudar com falhas técnicas no sistema de ramais");

TextoFim = (", seu plantão terminou. Não se esqueça de preencher o seu **diário de plantão**. É bem rapidinho. Olha o link aqui: https://bit.ly/2Tr59q4 . Gratidão!" + "\n");

TextoDoacao = ("! Entendi que você está fazendo uma doação. Para isso, por favor preencha o diário de plantão, aqui: https://bit.ly/2Tr59q4 para **registrar os dados de sua doação**. Gratidão!");

TextoFalha = (". Entendi que você está com uma falha técnica no sistema de ramais. Vamos resolver! Em primeiro lugar, por favor, (1) abra um ticket com a TI aqui: https://cvv-virtual.tomticket.com/ e, depois, (2) preencha seu diário de plantão para avisar sobre essa **falha técnica**, aqui: https://bit.ly/2Tr59q4")

TextoProblema = (". Entendi que você está com problemas técnicos em seu computador. Por favor, preencha seu diário de plantão para avisar sobre esse **problema técnico** aqui: https://bit.ly/2Tr59q4 . Além disso, peço que você leia o Regimento interno (página 7) aqui: https://bit.ly/2SDslBD");

@client.event
async def on_ready():
	for guild in client.guilds:
		print ("O robô está conectado no servidor: {}".format(guild))
	print("------")


@client.command()
async def ajuda(ctx):
	await ctx.send("Oi, " + str(ctx.message.author.mention) + TextoAjuda)

@client.event
async def on_command_error(message, error):
    if isinstance(error, commands.CommandNotFound):
        await message.send("Desculpa, " + str(message.author.mention) + ". Não entendi seu comando... Se precisar da lista de comandos, por favor digite **!ajuda** :)")

@client.command()
async def regular(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "início regular",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S')
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + "! Seu plantão **regular** começou. Gratidão!")

@client.command()
async def extra(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "início extra",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S')
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + "! Seu plantão **extra** começou. Gratidão!")

@client.command()
async def reposição(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "início reposição",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S')
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send("Oi, " + str(ctx.message.author.name) + "! Seu plantão **de reposição** começou. Gratidão!")

@client.command()
async def pausa(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "início pausa",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S')
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send("Vamos começar sua pausa, " + str(ctx.message.author.name) + "! Lembre-se do limite de 10 minutos de pausa (para voluntários de 3h) e 5 minutos (para voluntários de 1h30min) :)")
	
@client.command()
async def voltei(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "fim pausa",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S')
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send("Ok, " + str(ctx.message.author.name) + ". Já anotei seu retorno.")
	
@client.command()
async def terminei(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	aviso = AVISO
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "fim de plantão",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S')
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send(str(ctx.message.author.name) + TextoFim + "\n" + aviso)
	
@client.command()
async def substituindo(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	nome_subs = str(ctx.message.content).strip("!substituindo ")
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "fim de plantão",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S'),
		'substituiu': nome_subs
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send(str(ctx.message.author.name) + ", entendi que você está substituindo " + nome_subs + " e estou anotando essa substituição. Gratidão!")

@client.command()
async def apoio(ctx):
	db = CVV["cvv_registros"]
	agora = datetime.datetime.now(timezone('America/Sao_Paulo'))
	nome = ctx.message.author.name
	software = str(ctx.message.content).strip("!substituindo ")
	registro = {
		'nome': nome,
		'hora_sistema': agora,
		'tipo': "fim de plantão",
		'dia': agora.strftime('%d/%m/%Y'),
		'hora': agora.strftime('%H:%M:%S'),
		'software': software
		}
	if isinstance(ctx.message.channel, discord.channel.DMChannel):
		await ctx.message.author.send(":octagonal_sign: Não posso registrar comandos por DM. Peço que registre seu comando no canal <#741743872060817440>. Gratidão! :octagonal_sign:")
	else:
		db.insert_one(registro)
		await ctx.message.author.send(str(ctx.message.author.name) + ", entendi que você está fazendo um apoio usando o software " + software + " e estou anotando esse apoio. Gratidão!")

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
	f = open('./admins.JSON', 'r+')
	data = json.load(f)
	if ctx.author.id in data:
		id = str(ctx.message.content).strip("!adicionaadmin ")
		id_int = int(id)
		data.append(id_int)
		with open('./admins.json', 'w') as output:
			json.dump(data, output)
		return await ctx.send(str(ctx.message.author.mention) + " Ok! Adicionei um admin")
	await ctx.send(str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para adicionar admins. Por favor contate a equipe de Desenvolvimento de TI");

@client.command()
async def alteraaviso(ctx):
	f = open('./admins.JSON', 'r+')
	data = json.load(f)
	if ctx.author.id in data:
		global AVISO 
		AVISO = str(ctx.message.content).strip("!alteraaviso ")
		return await ctx.send(str(ctx.message.author.mention) + " Ok! Adicionei um aviso para os voluntários quando eles terminarem seus plantões :)");
	await ctx.send(str(ctx.message.author.mention) + " Desculpe, mas você não tem autorização para mudar avisos no fim dos plantões. Por favor contate a equipe de Desenvolvimento de TI");


client.run(bot_token)