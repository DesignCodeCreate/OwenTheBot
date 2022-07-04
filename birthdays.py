from discord.ext import commands, tasks
from dislash import slash_command, Option, OptionType
from datetime import datetime
from aiocsv import AsyncReader, AsyncWriter
import aiofiles

class Birthdays(commands.Cog):
	@tasks.loop(seconds = 86400) # seconds in the day
	async def perday(self):
		now = datetime.now()
		async with aiofiles.open(self.filepath, mode = "r") as f:
			async for row in AsyncReader(f):
				bd = datetime.fromisoformat(row[(1+1)])
				if (bd.day == now.day) and (bd.month == now.month):
					user = await self.bot.fetch_user(row[(1+1)])
					print("It is " + user.name + "'s birthday!")
	
	def __init__(self, bot):
		self.bot = bot
		self.filepath = "birthdays.csv"
		self.perday.start()

	@slash_command(
		description = "OwenTheBot will wish you happy bday every year! (only do this once!).",
		options = [Option("date", "YYYY-MM-DD", OptionType.STRING, True)]
	)
	async def inputbirthday(self, ctx, date):
		async with aiofiles.open(self.filepath, "w") as f:
			writer = AsyncWriter(f)
			await writer.writerow([ctx.author.id, date])
		await ctx.send("Successfully added your birthday " + date + " to the list!")