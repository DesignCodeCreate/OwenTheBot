import discord
from discord.ext import commands
from dislash import slash_command

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@slash_command(description = 'Invite To your Server!')
	async def invite(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Invite to Server", value = "[Invite Here](https://discord.com/api/oauth2/authorize?client_id=973939317900734555&permissions=139586948160&scope=applications.commands%20bot)")
		await ctx.send(embed = embed)
		
	@slash_command(description = "Shows who helped with the bots' creation!")
	async def credits(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Color.orange()
		
		embed.add_field(name = '@ninjadev64', value = 'He helped with the coding', inline = False)
		await ctx.send(embed = embed)
	
	@slash_command(description = "Gives a list of all the commands")
	async def help(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Color.orange()
	
		embed.add_field(name = "/rickroll", value = "Sends a rickroll link", inline = False)
		embed.add_field(name = "/invite", value = "Invite OwenTheBot to your server!")
		embed.add_field(name = "/math", value = "Does a math sum! To divide, use /, to multiply, use *, to add use +, to take away, use -", inline = False)
		embed.add_field(name = "/spam", value = "Owen the bot will Spam!", inline = False)
		embed.add_field(name = "/weather", value = "Checks the weather in hammersmith!", inline = False)
		embed.add_field(name = "/help", value = "Gets a list of commands", inline = False)
		embed.add_field(name = "/credits", value = "Show who helped with the bot", inline = False)
		embed.add_field(name = "/emojisearch", value = "play a find the input game!", inline = False)
		embed.add_field(name = "/catfact", value = "gets a fact about a cat", inline = False)
		embed.add_field(name = "/meme", value = "shows a funny meme", inline = False)
		await ctx.send(embed = embed)