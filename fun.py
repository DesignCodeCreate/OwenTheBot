import discord
from discord.ext import commands
from discord.app_commands import command, describe
from random import randint
import requests

words = open("words.txt").read().splitlines()
all_words = open("all_words.txt").read().splitlines()


def is_valid_word(word):
	return word.lower() in all_words


answers = {}


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(description="Rickroll")
	async def rickroll(self, ctx):
		await ctx.response.send_message("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

	@command(description="Spams the word you choose!")
	async def spam(self, ctx, word: str = "spam"):
		string = word
		for i in range(200):
			string = f"{word} {string}"
		await ctx.response.send_message(string)

	@command(description="Cat facts")
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

	@command(description="Bad Memes")
	async def meme(self, ctx):
		meme = requests.get("https://some-random-api.ml/meme").json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url=meme.get("image"))
		embed.set_footer(text=meme.get("caption"))
		await ctx.response.send_message(embed=embed)

	@command(description="Mini emoji search")
	async def emojisearch(self, ctx, findemoji: str, emojibg: str):
		spoiler1 = f"||{emojibg}||"
		spoiler2 = f"||{emojibg}||"
		rand = randint(0, 99)
		for i in range(rand):
			spoiler1 = f"{spoiler1}||{emojibg}||"
		for i in range(200 - rand):
			spoiler2 = f"{spoiler2}||{emojibg}||"

		await ctx.response.send_message(f"{spoiler1}||{findemoji}||{spoiler2}")

	@command(description="Get your info about your pokemon!")
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

		await ctx.response.send_message(embed=embed)
		
'''@command(description="Play the Wordle game!")
	async def wordle(self, ctx):
		word = words[randint(0, 2291)]
		answers[ctx.author.id] = word
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name="word", value=word)
		await ctx.response.send_message(embed=embed)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.content == answers.get(message.author.id):
			await message.reply("That's the correct answer!")
			del answers[message.author.id]
		elif message.author != self.bot.id:
			await message.reply("Keep trying!", delete_after=5)
			await message.delete(delay=5)
'''