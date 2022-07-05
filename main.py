import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from dislash import InteractionClient

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
keep_alive.user = "{0.user}".format(bot)
hello_answers = ["Hello! :)", "Hi!", "What's up?", "Yo!"]

if os.environ["guilds"] == "ALL": client = InteractionClient(bot)
else:
	guilds = []
	for id in os.environ["guilds"].split(", "): guilds.append(int(id))
	client = InteractionClient(bot, test_guilds = guilds)

# import cogs (groups of commands)
from fun import Fun
from info import Info
from help import Help
from birthdays import Birthdays
bot.add_cog(Fun(bot))
bot.add_cog(Info(bot))
bot.add_cog(Help(bot))

birthdays = Birthdays(bot)
bot.add_cog(birthdays)

@bot.event
async def on_ready():
	print("I am now running as {0.user}! :)".format(bot))
	birthdays.perday.start()

keep_alive()
try: bot.run(os.environ["token"]) 
except discord.errors.HTTPException: os.system("kill 1")