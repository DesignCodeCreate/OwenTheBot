import typing
import discord
from discord.ext import commands
from discord.app_commands import command, describe
from discord.ui import View, Button
from discord import ButtonStyle	
import random

from os import environ
from requests import get

questions = {
    (0, "Where were the Olympics held in 2012?"): ((
		"Rio", "London", "Athens", "Tokyo"
	), 1),
	(1, "What does CPU stand for?"): ((
		"Command Processing Unit", "Cognitive Power and Understanding",
		"Connecting Programming Unit", "Central Processing Unit"
	), 3),
	(2, "Can Albatrosses sleep in mid-air?"): ((True, False), 0),
	(3, "What is the IMDb rating of the Bluey episode Sleepytime?"): ((7, 6, 10, 8), 2),
	(4, "What is the order of strings on a standardly tuned classical guitar?"): (("EADGBE", "EAGDBE", "EABDGE"), 0),
	(5, "How many years have the Olympics been going on for?"): ((3000, 200, 1500, 2800), 0),
	(6, "Which instrument is the smallest in an Orchestra?"): (("Violin", "Viola", "Picolo", "Flute"), 2),
	(7, "When did Windows 98 come out?"): ((1998, 1994, 1999, 2000), 1),
	(8, "What nut is marzipan made of?"): (("Almonds", "Macadamias", "Brazil Nuts", "Cashews"), 1),
	(9, "What colour is not in the Olympic Rings?"): (("Red", "Green", "Yellow", "Purple"), 3),
	(10, "How many digit values are used in hexadecimal?"): ((10, 16, 6, 2), 1),
	(11, "What do you use to convert human-readable code to machine code?"): (("Transpiler", "Compiler", "Translator"), 1)
}

button_colours = [
	ButtonStyle.red,
	ButtonStyle.grey,
	ButtonStyle.green,
	ButtonStyle.blurple
]

class DuplicateUserError(Exception):
	pass

class Game():
	def __init__(self, thread, p1, p2, p3, p4):
		self.thread = thread
		self.players = {
			p1: -1,
			p2: -1,
			p3: -1,
			p4: -1
		}
		self.points = {
			p1: 0,
			p2: 0,
			p3: 0,
			p4: 0
		}
		for p in self.players.keys():
			if list(self.players.keys()).count(p) > 1:
				raise DuplicateUserError
		self.questioncount = 0
		self.sent_questions = []

	def next(self):
		if self.questioncount == 10:
			return None
		for p in self.players.keys():
			self.players[p] = -1
		question, answer = random.choice(list(questions.items()))
		if question[0] in self.sent_questions:
			return self.next()
		self.questioncount+=1
		return [question, answer]

	def set_answer(self, user, answer: int):
		self.players[user] = answer

class GameButton(Button):
	def __init__(
		self, style: ButtonStyle, label: any, id: any,
		game: Game, cog, is_correct: bool, correct_answer: str
	):
		super().__init__(style = style, label = str(label), custom_id = str(id))
		self.id = id
		self.cog = cog
		self.game = game
		self.is_correct = is_correct
		self.correct_answer = correct_answer

	async def callback(self, ctx):
		if self.game.players.get(ctx.user) != -1: return
		if self.is_correct:
			self.game.set_answer(ctx.user, self.id)
			embed = discord.Embed(colour = discord.Colour.green())
			embed.add_field(name = "Correct answer!", value = f"The correct answer was {self.correct_answer}")

			answers = list(self.game.players.values())
			self.game.points[ctx.user]+=(answers.count(-1) + answers.count(-2))
		else:
			self.game.set_answer(ctx.user, -2)
			embed = discord.Embed(colour = discord.Colour.red())
			embed.add_field(name = "Incorrect!", value = "You'll get it next time!")
		await ctx.response.send_message(embed = embed, ephemeral = True)
		
		if not -1 in self.game.players.values():
			await self.cog.send_question(self.game)
		
class Quiz(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	async def send_question(self, game):
		q = game.next()
		if q is None:
			embed = discord.Embed()
			embed.colour = discord.Colour.orange()
			embed.add_field(name = "The game ended", value = """
   Good game!
   This thread will automatically archive in 1 hour.
	  		""")
			await game.thread.send(embed = embed)
			for user, value in game.points.values():
				get(f"https://fruitypointsapi.ninjadev64.repl.co/modify_points?key={environ['fruitykey']}&id={user.id}&amount={value}")
			return
			
		embed = discord.Embed(
			color = discord.Colour.orange(),
			title = f"Question {game.questioncount}",
			description = f"{q[0][1]}"
		)
		view = View()
		for index, answer in enumerate(q[1][0]):
			is_correct = q[1][1] == index
			view.add_item(GameButton(button_colours[index], answer, index, game, self, is_correct, q[1][0][q[1][1]]))
		
		await game.thread.send(embed = embed, view = view)

	@command(description = "Play a 4 Player Trivia Game!")
	@describe(p2 = "Player 2", p3 = "Player 3", p4 = "Player 4")
	async def quiz(
		self, ctx,
		p2: typing.Union[discord.User, discord.Member],
		p3: typing.Union[discord.User, discord.Member],
		p4: typing.Union[discord.User, discord.Member]
	):
		message = await ctx.response.send_message("""
  Welcome to the trivia! There are 10 questions.
  The first person to answer the question receives 3 points.
  The second person to answer receives 2 points, and the third person 1 point.
  Have fun!
		""")
		try:
			game = Game(await (await ctx.original_response()).create_thread(
				name = f"OwenTheBot Quiz with {ctx.user.name}, {p2.name}, {p3.name} and {p4.name}",
				reason = "OwenTheBot Quiz",
				auto_archive_duration = 60,
			), ctx.user, p2, p3, p4)
		except DuplicateUserError:
			await message.reply("Error: You cannot have a user in the game more than once!")
			return

		await self.send_question(game)