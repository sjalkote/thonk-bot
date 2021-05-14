import sys

import discord
import psutil
from discord.ext.commands import *

from lib.bot.__init__ import Bcolors


class OwnerCog(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	# SHUTDOWN COMMAND -------------------------------------------------------------------------
	@command(name="shutdown")
	@is_owner()
	async def shutdown(self, ctx):
		await ctx.send("Alright, shutting down.")
		print(f"{Bcolors.print_info}{Bcolors.print_success}Stopping bot.{Bcolors.ENDC}")
		await self.bot.close()  # Not a very clean way to stop, but there is a Windows where the bot.stop and logout don't work.
	
	# RESTART COMMAND ---------------------------------------------------------------------------
	# @command(name="restart")
	# @is_owner()
	# async def restart(self, ctx):
	# 	await ctx.reply("Alright, I'm restarting.")
	# 	try:
	# 		print("------------------------------------------------------------------------------------------------------------")
	# 		await self.bot.close()
	# 	finally:
	# 		os.system("python launcher.py")
	
	# STATS COMMAND -----------------------------------------------------------------------------
	@command(name="botstats")
	@is_owner()
	async def botstats(self, ctx):
		embed = discord.Embed(title="Bot Status", type="rich")
		vmem = psutil.virtual_memory()
		embed.add_field(name="RAM Usage", value=f"{round(vmem.used / 1000000000, 2)}GB out of \
        {round(vmem.total / 1000000000, 2)}GB")
		embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
		embed.add_field(name="Python info", value=sys.version, inline=False)
		embed.add_field(name="Bot Info", value=f"Me: <@!{self.bot.user.id}>\nOwner: <@!{self.bot.owner_id}>")
		await ctx.send(embed=embed)
	
	# End of Cog -------------------------------------------------------------------------------------------------------------------------
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("owner")
			# print(Bcolors.print_cog + Bcolors.print_spec + "Utility " + Bcolors.ENDC + "cog started!")


def setup(bot):
	bot.add_cog(OwnerCog(bot))
