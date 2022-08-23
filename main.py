import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from discord.utils import get

# import cogs (groups of commands)
from fun import Fun
from info import Info
from help import Help
from quiz import Quiz
from birthdays import Birthdays
from points import Points

class Bot(commands.Bot):
	async def setup_hook(self):
		await self.add_cog(Fun(self))
		await self.add_cog(Info(self))
		await self.add_cog(Help(self))
		await self.add_cog(Quiz(self))
		await self.add_cog(Points(self))
		self.birthday_cog = Birthdays(self)
		await self.add_cog(self.birthday_cog)
		await self.tree.sync()

bot = Bot(command_prefix = "!", intents = discord.Intents.all())

keep_alive.user = "{0.user}".format(bot)

@bot.event
async def on_ready():
	print("I am now running as {0.user}! :)".format(bot))
	bot.birthday_cog.perday.start()

@bot.event
async def on_message(message):
	if message.author == bot.user: return
	if bot.user.mentioned_in(message) and message.channel.guild.me.guild_permissions.add_reactions:
		await message.add_reaction(get(bot.get_guild(979089805080137788).emojis, name = 'bot'))

keep_alive()
try: bot.run(os.environ["token"]) 
except discord.errors.HTTPException: os.system("kill 1")