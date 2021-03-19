import discord
import asyncio
import random
from datetime import *
from discord.ext.commands.cooldowns import *
from typing import Optional
from discord.ext.commands import *
from discord.ext import commands
from discord.ext import tasks
from lib.bot.__init__ import bcolors
from lib.bot.__init__ import print_info, print_spec, print_cog, print_scheduler, print_warn
# -------------------------------------------------------------------------------------------------------------------------------


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hit/Bonk command, fun way to 'hit' others for the specified reason (defaults to no reason if nothing is provided).
    # TODO: Custom error handling for member not found, make it so that it's allowed. Also add custom reasons if no reason.
    @commands.command(name="bonk", help="'Bonk' someone with objects for specified reasons!")
    async def hit(self, ctx, member: str, *, reason: Optional[str] = "no reason"):
        await ctx.message.delete()  # Delete the user message
        object_list = ["a train", "a bat", "some bees", "an acorn", "a truck", "a bulldozer", "a python", "a ban", "a mute", "a kick", "a pie", "GitHub premium", "Octocat",
                       "ThonkBot documentation", "a car", "Minecraft", "Mojang", "Steve", "Alex", "a villager", "a diamond", "an emerald", "Pylint", "Java", "a cookie",
                       "me", "JavaScript", "PHP", "their C drive", "their computer", "some HTML code", "some CSS code", "discord.py documentation", "a wall", "a plane",
                       "a black hole", "a joke", "a wet towel", "the time", "a clock", "Docker", "the Docker whale", "a turtle", "a stick", "their car keys", "a pokemon"]
        if member == "<@!815078851780542484>":  # Check if it's hitting the bot
            await ctx.send(f"{ctx.author.mention} tried to hit me, but I dodged and yeeted them!")
        else:  # Otherwise continue as normal
            await ctx.send(f"{ctx.author.mention} hit {member} with {random.choice(object_list)} for {reason}.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

            # We can comment this out later if needed.
            print(print_cog + print_spec + "Fun " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Fun(bot))  # Add the cog to the main class (Fun).
