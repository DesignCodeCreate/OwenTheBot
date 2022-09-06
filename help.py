import discord
from discord.ext import commands
from discord.app_commands import command, describe
from discord.ui import Button, View, Select
from discord import ButtonStyle	

class HelpSelect(Select):
	def __init__(self):
		options=[
			discord.SelectOption(label = "Fun", emoji = "🎢"),
			discord.SelectOption(label = "Info", emoji = "📚"),
			discord.SelectOption(label = "Other", emoji = "🤓"),
			discord.SelectOption(label = "Points", emoji = "🪙")
		]
		super().__init__(custom_id = "help", placeholder = "Please select", min_values = 1, max_values = 1, options = options)
	
	async def callback(self, ctx):
		await ctx.response.send_message(embed = embeds[self.values[0]], ephemeral = True)

embeds = {}

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		for name, cog in self.bot.cogs.items():
			embed = discord.Embed(colour = discord.Colour.orange())
			for command in cog.get_app_commands():
				args = (' '.join([f'[{arg.name}]' for arg in command.parameters]) if hasattr(command, "parameters") else "")
				embed.add_field(name = f"/{command.name} {args}", value = command.description, inline = False)
			embeds[name] = embed
		
	@command(description = "Gives a list of all the commands")
	async def help(self, ctx):
		view = View()
		view.add_item(HelpSelect())
		await ctx.response.send_message(view = view)