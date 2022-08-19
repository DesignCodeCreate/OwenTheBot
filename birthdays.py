import discord
from discord.ext import commands, tasks
from discord.app_commands import command, describe
from datetime import datetime
from aiocsv import AsyncReader, AsyncWriter
import aiofiles

class Birthdays(commands.Cog):
	@tasks.loop(seconds = 86400) # seconds in the day
	async def perday(self):
		now = datetime.now()
		async with aiofiles.open(self.filepath, mode = "r") as f:
			async for row in AsyncReader(f):
				bd = datetime.fromisoformat(row[1])
				if (bd.day == now.day) and (bd.month == now.month):
					user = await self.bot.fetch_user(row[0])
					embed = discord.Embed()
					embed.color = discord.Colour.orange()
					embed.add_field(name = "Happy birthday!", value = "It's " + user.name + "'s birthday! 🥳")

					channel = await self.bot.fetch_channel(row[2])
					await channel.send(embed = embed)
	
	def __init__(self, bot):
		self.bot = bot
		self.filepath = "birthdays.csv"

	@command(description = "@OwenTheBot will wish you happy bday every year! (only do this once!).")
	@describe(date = "YYYY-MM-DD")
	async def inputbirthday(self, ctx, date: str):
		async with aiofiles.open(self.filepath, "a") as f:
			writer = AsyncWriter(f)
			await writer.writerow([ctx.user.id, date, ctx.channel.id])
		await ctx.response.send_message("Successfully added your birthday " + date + " to the list!")