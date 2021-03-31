# THONK BOT - Created by TechnoShip123 (Thonk), my GitHub page is at https://github.com/TechnoShip123.
# This code is under the GNU GPL v3 License. LICENSE may not be altered or removed.


# Import the needed modules that the bot will use, like discord.py (duh).
import discord  # For the entire thing
from discord.ext import commands  # Subset of discord
from discord.ext import tasks  # Subset of discord
import sys  # For system commands
import logging  # For logging
import traceback  # For Errors
import datetime  # For timestamps
import time  # For time stuff
import json  # For API stuff
import urllib  # For API stuff
import requests  # For API stuff
import asyncio  # For timing stuff

# Here we define the command prefix for the bot, as well as the bot description and intents.
intents = discord.Intents.default()  # Simplify intents to intents.
intents.members = True  # Set intents for members to true. This will require verification if the bot is in more than 100 servers.

# Set the bot prefix, description, intents on, and make it case insensitive.
bot = commands.Bot(command_prefix='?!', description='A simple bot by TechnoShip123 (Thonk).', intents=intents, case_insensitive=True)

# We also want to get our bot token/key from our `token.txt` file. Putting it in directly in the source code would not be safe.
with open('token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')  # Assign the token to a str variable called TOKEN.


# VARIABLES, CLASSES, FUNCTIONS ---------------------------------------------------------------------------------------------------

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


# Here is the function for the quoting command using the ZenQuotes API
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


# MAIN CODE -----------------------------------------------------------------------------------------------------------------------
# Once we have all that set up, we send a message to the console letting us know the bot is ready and what login it uses.

# Notify and set status when the bot is ready.
@bot.event
async def on_ready():
    # Say that we logged in successfully, and give the username + userid that the bot has logged in as.
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + bcolors.OKGREEN + bcolors.BOLD + "Successful Login! " + bcolors.ENDC)
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + "Logged in as: " + bcolors.OKCYAN + bcolors.HEADER + bcolors.ITALIC + "{bot_username}".format(
            bot_username=bot.user.name) + bcolors.ENDC)
    print(
        bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + "Bot ID: " + bcolors.OKCYAN + bcolors.HEADER + bcolors.ITALIC + "{bot_user_id}".format(
            bot_user_id=bot.user.id) + bcolors.ENDC)

    # Here we set the bot's status, there is Playing, Watching, Listening to, Streaming, and Competing in.
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="you. | ?!help"))
    print(bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + bcolors.OKGREEN + "Bot status set! " + bcolors.ENDC)
    print('----------------------------------------------------------------------')  # Add a little seperator using hyphens (-).


# EVENT - When a new member joins the server say their name and that they joined the server.
@bot.event
async def on_member_join(member):
    print(bcolors.OKGREEN + "[SERVER]: " + bcolors.ENDC + bcolors.HEADER + f'{member}' + bcolors.ENDC + ' has joined the server!')


# COMMAND - Adds two numbers given by the user and seperated by a space.
@bot.command(name="add", help="Adds two numbers together")
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


    # This one could be: `await ctx.send("Invalid input. Try: `?!add 5 10` to add 5 + 10.")` (don't forget return)


# COMMAND - Saves the command idea given from someone to my pastebin.
@bot.command(name="suggest", help="Suggests a command for me to add to the bot.")
async def suggest(ctx, *suggestion):  # The command suggestions command
    channel = bot.get_channel(816422364681470013)  # Define my suggestion channel.

    # This section filters out the command so all I get back is the suggestion itself.
    uMessage = ' '.join(suggestion)

    embed = discord.Embed(
        title="Command Suggestion",
        description="A command suggestion was recieved:\n \n " + "`" + uMessage + "\n \n",
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    embed.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text="Requested by: " + ctx.author.name,
        icon_url=ctx.author.avatar_url
    )
    await channel.send(embed=embed)

    # Send it on the user's side
    await ctx.message.add_reaction('<a:checkmark:806962593457504296>')
    embed = discord.Embed(
        title="Command Suggestion",
        description="You suggested an improvement to the bot:\n \n " + "> " + uMessage + "\n \nIt was sent to Thonk's suggestion box!",
        timestamp=datetime.datetime.now(datetime.timezone.utc)
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


# COMMAND - Gives random quotes from a big collection provided by the ZenQuotes API
@bot.command(name='quote', help="Gives a random inspirational quote from a giant collection provided by ZenQuotes.io")
async def getZenquote(message):
    quote = get_quote()
    if quote == 'Too many requests. Obtain an auth key for unlimited access. -ZenQuotes.io':  # Check if we're reaching the limit on requests
        await message.channel.send("Do you seriously need more quotes? Wait 30 seconds please")  # Since there is a limit on requests, this is added to notify that it needs 30 seconds
    else:
        await message.channel.send(quote)  # Send the quote that we randomly chose from ZenQuotes


# COMMAND - Echoes back the user input
@bot.command(name='echo', help='Says back what you say!')
async def echo(ctx, *umessage):
    umessage = ''.join(umessage)
    await ctx.send(umessage)


# COMMAND - Self promo, this is a Github command, gives a link to my GitHub profile (TechnoShip123)
@bot.command(name="github", help="Gives the link to my GitHub profile")
async def github(ctx):
    embed = discord.Embed(title="TechnoShip123", url="http://github.com/TechnoShip123",
                          description="The link for my github page", color=0x00ffbf, timestamp=datetime.datetime.now(datetime.timezone.utc))

    embed.set_author(name="TechnoShip123", url="https://avatars.githubusercontent.com/u/75491816?s=460&u=f9d8a3cb1a09ed5cc5e918f04ff0e477bc0fadb9&v=4",
                     icon_url="https://github.com/TechnoShip123/DiscordBot/blob/master/resources/GitHub-Mark-Light-32px.png?raw=true")

    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/75491816?s=460&u=efc006f31ed85de2b464de18e5e71b3ffaf9800a&v=4")

    embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


# ERROR HANDLING ------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_command_error(ctx, error):
    # If the command has local error handler, then just return.
    if hasattr(ctx.command, 'on_error'):
        return

    # Get the original exception/error.
    error = getattr(error, 'original', error)

    # If the command does not exist
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('This command does not exist!')

    # If the BOT is missing permissions to run the command.
    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
        await ctx.send(_message)
        return

    # If the command is disabled.
    if isinstance(error, commands.DisabledCommand):
        await ctx.send('This command has been disabled.')
        return

    # If the command is on cooldown when the user requests it.
    if isinstance(exc, commands.CommandOnCooldown):
        await ctx.message.add_reaction('🕐')
        await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(exc.retry_after)))
        return

    # If the user needs certain permissions to run the command.
    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        await ctx.send(_message)
        return

    # If the command recieves an invalid input from the user.
    if isinstance(error, commands.UserInputError):
        await ctx.send("Invalid input.")
        return

    # If the command can not be used in DM's / Private Messages.
    if isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send('This command cannot be used in direct messages.')
        except discord.Forbidden:
            pass
        return

    # If the user of the command does not have the permission to use it.
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
        return

    # Ignore all other exception types, but print them to stderr
    print(bcolors.FAIL + "[ERROR]: " + bcolors.ENDC + bcolors.WARNING + 'Ignoring exception in command {}:'.format(
        ctx.command) + bcolors.ENDC, file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


# RUN CODE ------------------------------------------------------------------------------------------------------------------------

# Here is the final step, where we start to run our bot.
print(bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + bcolors.OKBLUE + bcolors.ITALIC + "Starting Bot... " + bcolors.ENDC)
bot.run(TOKEN)
