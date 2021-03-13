import discord
import asyncio
from datetime import *
from discord.ext.commands import Cog
from discord.ext.commands import *
from discord.ext.commands.cooldowns import *
from discord.ext import commands
from discord.ext import tasks
from lib.bot.__init__ import bcolors
from lib.bot.__init__ import print_info, print_spec, print_cog, print_scheduler, print_warn


class Utility(Cog):
    def __init__(self, bot):
        self.bot = bot

    # THE REMINDER COMMAND. Specify when you want to be reminded, and the bot will ping you on that time.
    # TODO: Make the cooldown ONLY IF THE COMMAND FAILS, such as if someone put a time that was too short or in an invalid format.
    @commands.cooldown(1, 150, commands.BucketType.user)  # Cooldown of 1 use every 150 seconds per user.
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
    @commands.cooldown(1, 120, BucketType.user)
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
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("utility")

            # We can comment this out later if wanted.
            print(print_cog + print_spec + "Utility " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Utility(bot))  # Add the cog to the main class (Utility).
