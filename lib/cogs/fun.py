import discord
import asyncio
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
    # TODO: Custom error handling for member not found, make it so that it's allowed.
    @commands.command(name="bonk", help="'Bonk' someone with objects for specified reasons!")
    async def hit(self, ctx, member: MemberConverter, *, reason: Optional[str] = "no reason"):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention} hit {member.mention} for {reason}!")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

            # We can comment this out later if needed.
            print(print_cog + print_spec + "Fun " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Fun(bot))  # Add the cog to the main class (Fun).
