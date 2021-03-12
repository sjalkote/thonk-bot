import discord
from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext import tasks
from lib.bot.__init__ import bcolors
from lib.bot.__init__ import print_info
from lib.bot.__init__ import print_spec
from lib.bot.__init__ import print_spec
from lib.bot.__init__ import print_scheduler
from lib.bot.__init__ import print_cog


class Utility(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("utility")

            # We can comment this out later if wanted.
            print(print_cog + print_spec + "Utility " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Utility(bot))  # Add the cog to the main class (Utility).
