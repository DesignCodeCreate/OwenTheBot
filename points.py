import discord
import typing
from discord.app_commands import command, describe
from discord.ext import commands
import requests

class Points(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.fruitypointsapi = "https://fruitypointsapi.ninjadev64.repl.co/"
		self.get_api = "get_points"
		self.modify_api = "modify_points"
		self.leaderboard = "leaderboard"
		
	@command(description = "Check how many points someone has on the Fruity Points Index!")
	async def points(self, ctx,
		user: typing.Optional[typing.Union[discord.User, discord.Member]]
	):
		user = user or ctx.user
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(
			name = "Points",
			value = f"{ctx.user} has " + str(requests.get(f"{self.fruitypointsapi}{self.get_api}?id={user.id}").json().get("points")) + " points."
		)
		await ctx.response.send_message(embed = embed)

	@command(description = "Check the leaderboard for the Fruity Points Index!")
	async def leaderboard(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		users = requests.get(f"{self.fruitypointsapi}{self.leaderboard}").json().get("leaderboard")
		place = 0
		string = ""
		for user in users:
			place+=1
			string+=f"{place}. {await self.bot.fetch_user(user.get('id'))}: {user.get('points')}\n"
		
		embed.add_field(name = "Leaderboard", value = string, inline = False)
		await ctx.response.send_message(embed = embed)