import os
from asyncio import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import *
from discord.ext.commands import *
from dotenv import load_dotenv
from ..db import db

import discord

load_dotenv()  # TODO: MAYBE MOVE TO ROOT DIR?
api_key = os.getenv('API_KEY')
brain_id = os.getenv('BRAIN_ID')
prefix = os.getenv('PREFIX')
print(api_key)
PREFIX = prefix
OWNER_ID = 755093458586173531

COGS = ["utility", "fun", "owner"]  # Update this when you add more cogs.


# Here we make a class to add colorful words to the terminal using ANSI Escape Sequences.
class Bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	ITALIC = '\033[3m'
	# Presets for use in terminal:
	print_info = OKCYAN + BOLD + "[INFO]: " + ENDC
	print_warn = FAIL + BOLD + "[WARN]: " + ENDC
	print_scheduler = OKCYAN + BOLD + "[SCHEDULER]: " + ENDC
	print_cog = OKGREEN + BOLD + "[COG]: " + ENDC
	print_spec = OKBLUE + ITALIC
	print_success = OKGREEN + BOLD
	print_com_used = OKBLUE + BOLD + "[Command]: " + ENDC
	print_evaluate = HEADER + BOLD + "[EVAL]: " + ENDC


# A conversion command for seconds into hours:minutes:seconds.
def convert(seconds):
	seconds %= 24 * 3600
	hour = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60
	return "%d:%02d:%02d" % (hour, minutes, seconds)


class Ready:
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)
	
	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f"{Bcolors.print_cog}{Bcolors.print_spec}{cog}{Bcolors.ENDC} cog ready")
	
	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


# noinspection PyAttributeOutsideInit
class Bot(Bot):
	def __init__(self):
		with open("./lib/bot/token.txt", "r", encoding="utf-8") as token_file:
			self.TOKEN = token_file.readline()
		
		self.ready = False
		self.cogs_ready = Ready()
		self.PREFIX = PREFIX
		self.guild = None
		self.scheduler = AsyncIOScheduler()
		
		db.autosave(self.scheduler)
		super().__init__(command_prefix=PREFIX, owner_id=OWNER_ID, intents=Intents.all(), case_insensitive=True,
		                 help_command=None)  # Basic setup, define the prefix, owner ID, and turn on intents.
	
	# Setup
	def setup(self):
		cog_amount = 0  # Set the cog counter to 0.
		for cog in COGS:  # Do this for every cog there is.
			self.load_extension(f"lib.cogs.{cog}")  # Load the cog from lib.cogs, CHANGE IF DIRECTORY STRUCTURE CHANGES.
			cog_amount += 1  # Raise the counter by one (the first cog will say 1 cog loaded instead of 0).
			# <cog_name> loaded! (1)
			print(f"{Bcolors.print_cog}{Bcolors.print_spec}{cog}{Bcolors.ENDC} loaded! ({Bcolors.HEADER}{cog_amount}{Bcolors.ENDC})")
		print(f"{Bcolors.print_cog}All cogs have been loaded! We have a total of {Bcolors.HEADER}{cog_amount}{Bcolors.ENDC} cogs.")
	
	# Stuff to setup when we first run the bot.
	def run(self, version):
		
		print(f"{Bcolors.print_info}Running {Bcolors.print_spec}setup...{Bcolors.ENDC}")
		self.VERSION = version
		self.setup()
		
		print(f"{Bcolors.print_info}{Bcolors.OKGREEN}{Bcolors.BOLD}Setup Complete!{Bcolors.ENDC}")
		print(f"{Bcolors.print_info}Attempting {Bcolors.print_spec}login...{Bcolors.ENDC}")
		super().run(self.TOKEN, reconnect=True)
	
	# When the bot connects.
	async def on_connect(self):
		# Say that we logged in successfully, and give the username + userid that the bot has logged in as.
		print(f"{Bcolors.print_info}{Bcolors.print_success}Successful Connection! {Bcolors.ENDC}")
		print(f"{Bcolors.print_info}Logged in as: {Bcolors.OKCYAN}{Bcolors.HEADER}{Bcolors.ITALIC}{str(bot.user)}{Bcolors.ENDC}")
		print(f"{Bcolors.print_info}Bot ID: {Bcolors.OKCYAN}{Bcolors.HEADER}{Bcolors.ITALIC}{bot.user.id}{Bcolors.ENDC}")
	
	# When the bot disconnects/stops.
	async def on_disconnect(self):
		print(f"{Bcolors.print_warn}{Bcolors.WARNING}The bot has {Bcolors.BOLD}disconnected!{Bcolors.ENDC}")
	
	# ERROR HANDLING ------------------------------------------------------------------------------------------------------------------
	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong! ```\n" + str(args) + "\n```")
		raise
	
	async def on_command_error(self, ctx, exc):
		# If the command does not exist/is not found.
		if isinstance(exc, CommandNotFound):
			await ctx.message.add_reaction("<:questionmark:825353476317642752>")
		
		# If it has the attribute `original`
		elif hasattr(exc, "original"):
			raise exc.original
		
		# If the command is currently on a cooldown.
		elif isinstance(exc, CommandOnCooldown):
			cooldown_remaining = exc.retry_after  # Assign the remaining cooldown duration (in seconds) to a variable.
			if cooldown_remaining > 60:  # Only if the cooldown is greater than 60 seconds...
				cooldown_remaining = convert(cooldown_remaining)  # Use our convert function to convert the seconds into H:M:S format.
			else:
				cooldown_remaining = str(round(cooldown_remaining)) + " seconds"
			await ctx.message.add_reaction('⏱')  # Also try hourglass (⌛). This adds a reaction to the user's message.
			message = await ctx.reply(f"Sorry! That command is currently on a cooldown! Please try again after {cooldown_remaining}!")
			await sleep(5)
			await message.delete()
		
		# If the command is missing a required argument, like the remind command missing the duration.
		elif isinstance(exc, MissingRequiredArgument):
			await ctx.message.add_reaction("<:denied:806962608912597002>")
			await ctx.reply("Uh oh! You're missing a required argument!")
		
		elif isinstance(exc, MemberNotFound):
			message = await ctx.send("Couldn't find that member!")
			await sleep(5)
			await message.delete()
		
		elif isinstance(exc, NotOwner):
			await ctx.message.add_reaction("🔐")
			message = await ctx.send("That command is for my bot owner! Check the `?!help` command.")
			await sleep(5)
			await message.delete()
		
		elif isinstance(exc, MissingPermissions):
			pass
		elif isinstance(exc, BotMissingPermissions):
			await ctx.send("I'm missing permissions!")
		
		# If no error handling is available for it, send the error.
		else:
			try:
				await ctx.send(f"We hit an error! <@!755093458586173531> " + f"""Error:```{exc}```""")
			except Exception as critical_exception:
				print(f"""{Bcolors.FAIL}{Bcolors.BOLD}Couldn't send the error message. Error:\n {critical_exception}{Bcolors.ENDC}""")
			finally:
				print(f"{Bcolors.FAIL}[ERROR]: {exc}{Bcolors.ENDC}")
			# raise exc  # So we see this in the terminal.
	
	# ---------------------------------------------------------------------------------------------------------------------------------
	# When the bot is fully ready.
	async def on_ready(self):
		if not self.ready:
			# Wait for the cogs to be ready, let the bot start with everything ready to go at once.
			while not self.cogs_ready.all_ready():
				await sleep(0.5)
			while not self.cogs_ready.all_ready():
				await sleep(0.5)
			self.ready = True
			# SCHEDULER TEST, it will add the test_schedule job at the specified time (second=). NOTE - The below says `second="0,
			# 15"`. What that means is that any minute, whenever the seconds is = 0 or 15, it will add the job. This means it won't send
			# at 30 seconds or at 45 seconds. For example, 12:30:0 and 12:30:15 would send, but not at 12:30:30 and 12:30:45. This also
			# accepts things such as `day_of_week=0` (Sundays), `hour=12` (12:00 and 24:00), and `minute=0` (12:00 and 12:01) as well.
			
			# self.scheduler.add_job(self.test_schedule, CronTrigger(second="0, 15"))
			# print(print_scheduler + "Job Added: " + print_spec + "test_schedule" + Bcolors.ENDC)
			self.scheduler.start()
			
			print(f"{Bcolors.print_scheduler}{Bcolors.print_spec}Scheduler{Bcolors.ENDC} started!")
			status = f"you for ?!"  # The bot status
			await bot.change_presence(activity=discord.Activity(name=status, type=discord.ActivityType.watching))  # Set the bot
			# presence/status
			print(f"{Bcolors.print_info}Bot {Bcolors.print_spec}status set!{Bcolors.ENDC}")
			
			print(f"{Bcolors.print_info}{Bcolors.OKGREEN}{Bcolors.BOLD}Bot is ready!{Bcolors.ENDC}")
			# print('-----------------------------------------------------------------------------------------------------------------')
	
	async def on_message(self, message):
		# If the bot gets mentioned or pinged in any way.
		if bot.user in message.mentions:
			await message.add_reaction("<:nice:817119421445046293>")
			await message.channel.send("Yeah that's me, use `?!help` to get a list of commands!")
		
		# If someone says hi.
		elif message.content.lower() == "hello" or message.content.lower() == "hi":
			await message.add_reaction("👋")
		await bot.process_commands(message)
	
	async def on_command_completion(self, ctx):
		print(f"{Bcolors.OKBLUE}[Command]: {Bcolors.ENDC}{Bcolors.OKCYAN}{ctx.message.author} issued {Bcolors.HEADER}"
		      f"{ctx.message.content}{Bcolors.ENDC}")


bot = Bot()
