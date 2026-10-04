import discord
from discord.ext import commands
import requests

weather_api = "https://api.open-meteo.com/v1/forecast?"
latitude = 28.2096 # default of Pokhara
longitude = 83.9856

class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("weather online!")

    @commands.command()
    async def current_weather(self,ctx):
        await ctx.send("wait for api to send back data", delete_after=5.0)
        url = f"{weather_api}latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        data = response.json()
        print(data)
        await ctx.send(
            f'''
            Current temp = {data["current_weather"]["temperature"]}
Current windspeed = {data["current_weather"]["windspeed"]}
            '''
        )

async def setup(bot):
    await bot.add_cog(weather(bot))