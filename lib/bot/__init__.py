from asyncio import sleep
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import *
from discord.errors import *
from discord.ext.commands import *

from ..db import db

PREFIX = "?!"
OWNER_ID = '755093458586173531'


# Here we make a class to add colorful words to the terminal using ANSI Escape Sequences.
class bcolors:
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


print_info = bcolors.OKCYAN + bcolors.BOLD + "[INFO]: " + bcolors.ENDC
print_scheduler = bcolors.OKCYAN + bcolors.BOLD + "[SCHEDULER]: " + bcolors.ENDC
print_spec = bcolors.OKBLUE + bcolors.ITALIC
print_warn = bcolors.FAIL + bcolors.BOLD + "[WARN]: " + bcolors.ENDC
# TODO: Make a list of these


class Bot(Bot):
    def __init__(self):
        with open("./lib/bot/token.txt", "r", encoding="utf-8") as tokenfile:
            self.TOKEN = tokenfile.read()

        self.ready = False
        self.PREFIX = PREFIX
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_id=OWNER_ID, intents=Intents.all())  # Basic setup, define the prefix, owner ID, and turn on intents.

    # Stuff to setup when we first run the bot.
    def run(self, version):

        print(print_info + "Running the " + print_spec + "setup..." + bcolors.ENDC)
        self.VERSION = version

        print(print_info + bcolors.OKGREEN + bcolors.BOLD + "Setup Complete!" + bcolors.ENDC)
        print(print_info + "Attempting " + print_spec + "login..." + bcolors.ENDC)
        super().run(self.TOKEN, reconnect=True)

    # When the bot connects.
    async def on_connect(self):
        # Say that we logged in successfully, and give the username + userid that the bot has logged in as.
        print(
            print_info + bcolors.OKGREEN + bcolors.BOLD + "Successful Connection! " + bcolors.ENDC)
        print(
            print_info + "Logged in as: " + bcolors.OKCYAN + bcolors.HEADER + bcolors.ITALIC + "{bot_username}".format(
                bot_username=bot.user.name) + bcolors.ENDC)
        print(
            print_info + "Bot ID: " + bcolors.OKCYAN + bcolors.HEADER + bcolors.ITALIC + "{bot_user_id}".format(
                bot_user_id=bot.user.id) + bcolors.ENDC)

    # When the bot disconnects/stops.
    async def on_disconnect(self):
        print(print_warn + bcolors.WARNING + "The bot has" + bcolors.BOLD + "disconnected!" + bcolors.ENDC)

# ERROR HANDLING ------------------------------------------------------------------------------------------------------------------
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong!")
        raise

    async def on_command_error(self, ctx, exc):
        # If the command does not exist/is not found.
        if isinstance(exc, CommandNotFound):
            await ctx.reply("Sorry! That command does not currently exist!")
            pass

        # If it has the attribute `original`
        elif hasattr(exc, "original"):
            raise exc.original

        # If no error handling is available for it, send the error.
        else:
            await ctx.reply("Uh Oh! Looks like we got a weird error! ```" + exc + "```" + "<@!" + str(bot.owner_id) + ">" + "do something about this!")
            raise exc

# ---------------------------------------------------------------------------------------------------------------------------------
    # When the bot is fully ready.
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            # SCHEDULER TEST, it will add the test_schedule job at the specified time (second=).
            # NOTE - The below says `second="0,15"`. What that means is that any minute, whenever the seconds is = 0 or 15, it will add the job.
            # This means it won't send at 30 seconds or at 45 seconds. For example, 12:30:0 and 12:30:15 would send, but not at 12:30:30 and 12:30:45.
            # This also accepts things such as `day_of_week=0` (Sundays), `hour=12` (12:00 and 24:00), and `minute=0` (12:00 and 12:01) as well.

            # self.scheduler.add_job(self.test_schedule, CronTrigger(second="0, 15"))
            # print(print_scheduler + "Job Added: " + print_spec + "test_schedule" + bcolors.ENDC)
            self.scheduler.start()

            print(print_info + bcolors.OKBLUE + bcolors.ITALIC + 'Scheduler' + bcolors.ENDC + ' started!')
            print(print_info + bcolors.OKGREEN + bcolors.BOLD + 'Bot is ready!' + bcolors.ENDC)
            print('-----------------------------------------------------------------------------------------------------------------')

            # Easy way to ping the bot or me (owner) in a mention, discord structures mentions like this.
            bot_mention = "<@!" + str(bot.user.id) + ">"
            owner_mention = "<@!" + str(bot.owner_id) + ">"

            # Now set the bot is completely ready.

            # Set it to send to: Bot Creator's Bot-Spam Channel (MDSP) and Thonk-Bot Status Channel (Bot Server)
            channels = [self.get_channel(796492337789403156), self.get_channel(819178732932956191)]
            # Create a neat embed saying that the bot is online, as well as the timestamp, and a green color.
            embed = Embed(
                title="Bot Online!",
                description=bot_mention + " is now online!",
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                color=0x00ff00
            )

            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/815078851780542484/a10e59ac12b66984453e299e8cb89a8a.png?size=256")
            embed.add_field(name="Username", value=bot.user.name, inline=True)
            embed.add_field(name="Owner", value=owner_mention, inline=True)
            embed.add_field(name="ID", value=bot.user.id, inline=False)
            # embed.add_field(name="Name", value="Value", inline=True)

            embed.set_footer(
                text="Online Notifier",
                icon_url='https://cdn.discordapp.com/avatars/815078851780542484/a10e59ac12b66984453e299e8cb89a8a.png?size=256'
            )
            for channel in channels:
                await channel.send(embed=embed)  # Send the online message to the botcreators channel and the update channel.

        else:
            print("bot reconnected")

    # A test for the scheduling functionality, the scheduler will do this at the specified time.
    async def test_schedule(self):
        channel = self.get_channel(819727424659914762)
        await channel.send('This is a scheduled message, the bot is working fine!')


bot = Bot()
