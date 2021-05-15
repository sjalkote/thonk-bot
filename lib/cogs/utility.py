import asyncio
import datetime
import json
import random
import urllib
from datetime import *

import discord
from discord.ext.commands import *
from discord.ext.commands.cooldowns import *

# --------------------------------------------------------------------------------------------------------------------
help_utility = """
`?!help` - The command you're using right now! Get help for the various commands of this bot.\n
`?!remind` - Set a reminder for anything, for a duration of 5 minutes to 7 days! Cooldown of 1 use every 5 minutes.\n
`?!mcserver` - Check the status of any Minecraft server by simply specifying the IP after the command! Cooldown of one\
 use every 10 seconds.\n
`?!ping` - Get the bot's latency.\n
`?!info` - Send a link to info sources such as the documentation website and my GitHub.\n
"""

help_fun = """
`?!bonk` - 'Hit' another member for a specified reason with random objects!\n
`?!8ball` - Give a question and the 8-ball will answer!\n
`?!soup` - Get your fresh soup here!\n
`?!quote` - Get a random inspirational quote!\n
`?!say` - Say something through the bot, supports various emojis from my server! List them with `--emojis`. It can also\
 send gifs, use `--gifs ` and then the name of a gif in the available gifs! To list available gifs just use `--gifs`.\n
`?!ai` - Talk to ThonkBot, an AI! Use `?!ai ` then write your message, and ThonkBot will reply! It is user specific so\n
it can remember things about you, like if you tell it a name.

"""

help_owner = """
            `?!restart` - Restart the entire bot.\n
            `?!shutdown` - Turns off the bot and exists the script.\n
            `?!botstats` - Get bot and machine information.

"""


class Utility(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.polls = []
	
	# Define the help pages. ADD MORE WHEN NEEDED.
	page1 = discord.Embed(title="Utility Commands", description=help_utility, color=discord.Color.orange(),
	                      url="https://thonkbot.zetasj.com#utility")
	page1.set_footer(text="You can check out my documentation at https://thonkbot.zetasj.com#utility !")
	page2 = discord.Embed(title="Fun Commands", description=help_fun, color=discord.Color.green(),
	                      url="https://thonkbot.zetasj.com#fun")
	page2.set_footer(text="You can check out my documentation at https://thonkbot.zetasj.com#fun !")
	page3 = discord.Embed(title="Owner Commands", description=help_owner, color=discord.Color.blue(),
	                      url="https://thonkbot.zetasj.com#owner")
	page3.set_footer(text="You can find my documentation at https://thonkbot.zetasj.com#owner")
	# page = discord.Embed(title="TEST Bot Help", description="Page", colour=discord.Colour.orange())
	bot.help_pages = [page1, page2, page3]  # Make sure to add new pages here as well
	
	# HELP COMMAND? --------------------------------------------------------------------------------------------------
	@command(name="help")
	async def help(self, ctx, *cmdname):
		ecolor = int("{:06x}".format(random.randint(0, 0xFFFFFF)), 16)  # Get a random embed color.
		
		# IF statements for specific help command parameters:
		if cmdname:
			
			if cmdname[0] == "help":
				embed = discord.Embed(title="HELP: Help Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="The help command `?!help` is what you are using right now! It can "
				                                  "give a paged embed with a description on all "
				                                  "available commands. You can navigate the embed between pages using "
				                                  "the reactions below it, only the person that issues the "
				                                  "command will be able to control the pages. To see help on a "
				                                  "specific command like you are right now, use `?!help "
				                                  "<command_name>`. For example, to see help on the remind command, "
				                                  "use `?!help remind`.")
				await ctx.send(embed=embed)
			
			elif cmdname[0] == "remind":
				embed = discord.Embed(title="HELP: Remind Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="The `?!remind` command is a useful tool to get a ping with the "
				                                  "reminder description you specify. The limit is "
				                                  "from 5 minutes to 7 days. To use the command, use the following "
				                                  "syntax: `?!remind <duration> <description>`. For the duration "
				                                  "seconds are specified with `s`, minutes are `m`, hours are `h`, "
				                                  "and days are `d`. For example, a reminder in 20 minutes about "
				                                  "an upcoming "
				                                  "exam, could be `?!remind 20m upcoming exam`. The cooldown on this "
				                                  "command is 1 use every 5 minutes per user.")
				await ctx.send(embed=embed)
			elif cmdname[0] == "mcserver":
				embed = discord.Embed(title="HELP: MC Server Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="The `?!mcserver` command allows you to check the status of any "
				                                  "open Minecraft Server! To use the command you need to "
				                                  "specify the server IP after the command, for example, `?!mcserver "
				                                  "mc.server.net`. If the server is online, you will get info "
				                                  "such "
				                                  "as the amount of online players, server MOTD, and more. If the "
				                                  "server is not online or the IP is invalid, you will get an "
				                                  "'invalid or offline' message.")
				await ctx.send(embed=embed)
			elif cmdname[0] == "ping":
				embed = discord.Embed(title="HELP: Ping Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="This command simply allows you to check the bot's latency, it will "
				                                  "return in milliseconds rounded to a whole number.")
				await ctx.send(embed=embed)
			elif cmdname[0] == "info":
				embed = discord.Embed(title="HELP: Info Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="This command allows you to get links for relevant sources of info, "
				                                  "including my documentation page and the GitHub repository. "
				                                  "Optionally, you can specify a user after the command (`?!info "
				                                  "<user_mention>`) and it will ping that user in the message.")
				await ctx.send(embed=embed)
			elif cmdname[0] == "bonk":
				embed = discord.Embed(title="HELP: Bonk Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="The bonk command allows you to 'hit' another member for a "
				                                  "specified reason with randomly-selected objects! "
				                                  "The usage of the command is `?!bonk <@member> <reason>`. If you "
				                                  "don't specify the reason through usage such as "
				                                  "`?!bonk <@member>`, it will hit them 'for no reason'.")
				await ctx.send(embed=embed)
			elif cmdname[0] == "8ball":
				embed = discord.Embed(title="HELP: Eight-Ball Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="Ask the eight-ball a question and it shall give you its insight. "
				                                  "The usage is `?!8ball <question>`.")
				await ctx.send(embed=embed)
			
			elif cmdname[0] == "soup":
				embed = discord.Embed(title="HELP: Soup Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="Get some fresh soup, with a reaction and a message!")
				await ctx.send(embed=embed)
			
			elif cmdname[0] == "quote":
				embed = discord.Embed(title="HELP: Quote Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="Get a quote from a huge collection provided by the ZenQuotes API! "
				                                  "Includes the quote and the author.")
				await ctx.send(embed=embed)
			
			elif cmdname[0] == "say":
				embed = discord.Embed(title="HELP: Say Command", color=ecolor, url="https://thonkbot.zetasj.com",
				                      description="The say command allows you to say things from the bot, including "
				                                  "emojis, or choosing a gif! To view available "
				                                  "emojis you can use `?!say --emojis`, and it will list them. To "
				                                  "view available gifs, use `?!say --gifs`. "
				                                  "To send a message you can use `?!say <message>`, and add emojis "
				                                  "anywhere in the message with `:emojiname:`. "
				                                  "For gifs, just specify the gif name that it is listed as in the "
				                                  "`--gifs` list, but specify that it is a gif, "
				                                  "otherwise it will assume you are asking to send a message. For "
				                                  "example, `?!say --gifs sus`.")
				await ctx.send(embed=embed)
			
			# If the command does not exist:
			else:
				await ctx.send("Sorry, that command does not exist here!")
		
		# If no specific command parameter is specified, we give the general help page.
		else:
			buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]  # skip to start, left, right, skip to end
			current = 0
			msg = await ctx.send(embed=bot.help_pages[current])
			for button in buttons:
				await msg.add_reaction(button)
			
			while True:
				try:
					reaction, user = await self.bot.wait_for("reaction_add",
					                                         check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons,
					                                         timeout=60.0)
				
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
	
	# ----------------------------------------------------------------------------------------------------------------
	# The Info command, gives the links to relative info such as documentation and the repository.
	@command(name="info", aliases=["github"])
	async def info(self, ctx, *user):
		embed = discord.Embed(title="TechnoShip123", url="http://github.com/TechnoShip123",
		                      description="The link for my github page is:\n <https://github.com/TechnoShip123>",
		                      color=0x00ffbf, timestamp=datetime.utcnow())
		embed.add_field(name="Bot Repository",
		                value="The bot repository can be found here:\n <https://github.com/TechnoShip123/thonk-bot>")
		embed.add_field(name="Documentation", value="My documentation can be found at:\n <https://thonkbot.zetasj.com>",
		                inline=False)
		
		embed.set_author(name="TechnoShip123",
		                 url="https://avatars.githubusercontent.com/u/75491816?s=460&u" +
		                     "=f9d8a3cb1a09ed5cc5e918f04ff0e477bc0fadb9&v=4",
		                 icon_url="https://github.com/TechnoShip123/DiscordBot/blob/master/resources/GitHub-Mark"
		                          "-Light-32px.png?raw=true")
		
		embed.set_thumbnail(
			url="https://avatars.githubusercontent.com/u/75491816?s=460&u=efc006f31ed85de2b464de18e5e71b3ffaf9800a&v=4")
		
		embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar_url)
		
		if user:
			await ctx.message.delete()
			await ctx.send(f"{user[0]}, take a look at my information:", embed=embed)
		else:
			await ctx.send(embed=embed)
	
	# ----------------------------------------------------------------------------------------------------------------
	# LATENCY COMMAND
	@command(name="ping", aliases=["latency"], help="Gets the bot latency")
	async def ping(self, ctx):
		await ctx.send(f'🏓 Pong! Latency is **{round(self.bot.latency * 1000)}ms**.')
	
	# ----------------------------------------------------------------------------------------------------------------
	# THE REMINDER COMMAND. Specify when you want to be reminded, and the bot will ping you on that time.
	# noinspection PyUnboundLocalVariable
	@cooldown(1, 150, BucketType.user)  # Cooldown of 2 uses every 150 seconds per user.
	@command(name="remind", aliases=["reminder, remindme"])
	async def remind(self, ctx, time, *, reminder):
		
		user = "<@!" + str(ctx.author.id) + ">"
		embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
		embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=f"{ctx.message.author.avatar_url}")
		seconds = 0
		# If no reminder is specified:
		if reminder is None:
			embed.add_field(name='Warning',
			                value="Please specify what do you want me to remind you about. (after the time interval)")
			self.remind.reset_cooldown(ctx)
		elif time[:-1].isnumeric() is False:
			self.remind.reset_cooldown(ctx)
			embed.add_field(name='Warning',
			                value="Please specify a valid time! For example, `5m` for 5 minutes, or `2d for 2 days`!")
		
		else:
			if time.lower().endswith("d"):
				seconds += int(time[:-1]) * 60 * 60 * 24
				counter = f"{seconds // 60 // 60 // 24} day(s)"
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
				                value='Please specify a proper duration, `?!remind <time> <name>`. For example, '
				                      '`?!remind 5m Coding` for a reminder in 5 minutes.')
				self.remind.reset_cooldown(ctx)
			elif seconds < 300:
				embed.add_field(name='Duration Too Small!',
				                value='You have specified a too short duration!\nThe minimum duration is 5 minutes.')
				self.remind.reset_cooldown(ctx)
			elif seconds > 604800:
				embed.add_field(name='Duration Too Large!',
				                value='You have specified too long of a duration!\nThe maximum duration is 7 days.')
				self.remind.reset_cooldown(ctx)
			else:
				await ctx.reply(f"Alright, I will remind you about {reminder} in {counter}.")
				await asyncio.sleep(seconds)
				await ctx.send(f"Hey {user}, you asked me to remind you about {reminder} {counter} ago.")
				return
		await ctx.send(embed=embed)  # Send the embed with the information.
	
	# Remind Command ERROR HANDLER (Invalid Input)
	@remind.error
	async def remind_error(self, ctx, exc):
		if isinstance(exc, MissingRequiredArgument):
			self.remind.reset_cooldown(ctx)
		elif isinstance(exc, ValueError):
			self.remind.reset_cooldown(ctx)
			await ctx.send("That isn't a valid time duration")
	
	# await ctx.send("A required argument was missing")
	
	# ----------------------------------------------------------------------------------------------------------------
	# THE SUGGESTION COMMAND. Write down a suggestion and it'll ping in an embed.
	"""@commands.cooldown(1, 120, BucketType.user) @command(name="suggest", aliases=["suggestion"], help="This
    command can be used to suggest new commands for the bot!") async def suggest(self, ctx):

        # Terrible unoptimized way to remove the prefix, I'll fix this later.
        uMessage = ctx.message.content.replace("?!suggest", "", 1)
        uMessage = uMessage.replace("?!suggestion", "", 1)
        await ctx.message.delete()

        # Send it on the user's side embed = discord.Embed( title="Command Suggestion", description="You suggested an
        improvement to the bot:\n \n " + "> " + uMessage + "\n \n<@!755093458586173531> take a look at this!",
        timestamp=datetime.now(timezone.utc), color=0xfbff00 ) embed.set_author( name=ctx.author.name,
        icon_url=ctx.author.avatar_url ) embed.set_footer( text="Requested by: " + ctx.author.name,
        icon_url=ctx.author.avatar_url ) await ctx.send(embed=embed) """
	
	# MC Server ------------------------------------------------------------------------------------------------------
	@cooldown(1, 10, BucketType.user)
	@command(name="mcserver", help="Allows you to check the status of any specified Minecraft Server!")
	async def mcserver(self, ctx, argument: str):
		# Pull the ip/text they sent (auto separated from command).
		server_ip = argument
		await ctx.message.add_reaction("<a:thonkload:820298504634105866>")
		await ctx.send("<a:thonkload:820298504634105866> One moment, retrieving server information...")
		
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
				title="<a:MinecraftGrassBlock:820298284228542484> MC Server Status "
				      "<a:MinecraftGrassBlock:820298284228542484>",
				color=0x00ff2a)
			embed.set_author(name="Minecraft", url="https://minecraft.net/",
			                 icon_url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2d"
			                          "/Plains_Grass_Block.png/revision/latest?cb=20190525093706")
			embed.add_field(name="MOTD", value=motd)
			embed.add_field(name="Version", value=str(version))
			embed.add_field(name="Online Player Count", value=str(online_players))
			embed.add_field(name="Max Players", value=str(max_players))
			embed.add_field(name="Server IP", value=server_ip + " (IP: `" + str(ip) + "`)")
			
			embed.set_footer(text="Requested by: " + ctx.author.name)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(
				title="<a:MinecraftGrassBlock:820298284228542484> MC Server Status "
				      "<a:MinecraftGrassBlock:820298284228542484>",
				color=0x00ff2a,
				description="The server is offline or the IP is invalid!")
			embed.set_author(name="Minecraft", url="https://minecraft.net/",
			                 icon_url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/2/2d"
			                          "/Plains_Grass_Block.png/revision/latest?cb=20190525093706", )
			
			embed.set_footer(text="Requested by: " + ctx.author.name)
			await ctx.send(embed=embed)
	
	# POLL COMMAND ----------------------------------------------------------------------------------------------------
	@command(name="poll", aliases=["createpoll", "makepoll"])
	@has_permissions(manage_guild=True)
	async def poll(self, ctx, hours: int, question: str, *options):
		if len(options) > 10:
			await ctx.send("Sorry, you can only set a maximum of 10 options!")
		else:
			nums = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
			        "6⃣", "7⃣", "8⃣", "9⃣", "🔟")
			embed = discord.Embed(title="Poll",
			                      description=question,
			                      color=int("{:06x}".format(random.randint(0, 0xFFFFFF)), 16),
			                      timestamp=datetime.utcnow())
			fields = [("Options", "\n".join([f"{nums[idx]} {option}" for idx, option in enumerate(options)]), False),
			          ("Instructions", "React to cast a vote!", False)]
			
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			
			message = await ctx.send(embed=embed)
			
			for emoji in nums[:len(options)]:
				await message.add_reaction(emoji)
			
			self.polls.append((message.channel.id, message.id))
			
			self.bot.scheduler.add_job(self.complete_poll, "date", run_date=datetime.now() + timedelta(seconds=hours),
			                           args=[message.channel.id, message.id])
	
	@poll.error
	async def poll_error(self, ctx, exc):
		if isinstance(exc, MissingPermissions):
			await ctx.message.add_reaction("🔒")
			message = await ctx.send("You need `Manage Server` permissions to use this command!")
			await asyncio.sleep(5)
			await message.delete()
	
	async def complete_poll(self, channel_id, message_id):
		message = await self.bot.get_channel(channel_id).fetch_message(message_id)
		
		most_voted = max(message.reactions, key=lambda r: r.count)
		
		await message.channel.send(
			f"Voting is done and option {most_voted.emoji} was the most popular with {most_voted.count - 1:,} votes!")
		self.polls.remove((message.channel.id, message.id))
	
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("utility")


# print(Bcolors.print_cog + Bcolors.print_spec + "Utility " + Bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
	bot.add_cog(Utility(bot))  # Add the cog to the main class (Utility).
