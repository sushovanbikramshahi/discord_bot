import discord
from discord.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(name = "server_info")
    @commands.guild_only()
    async def server_info(self,ctx):
        guild = ctx.guild
        embed = discord.Embed(title=guild.name, color=discord.Color.blue())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        owner = guild.owner.mention if guild.owner else "Unknown"
        embed.add_field(name="Owner", value=owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Created", value=guild.created_at.strftime("%d %b %Y"))
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.set_footer(text=f"Server ID: {guild.id}")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerInfo(bot))