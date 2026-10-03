import discord
from discord.ext import commands
import logging

from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv('DISCORD_KEY')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='%', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')


@bot.event
async def on_member_join(member):
    print(f'Welcome idiot {member.name}!')




#filtering the words
BANNED_WORDS = ["shit", "fuck", "bitch"]  # add your own curse 

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    content = message.content.lower()
    if any(word in content for word in BANNED_WORDS):
        await message.delete()
        await message.channel.send(
            f"{message.author.mention}, PLZ be more civilized",
            delete_after=5  # warning removes itself after 5 seconds
        )
        return

    await bot.process_commands(message)


#just checking if the bot responses
@bot.command()
async def hello(ctx):
    await ctx.send(f'hi {ctx.author.mention}')


#role assignment and removal    (&assign @user @role) (&remove @user @role)
@bot.command()
async def assign(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{member.mention} got the {role.name} role!")

@bot.command()
async def remove(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} lost the {role.name} role!")

bot.run(token,log_handler=handler, log_level=logging.DEBUG)



