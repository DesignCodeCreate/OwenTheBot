import discord
import os
from keep_alive import keep_alive
from discord.ext import commands, tasks
from discord.utils import get

# import cogs (groups of commands)
from fun import Fun
from info import Info
from help import Help
from quiz import Quiz
from birthdays import Birthdays
from points import Points
from other import Other
class Bot(commands.Bot):
	async def setup_hook(self):
		await self.add_cog(Fun(self))
		await self.add_cog(Other(self))
		await self.add_cog(Info(self))
		await self.add_cog(Quiz(self))
		await self.add_cog(Points(self))
		self.birthdays = Birthdays(self)
		await self.add_cog(self.birthdays)
		
		await self.add_cog(Help(self))
		await self.tree.sync()

bot = Bot(command_prefix = "!", intents = discord.Intents.all())

@tasks.loop(seconds = 600)
async def update_status():
	await bot.change_presence(activity = discord.Streaming(
		name = f"/help! ¦ {len(bot.guilds)} servers",
		url = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
	))

@bot.event
async def on_ready():
	print(f"I am now running as {bot.user} in {len(bot.guilds)} servers! :)\n")
	for count, guild in enumerate(bot.guilds, start = 1):
		print(count, guild.name)
	if not bot.birthdays.perday.is_running():
		bot.birthdays.perday.start()
	update_status.start()

@bot.event
async def on_message(message):
	if message.author == bot.user: return
	if bot.user.mentioned_in(message) and message.channel.guild.me.guild_permissions.add_reactions:
		await message.add_reaction(get(bot.get_guild(979089805080137788).emojis, name = 'bot'))

keep_alive()
try: bot.run(os.environ["token"]) 
except discord.errors.HTTPException: os.system("kill 1")