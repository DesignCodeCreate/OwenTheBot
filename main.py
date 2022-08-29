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
		fun = Fun(self)
		info = Info(self)
		quiz = Quiz(self)
		points = Points(self)
		self.birthdays = Birthdays(self)
		
		await self.add_cog(fun)
		await self.add_cog(info)
		await self.add_cog(quiz)
		await self.add_cog(points)
		await self.add_cog(self.birthdays)
		
		await self.add_cog(Help(self, fun, info, quiz, points, self.birthdays))
		await self.tree.sync()

bot = Bot(command_prefix = "!", intents = discord.Intents.all())

keep_alive.user = "{0.user}".format(bot)

@bot.event
async def on_ready():
	print("I am now running as {0.user}! :)".format(bot))
	if not bot.birthdays.perday.is_running():
		bot.birthdays.perday.start()

@bot.event
async def on_message(message):
	if message.author == bot.user: return
	if bot.user.mentioned_in(message) and message.channel.guild.me.guild_permissions.add_reactions:
		await message.add_reaction(get(bot.get_guild(979089805080137788).emojis, name = 'bot'))

keep_alive()
try: bot.run(os.environ["token"]) 
except discord.errors.HTTPException: os.system("kill 1")