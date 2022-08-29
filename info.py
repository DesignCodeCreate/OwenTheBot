import typing
import discord
from discord.ext import commands
from discord.app_commands import command, describe, choices, Choice
from os import environ
import requests

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.weatherkey = environ['weatherkey']

	@command(description = "Does maths")
	@describe(calculation = "Math calculation", secret = "Only sent to you")
	async def math(self, ctx, calculation: str = "1+1", secret: typing.Optional[bool] = False):
		embed = discord.Embed()
		embed.colour = discord.Color.orange()
		embed.add_field(name = (eval(calculation)), value = f'is the answer to {calculation}', inline = False)
		try: await ctx.response.send_message(embed = embed, ephemeral = secret)
		except (SyntaxError, NameError):
			await ctx.response.send_message("There was an error in your requested calculation. Please make sure you have used a valid mathematical expression and that multiplication is signified with an asterix (*).", ephemeral = True)
	
	@command(description = "Checks the weather!")
	@choices(
		option = [
			Choice(name = "Temperature", value = "temp"),
		    Choice(name = "Cloud Formation", value = "sky"),
		    Choice(name = "Humidity", value = "humidity"),
			Choice(name = "Wind", value = "wind")
		]
	)
	async def weather(self, ctx, option: str, city: str = "London"):
		geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.weatherkey}").json()
	
		weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={geo[0].get('lat')}&lon={geo[0].get('lon')}&appid={self.weatherkey}&units=metric").json()
		icon = "http://openweathermap.org/img/wn/" + weather.get("weather")[0].get("icon") + "@2x.png"
		
		embed = discord.Embed()
		embed.colour = discord.Colour.orange()
		embed.set_thumbnail(url = icon)
		embed.set_footer(text = f"Weather in {city}")
		
		if option == "temp":
			embed.add_field(name = "Current temperature", value = str(weather.get("main").get("temp")) + "°C")
		elif option == "sky":
			embed.add_field(name = "Sky", value = str(weather.get("weather")[0].get("description")))
		elif option == "humidity":
			embed.add_field(name = "Humidity", value = str(weather.get("main").get("humidity")) + "%")
		elif option == "wind":
			embed.add_field(name = "Wind speed", value = str(weather.get("wind").get("speed")))
		else:
			embed.add_field(name = f"Sorry, there is no such option {option}")
			
		await ctx.response.send_message(embed = embed)