import discord
import os
import asyncio
import psutil
import sys
from datetime import *
from discord.ext.commands import *
from discord.ext.commands.cooldowns import *
from discord.ext import *
from lib.bot.__init__ import bcolors


class OwnerCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    # SHUTDOWN COMMAND -------------------------------------------------------------------------
    @command(name="shutdown")
    @is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Alright, shutting down.")
        print(f"{bcolors.print_info}{bcolors.print_success}Stopping bot.{bcolors.ENDC}")
        exit(0)  # Not a very clean way to stop, but there is a Windows where the bot.stop and logout don't work.

    # RESTART COMMAND ---------------------------------------------------------------------------
    @command(name="restart")
    @is_owner()
    async def restart(self, ctx):
        await ctx.reply("Alright, I'm restarting.")
        try:
            await bot.close()
        finally:
            os.system("python3 launcher.py")

    # STATS COMMAND -----------------------------------------------------------------------------
    @command(name="botstats")
    @is_owner()
    async def botstats(self, ctx):
        embed = discord.Embed(title="Server Status", type="rich")
        vmem = psutil.virtual_memory()
        embed.add_field(name="RAM Usage", value=f"{round(vmem.used / 1000000000, 2)}GB out of \
        {round(vmem.total / 1000000000, 2)}GB")
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="Python info", value=sys.version, inline=False)
        embed.add_field(name="Bot Info", value=f"Me: <@!{self.bot.user.id}>\nOwner: <@!{self.bot.owner_id}>")
        await ctx.send(embed=embed)

    '''
    # An anti-spam checker made for ThatOtherAndrew, checks if 3 or more messages are being spammed that are mentioning
     people, then 'deploys a chain chomp'.
    @Cog.listener()
    async def on_message(self, message):
        def _check(m):
            return (m.author == message.author
                    and len(m.mentions)
                    and (datetime.utcnow() - m.created_at).seconds < 60)

        if not message.author.bot:
            if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:  # If we detect spamming
                await message.channel.send("Don't spam mentions!", delete_after=10)
                await message.channel.send("https://i.imgur.com/LzDKgZN.png")
    '''

# End of Cog -------------------------------------------------------------------------------------------------------
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("owner")
            # print(bcolors.print_cog + bcolors.print_spec + "Utility " + bcolors.ENDC + "cog started!")


def setup(bot):
    bot.add_cog(OwnerCog(bot))
