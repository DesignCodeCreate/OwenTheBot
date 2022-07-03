import discord
import os
import random
from keep_alive import keep_alive
from discord.ext import commands
from dislash import InteractionClient

bot = commands.Bot(command_prefix = "!")
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
bot.add_cog(Fun(bot))
bot.add_cog(Info(bot))
bot.add_cog(Help(bot))

@client.event
async def on_message(message):
	if message.author == bot.user: return
	if not bot.user.mentioned_in(message): return
	
	if ("hello" in message.content.lower() or
		"hi" in message.content.lower() or
		"yo" in message.content.lower()):
		await message.reply(random.choice(hello_answers))
	if ("you're cool" in message.content.lower() or
		"smart" in message.content.lower()):
		await message.reply('Thanks! I appreciate the feedback')

@bot.event
async def on_ready():
	print("I am now running as {0.user}! :)".format(bot))

keep_alive()
try: bot.run(os.environ["token"]) 
except discord.errors.HTTPException: os.system("kill 1")