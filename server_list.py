import typing
import discord
from discord.ui import View, Select
from discord.ext import commands
from discord.app_commands import command, describe, choices, Choice

class ServerList(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(description = f"Check the servers OwenTheBot is in!")
	async def server_list(self, ctx):
		select = Select(options=[
			discord.SelectOption(
				label = "Count", 
				emoji = "🔢",
				description = f"Display how many servers {self.bot.user.name} is in!"
			),
			
			discord.SelectOption(
				label = "Names", 
				emoji = "📙",
				description = f"See the servers you're in with {self.bot.user.name}"
			)
		])
		async def callback(interaction):
			if select.values[0] == "Names":
				names_list = [guild.name for guild in ctx.user.mutual_guilds]
				embed = discord.Embed(colour = discord.Colour.orange())
				embed.add_field(name = "Names", value = "\n".join(names_list))
				await interaction.response.send_message(embed = embed, ephemeral = True)
			elif select.values[0] == "Count":
				embed = discord.Embed(colour = discord.Colour.orange())
				embed.add_field(name = "Count", value = f"{self.bot.user} is in {len(self.bot.guilds)} servers!")
				await interaction.response.send_message(embed = embed)
				
		select.callback = callback
		view = View()
		view.add_item(select)

		await ctx.response.send_message(view = view)