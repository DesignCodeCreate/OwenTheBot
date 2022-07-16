
import discord
from discord.ext import commands
from dislash import slash_command, Option, OptionType
from random import randint
import requests

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@slash_command(description = 'Rickroll')
	async def rickroll(self, ctx):
		await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
	
	@slash_command(description = "Spams the word you choose!", options = [Option("string", "Word", OptionType.STRING)])
	async def spam(self, ctx, string = "spam"):
		string1 = string
		for i in range(200):
			string = f"{string} {string1}"
		await ctx.send(string)
	
	@slash_command(description = 'Cat facts')
	async def catfact(self, ctx):
		cat = requests.get('https://some-random-api.ml/animal/cat').json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url = cat.get("image"))
		embed.add_field(name = "Cat Fact", value = cat.get("fact"))
		embed.set_footer(text = "Powered by Some Random API", icon_url = "https://i.some-random-api.ml/logo.png")
		await ctx.send(embed = embed)
	
	@slash_command(description = "Bad Memes")
	async def meme(self, ctx):
		meme = requests.get("https://some-random-api.ml/meme").json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url = meme.get("image"))
		embed.set_footer(text = meme.get("caption"))
		await ctx.send(embed = embed)

	@slash_command(description = "Mini emoji search", options = [
		Option("findemoji", "Emoji", OptionType.STRING, True),
		Option("emojibg", "Emoji", OptionType.STRING, True)
	])
	async def emojisearch(self, ctx, findemoji = "", emojibg = ""):
		spoiler1 = f"||{emojibg}||"
		spoiler2 = f"||{emojibg}||"
		rand = randint(0, 99)
		for i in range(rand):
			spoiler1 = f"{spoiler1}||{emojibg}||"
		for i in range(200 - rand):
			spoiler2 = f"{spoiler2}||{emojibg}||"
		
		await ctx.send(f"{spoiler1}||{findemoji}||{spoiler2}")



	@slash_command(description = "Get your info about your pokemon!", options = [Option("pokemon", "pokemon", OptionType.STRING)])
	async def pokedex(self, ctx, pokemon = "pikachu"):
		pokemons = requests.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon}").json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url = pokemons.get("sprites").get("animated"))
		embed.add_field(name = "Name", value = pokemons.get("name"))
		embed.add_field(name = "Type", value = pokemons.get("type"))
		embed.add_field(name = "Gender", value = pokemons.get("gender"))
		embed.add_field(name = "Health", value = pokemons.get("stats").get("hp"))
		embed.add_field(name = "Height", value = pokemons.get("height"))
		embed.add_field(name = "Evolution", value = pokemons.get("family").get("evolutionstage"))
		embed.add_field(name = "Info", value = pokemons.get("description"), inline = False)
		await ctx.send(embed = embed)

	