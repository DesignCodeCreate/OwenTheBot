import discord
from discord.ext import commands
from discord.app_commands import command, describe
from random import randint
import requests
from requests import get
from os import environ

words = open("words.txt").read().splitlines()
all_words = open("all_words.txt").read().splitlines()

def is_valid_word(word):
	return word.lower() in all_words

channels = {}
game_end = {}
word_dict = {}

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(description = "Rickroll")
	async def rickroll(self, ctx):
		await ctx.response.send_message("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

	@command(description = "Spams the word you choose!")
	async def spam(self, ctx, word: str = "spam"):
		string = word
		for i in range(200):
			string = f"{word} {string}"
		await ctx.response.send_message(string)

	@command(description = "Cat facts")
	async def catfact(self, ctx):
		cat = requests.get("https://some-random-api.ml/animal/cat").json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url=cat.get("image"))
		embed.add_field(name="Cat Fact", value=cat.get("fact"))
		embed.set_footer(
			text="Powered by Some Random API",
			icon_url="https://i.some-random-api.ml/logo.png",
		)
		await ctx.response.send_message(embed=embed)

	@command(description = "Bad memes")
	async def meme(self, ctx):
		meme = requests.get("https://some-random-api.ml/meme").json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url=meme.get("image"))
		embed.set_footer(text=meme.get("caption"))
		await ctx.response.send_message(embed=embed)

	@command(description = "Mini emoji search")
	async def emojisearch(self, ctx, findemoji: str, emojibg: str):
		spoiler1 = f"||{emojibg}||"
		spoiler2 = f"||{emojibg}||"
		rand = randint(0, 99)
		for i in range(rand):
			spoiler1 = f"{spoiler1}||{emojibg}||"
		for i in range(200 - rand):
			spoiler2 = f"{spoiler2}||{emojibg}||"

		await ctx.response.send_message(f"{spoiler1}||{findemoji}||{spoiler2}")

	@command(description = "Get info about your pokemon!")
	async def pokedex(self, ctx, pokemon: str):
		pokemons = requests.get(f"https://some-random-api.ml/pokedex?pokemon={pokemon.title()}").json()
		
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()

		embed.set_image(url=pokemons.get("sprites").get("animated"))
		embed.set_author(name=pokemons.get("name"))
		embed.add_field(name="Name", value=pokemons.get("name"))
		embed.add_field(name="Type", value=pokemons.get("type")[0])
		embed.add_field(name="Gender", value=", ".join(pokemons.get("gender")))
		embed.add_field(name="Health", value=pokemons.get("stats").get("hp"))
		embed.add_field(name="Height", value=pokemons.get("height"))
		embed.add_field(name="Weight", value=pokemons.get("weight"))
		embed.add_field(
			name="Evolution Line",
			value=", ".join(pokemons.get("family").get("evolutionLine")),
			inline=True,
		)
		embed.add_field(name="Evolution Stage", value=pokemons.get("family").get("evolutionStage"))
		embed.add_field(name="Info", value=pokemons.get("description"), inline=False)

		await ctx.response.send_message(embed = embed)
		
	@command(description = "Play the Wurdle game!")
	async def wurdle(self, ctx):
		channels[ctx.user.id] = ctx.channel.id
		game_end[ctx.user.id] = False
		word_dict[ctx.user.id] = words[randint(0, 2291)]
		
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Word", value = word_dict[ctx.user.id])
		await ctx.response.send_message(embed = embed)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user: return
		if channels.get(message.author.id) != message.channel.id: return
		if game_end.get(message.author.id) == True: return
		if message.content == word_dict.get(message.author.id):
			embed = discord.Embed()
			embed.colour = discord.Colour.orange()
			embed.add_field(name = "Well done!", value = "You won 10 Fruity Points!")
			await message.reply(embed = embed, delete_after = 30)
			await message.delete()
			game_end[message.author.id] = True
			user = message.author.id
			# implementing Fruity Points
			get(f"https://fruitypointsapi.ninjadev64.repl.co/modify_points?key={environ['fruitykey']}&id={user}&amount=10")
		else:
			await message.reply("""
   You're not quite there yet. Keep trying!
   Remember, you can use /wurdlestop to end the game!""",
				delete_after = 2
			)
			await message.delete()

	@command(description = "Use this command to stop your Wurdle game.")
	async def wurdlestop(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "The game ended", value = "Good try!")
		game_end[ctx.user.id] = True
		await ctx.response.send_message(embed = embed)