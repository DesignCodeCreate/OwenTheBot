import discord
from discord.ext import commands
from discord.app_commands import command, describe

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@command(description = 'Invite to your server!')
	async def invite(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.add_field(name = "Invite to Server", value = "[Invite here](https://discord.com/api/oauth2/authorize?client_id=973939317900734555&permissions=139586948160&scope=applications.commands%20bot)")
		await ctx.response.send_message(embed = embed)
		
	@command(description = "Shows who helped with the bots' creation!")
	async def credits(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Color.orange()
		embed.add_field(name = "Developers: ", value = "\u200b")
		embed.add_field(name = "@DesigningCodingCreating", value = "The original developer, also made the bot's logo.", inline = False)
		embed.add_field(name = '@ninjadev64', value = 'Helped with lots of code.', inline = False)
		embed.add_field(name = "\u200b", value = "\u200b", inline = False)
		embed.add_field(name = "Random Ideas: ", value = "\u200b")
		embed.add_field(name = "@Bananana03", value = "The Rickroll Command", inline = False)
		embed.add_field(name = "@Snoppysnop", value = "Came up with the spam idea")
		
		await ctx.response.send_message(embed = embed)

	@command(description = "Gives a list of all the commands")
	async def help(self, ctx):
		embed = discord.Embed()
		embed.colour = discord.Color.orange()
	
		embed.add_field(name = "/rickroll", value = "Sends a rickroll link", inline = False)
		embed.add_field(name = "/invite", value = "Invite OwenTheBot to your server!")
		embed.add_field(name = "/math", value = "Does a math sum! To divide use / and to multiply use *", inline = False)
		embed.add_field(name = "/spam", value = "OwenTheBot will spam!", inline = False)
		embed.add_field(name = "/weather", value = "Checks the weather in hammersmith!", inline = False)
		embed.add_field(name = "/help", value = "Gets a list of commands", inline = False)
		embed.add_field(name = "/credits", value = "Show who helped with the bot", inline = False)
		embed.add_field(name = "/emojisearch", value = "Play a find the input game!", inline = False)
		embed.add_field(name = "/catfact", value = "Gets a fact about a cat", inline = False)
		embed.add_field(name = "/meme", value = "Shows a funny meme", inline = False)
		embed.add_field(name = "/inputbirthday", value = "OwenTheBot will send you a happy birthday in the channel you ran the command.", inline = False)
		embed.add_field(name = "/pokedex", value = "Find out about your favourite pokemon!")
		embed.add_field(name = "/quiz", value = "Play a 4-player trivia game!")
		await ctx.response.send_message(embed = embed)