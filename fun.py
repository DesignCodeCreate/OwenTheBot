import discord
from discord.ext import commands
from discord.app_commands import command, describe
from random import randint
import requests
from requests import get
from os import environ
import typing

from colorama import Fore

words = open("words.txt").read().splitlines()
all_words = open("all_words.txt").read().splitlines()

def is_valid_word(word):
	return word.lower() in all_words

channels = {}
answers = {}

game_end = {}
wurdle_guesses = {}
wurdle_embeds = {}
riddle_dict = {}

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(description = "Rickroll")
	async def rickroll(self, ctx):
		await ctx.response.send_message("https://www.youtube.com/watch?v=xvFZjo5PgG0")

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
		embed.set_image(url = cat.get("image"))
		embed.add_field(name = "Cat Fact", value = cat.get("fact"))
		embed.set_footer(
			text = "Powered by Some Random API",
			icon_url = "https://i.some-random-api.ml/logo.png",
		)
		await ctx.response.send_message(embed = embed)

	@command(description = "Bad memes")
	async def meme(self, ctx):
		meme = requests.get("https://some-random-api.ml/meme").json()
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_image(url = meme.get("image"))
		embed.set_footer(text = meme.get("caption"))
		await ctx.response.send_message(embed = embed)

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
	@describe(beta = "This is a beta command")
	async def wurdle(self, ctx, beta: typing.Optional[str]):
		channels[ctx.user.id] = ctx.channel.id
		game_end[ctx.user.id] = False
		answers[ctx.user.id] = words[randint(0, 2291)]
		wurdle_guesses[ctx.user.id] = []
		
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Wurdle", value = "\u200b")
		await ctx.response.send_message(embed = embed)
		wurdle_embeds[ctx.user.id] = await ctx.original_response()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user: return
		if channels.get(message.author.id) != message.channel.id: return
		if game_end.get(message.author.id) == True: return
		if message.content == answers.get(message.author.id):
			embed = discord.Embed()
			embed.colour = discord.Colour.orange()
			embed.add_field(name = "Well done!", value = f"You won {6-len(wurdle_guesses.get(message.author.id))} Fruity Points!")
			await message.reply(embed = embed, delete_after = 30)
			await message.delete()
			game_end[message.author.id] = True
			# implementing Fruity Points
			get(f"https://fruitypointsapi.ninjadev64.repl.co/modify_points?key={environ['fruitykey']}&id={message.author.id}&amount={6-len(wurdle_guesses.get(message.author.id))}")
		else:
			if message.content.lower() in all_words:
				wurdle_guesses.get(message.author.id).append(message.content.lower())
				embed = discord.Embed(color = discord.Colour.orange())	

				content = ""
				answer = answers.get(message.author.id)
				for guess in wurdle_guesses.get(message.author.id):
					for x, y in zip(answer, guess):
						if x == y:
							content+=f"{Fore.GREEN}{y}{Fore.RESET}" # green
						elif y in answer:
							content+=f"{Fore.YELLOW}{y}{Fore.RESET}" # yellow
						else:
							content+=y # normal
					content+="\n"
				
				embed.add_field(name = "Wurdle", value = f"""```ansi\n{content}\n```""")
				await wurdle_embeds.get(message.author.id).edit(embed = embed)
			else:
				embed = discord.Embed(color = discord.Colour.orange())
				embed.add_field(name = "Not valid", value = "Please enter a valid 5-letter word")
				await message.reply(embed = embed, delete_after = 5)
			await message.delete()

	@command(description = "Use this command to stop your Wurdle game.")
	async def wurdlestop(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "The game ended", value = f"The word was {answers.get(ctx.user.id)}")
		game_end[ctx.user.id] = True
		await ctx.response.send_message(embed = embed)
		
	@command(description = "Answer A random riddle!")
	async def riddle(self, ctx):
		json = requests.get("https://riddles-api.vercel.app/random").json()
		global riddle_ans
		riddle_ans = riddle_dict.get(ctx.user.id)
		riddle_dict[ctx.user.id] = json.get("answer")
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Riddle", value = json.get("riddle"))
		embed.add_field
		await ctx.response.send_message(embed = embed)
		
	@command(description = "Get the answer to your riddle!")
	async def riddle_answer(self, ctx):
		answer = riddle_dict.get(ctx.user.id)
		if answer is None:
			embed = discord.Embed()
			embed.colour = discord.Colour.orange()
			embed.add_field(name = "No command", value = "You didn't do a riddle!")
			await ctx.response.send_message(embed = embed, ephemeral = True)
			return
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Latest answer", value = f"The answer was {answer}!")
		await ctx.response.send_message(embed = embed)

	@command(description = "Get the number of pieces in a rubix cube.")
	async def cube(self, ctx, sides: int):
		x = sides * sides * sides - (sides - 2) * (sides - 2) * (sides - 2)
		embed = discord.Embed(
			colour = discord.Colour.orange()
		)
		embed.add_field(name = "Number of pieces", value = x)
		await ctx.response.send_message(embed = embed)