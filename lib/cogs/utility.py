import discord
import asyncio
import urllib
import json
from datetime import *
from discord.ext.commands import Cog
from discord.ext.commands import *
from discord.ext.commands.cooldowns import *
from discord.ext import commands
from discord.ext import tasks
from lib.bot.__init__ import bcolors
from lib.bot.__init__ import print_info, print_spec, print_cog, print_scheduler, print_warn

# -------------------------------------------------------------------------------------------------------------------------------
help_utility = """
                `?!remind` - Set a reminder for anything, for a duration of 5 minutes to 7 days! Cooldown of 1 use every 5 minutes.\n
                `?!mcserver` - Check the status of any Minecraft server by simply specifying the IP after the command! Cooldown of one use every 10 seconds.\n
                `?!ping` - Get the bot's latency.\n
                `?!github` - Send a link to my GitHub page.\n
"""
help_fun = """
            `?!bonk` - 'Hit' another member for a specified reason with random objects!\n
            `?!8ball` - Give a question and the 8-ball will answer!\n
            `?!soup` - Get your fresh soup here!\n
            `?!quote` - Get a random inspirational quote!\n
            
"""


class Utility(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define the help pages. ADD MORE WHEN NEEDED.
    page1 = discord.Embed(title="Utility Commands", description=help_utility, colour=discord.Colour.orange())
    page2 = discord.Embed(title="Fun Commands", description=help_fun, colour=discord.Colour.green())
    # page3 = discord.Embed(title="TEST Bot Help 3", description="Page 3", colour=discord.Colour.orange())
    bot.help_pages = [page1, page2]  # Make sure to add new pages here as well

    # HELP COMMAND? ---------------------------------------------------------------------------------------------------------------------------
    # TODO: Find a more optimized solution if possible
    @command(name="help")
    async def help(self, ctx):
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]  # skip to start, left, right, skip to end
        current = 0
        msg = await ctx.send(embed=bot.help_pages[current])
        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                # return print("test")
                pass

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0

                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == u"\u27A1":
                    if current < len(bot.help_pages) - 1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(bot.help_pages) - 1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=bot.help_pages[current])

    # -------------------------------------------------------------------------------------------------------------------------------------
    # The GitHub Command, gives a link to the github.
    @command(name="github")
    async def github(self, ctx):
        embed = discord.Embed(title="TechnoShip123", url="http://github.com/TechnoShip123",
                              description="The link for my github page", color=0x00ffbf, timestamp=datetime.utcnow())

        embed.set_author(name="TechnoShip123", url="https://avatars.githubusercontent.com/u/75491816?s=460&u=f9d8a3cb1a09ed5cc5e918f04ff0e477bc0fadb9&v=4",
                         icon_url="https://github.com/TechnoShip123/DiscordBot/blob/master/resources/GitHub-Mark-Light-32px.png?raw=true")

        embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/75491816?s=460&u=efc006f31ed85de2b464de18e5e71b3ffaf9800a&v=4")

        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    # -------------------------------------------------------------------------------------------------------------------------------------
    # LATENCY COMMAND
    @commands.command(name="ping", help="Gets the bot latency", case_insensitive=True)
    async def ping(self, ctx):
        await ctx.send(f'🏓 Pong! Latency is **{round(self.bot.latency * 1000)}ms**.')

    # -------------------------------------------------------------------------------------------------------------------------------------
    # THE REMINDER COMMAND. Specify when you want to be reminded, and the bot will ping you on that time.
    # TODO: Make the cooldown ONLY IF THE COMMAND FAILS, such as if someone put a time that was too short or in an invalid format.
    @commands.cooldown(2, 150, commands.BucketType.user)  # Cooldown of 2 uses every 150 seconds per user.
    @command(name="remind", aliases=["reminder, remindme"], help="This command allows you to set a remind from 5 minutes to 7 days! Specify your value like 5m for 5 minutes.")
    async def remind(self, ctx, time, *, reminder):
        # print(time)
        # print(reminder)
        user = "<@!" + str(ctx.author.id) + ">"
        embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=f"{ctx.message.author.avatar_url}")
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')  # Error message
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} day(s)"  # TODO: If the result is 1 then send as day otherwise as days.
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hour(s)"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minute(s)"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} second(s)"
        if seconds == 0:
            embed.add_field(name='Invalid Duration!',
                            value='Please specify a proper duration, `?!remind <time> <name>`. For example, `?!remind 5m Coding` for a reminder in 5 minutes.')
        elif seconds < 300:
            embed.add_field(name='Duration Too Small!',
                            value='You have specified a too short duration!\nThe minimum duration is 5 minutes.')
        elif seconds > 604800:
            embed.add_field(name='Duration Too Large!', value='You have specified too long of a duration!\nThe maximum duration is 7 days.')
        else:
            await ctx.reply(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.send(f"Hey {user}, you asked me to remind you about {reminder} {counter} ago.")
            return
        await ctx.send(embed=embed)  # Send the embed with the information.

    # --------------------------------------------------------------------------------------------------------------------------------------------------
    # THE SUGGESTION COMMAND. Write down a suggestion and it'll ping in an embed.
    """@commands.cooldown(1, 120, BucketType.user)
    @command(name="suggest", aliases=["suggestion"], help="This command can be used to suggest new commands for the bot!")
    async def suggest(self, ctx):

        # Terrible unoptimized way to remove the prefix, I'll fix this later.
        uMessage = ctx.message.content.replace("?!suggest", "", 1)
        uMessage = uMessage.replace("?!suggestion", "", 1)
        await ctx.message.delete()

        # Send it on the user's side
        embed = discord.Embed(
            title="Command Suggestion",
            description="You suggested an improvement to the bot:\n \n " + "> " + uMessage + "\n \n<@!755093458586173531> take a look at this!",
            timestamp=datetime.now(timezone.utc),
            color=0xfbff00
        )
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        )
        embed.set_footer(
            text="Requested by: " + ctx.author.name,
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)"""

    # MC Server --------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.cooldown(1, 10, BucketType.user)
    @command(name="mcserver", help="Allows you to check the status of any specified Minecraft Server!")
    async def mcserver(self, ctx, argument: str):
        # Pull the ip/text they sent (auto seperated from command).
        server_ip = argument
        await ctx.message.add_reaction("<a:thonkload:820298504634105866>")
        message = await ctx.send("<a:thonkload:820298504634105866> One moment, retrieving server information...")

        response = urllib.request.urlopen(f"https://api.mcsrvstat.us/2/{server_ip}")
        data = json.load(response)
        online: bool = data['debug']['ping']  # Check if it's online.
        if online:
            motd: str = data['motd']['clean'][0].strip()
            version: int = data['version']
            online_players: int = data['players']['online']
            max_players: int = data['players']['max']
            ip: str = data['ip']

            embed = discord.Embed(
                title="<a:MinecraftGrassBlock:820298284228542484> MC Server Status <a:MinecraftGrassBlock:820298284228542484>",
                color=0x00ff2a)
            embed.set_author(name="Minecraft", url="https://minecraft.net/",
                             icon_url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2d/Plains_Grass_Block.png/revision/latest?cb=20190525093706")
            embed.add_field(name="MOTD", value=motd, inline=True)
            embed.add_field(name="Version", value=str(version), inline=True)
            embed.add_field(name="Online Player Count", value=str(online_players), inline=True)
            embed.add_field(name="Max Players", value=str(max_players), inline=True)
            embed.add_field(name="Server IP", value=server_ip + " (IP: `" + str(ip) + "`)", inline=True)

            embed.set_footer(text="Requested by: " + ctx.author.name)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="<a:MinecraftGrassBlock:820298284228542484> MC Server Status <a:MinecraftGrassBlock:820298284228542484>",
                color=0x00ff2a,
                description="The server is offline or the IP is invalid!")
            embed.set_author(name="Minecraft", url="https://minecraft.net/",
                             icon_url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2d/Plains_Grass_Block.png/revision/latest?cb=20190525093706", )

            embed.set_footer(text="Requested by: " + ctx.author.name)
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("utility")

            # We can comment this out later if needed.
            print(print_cog + print_spec + "Utility " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Utility(bot))  # Add the cog to the main class (Utility).
