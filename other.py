import discord
from discord.ext import commands
from discord.app_commands import command, describe
from discord.ui import Button, View, Select
from discord import ButtonStyle	

class Other(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@command(description = "Invite OwenTheBot to your server!")
	async def invite(self, ctx):
		button = Button(label = "Invite", style = discord.ButtonStyle.url, url = "https://discord.com/api/oauth2/authorize?client_id=973939317900734555&permissions=139586948160&scope=applications.commands%20bot")
		view = View()
		view.add_item(button)
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Invite to server", value = "Click the button to invite!")
		await ctx.response.send_message(embed = embed, view = view)


	@command(description = "Shows who helped with the bots' creation!")
	async def credits(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Developers: ", value = "\u200b", inline = False)
		embed.add_field(name = "@DesigningCodingCreating", value = "The original developer, also made the bot's logo.", inline = False)
		embed.add_field(name = '@ninjadev64', value = 'Helped with lots of code.', inline = False)
		embed.add_field(name = "\u200b", value = "\u200b", inline = False)
		embed.add_field(name = "Random Ideas: ", value = "\u200b", inline = False)
		embed.add_field(name = "@Bananana03", value = "The Rickroll Command", inline = False)
		embed.add_field(name = "@snoppysnop", value = "Came up with the spam idea", inline = False)
		
		await ctx.response.send_message(embed = embed)