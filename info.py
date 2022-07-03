import discord
from discord.ext import commands
from dislash import slash_command, Option, OptionType, OptionChoice
from os import environ
import requests

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.weatherkey = environ['weatherkey']

	@slash_command(
		description = "Does Math Sums",
		options = [
			Option("calculation", "Math calculation", OptionType.STRING, True),
			Option("secret", "Only sent to you", OptionType.BOOLEAN, False)
		]
	)
	async def math(self, ctx, calculation = "1+1", secret = False):
		embed = discord.Embed()
		embed.colour = discord.Color.orange()
		embed.add_field(name = (eval(calculation)), value = f'is the answer to {calculation}', inline = False)
		try: await ctx.send(embed = embed, ephemeral = secret)
		except (SyntaxError, NameError):
			await ctx.send("There was an error in your requested calculation. Please make sure you have used a valid mathematical expression and that multiplication is signified with an asterix (*).", ephemeral = True)
	
	@slash_command(
		options = [
			Option(
	            "option",
				description = "Checks the weather!",
	            type = OptionType.STRING,
	            required = True,
				choices = [
	                OptionChoice("Temperature", "temp"),
	                OptionChoice("Cloud Formation", "sky"),
	                OptionChoice("Humidity", "humidity"),
					OptionChoice("Wind", "wind")
	            ]
	        ),
			Option("city", "Choose City", OptionType.STRING, True)
	    ]	
	)
	async def weather(self, ctx, option: str, city = "London"):
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
			embed.add_field(name = "Wind Speed", value = str(weather.get("wind").get("speed")))
		else:
			embed.add_field(name = "Sorry, there is no such command")
			
		await ctx.send(embed = embed)