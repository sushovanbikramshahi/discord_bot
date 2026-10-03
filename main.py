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

bot = commands.Bot(command_prefix='!', intents=intents)

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


#polling system (%poll "question")
class PollView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.votes = {}  # user id -> "like" or "dislike"

    def update_labels(self):
        likes = list(self.votes.values()).count("like")
        dislikes = list(self.votes.values()).count("dislike")
        self.like_button.label = f"👍 {likes}"
        self.dislike_button.label = f"👎 {dislikes}"

    @discord.ui.button(label="👍 0", style=discord.ButtonStyle.green)
    async def like_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.votes[interaction.user.id] = "like"
        self.update_labels()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="👎 0", style=discord.ButtonStyle.red)
    async def dislike_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.votes[interaction.user.id] = "dislike"
        self.update_labels()
        await interaction.response.edit_message(view=self)


@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question, color=discord.Color.gold())
    await ctx.send(embed=embed, view=PollView())


#making sound if important words are mentioned (!imp "message")
import asyncio 
SOUND_NAME = "airhorn"

@bot.command()
async def imp(ctx, *, message: str = None):
    if message is None:
        await ctx.send("Usage: `!imp your message`")
        return
    try:
        await ctx.message.delete() #delets the user massage so no redundancy

    except discord.Forbidden:
        pass  

    await ctx.send(f"📢 **IMPORTANT** from {ctx.author.mention}: {message}")

    channel = None
    if ctx.author.voice:
        channel = ctx.author.voice.channel
    else:
        for vc in ctx.guild.voice_channels:
            if any(not m.bot for m in vc.members):
                channel = vc
                break

    if channel is None:
        return

    if ctx.voice_client is None:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)

    try:
        all_sounds = await bot.fetch_soundboard_default_sounds()
        sound = discord.utils.get(all_sounds, name=SOUND_NAME)
        if sound:
            await channel.send_sound(sound)
            await asyncio.sleep(6)
        else:
            print(f"Sound '{SOUND_NAME}' not found")
    except Exception as e:
        print(f"Sound error: {e}")
    finally:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

#banning and kicking users
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked because: {reason}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned because: {reason}")

#warning system
warn_count = {}
Max_Warns = 3

@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx , member: discord.Member , * , reason=None):
    if member.bot and ctx.author.guild_permissions.administrator:
        await ctx.send("You cannot warn a bot.")
        return

    warn_count[member.id] = warn_count.get(member.id, 0) + 1
    await ctx.send(f"{member.mention} has been warned for: {reason}. Total warnings: {warn_count[member.id]}")


    if warn_count[member.id] >= Max_Warns:
        await member.kick(reason="Exceeded maximum warnings")
        await ctx.send(f"{member.mention} has been kicked for exceeding the maximum warnings.")
        warn_count[member.id] = 0  # Reset the warning count after kicking


@bot.command()
async def warncount(ctx , member: discord.Member):
    count = warn_count.get(member.id , 0)
    await ctx.send(f"{member.mention} has got {count} warnings out of {Max_Warns} warnings.")

@bot.command()
async def resetwarn(ctx , member: discord.Member):
    warn_count[member.id] = 0
    await ctx.send(f"{member.mention}'s warnings have been reset.")

bot.run(token,log_handler=handler, log_level=logging.DEBUG)



