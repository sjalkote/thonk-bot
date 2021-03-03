# THONK BOT - Created by TechnoShip123 (Thonk), my GitHub page is at https://github.com/TechnoShip123.
# This code is under the GNU GPL v3 License. LICENSE may not be altered or removed.

# Import the needed modules that the bot will use, like discord.py (duh).
import discord  # For the entire thing
from discord.ext import commands  # Subset of discord
from discord.ext import tasks  # Subset of discord
import sys  # For system commands
import logging  # For logging TODO: Set up logging
import traceback  # For Errors

# Here we define the command prefix for the bot, as well as the bot description and intents.
intents = discord.Intents.default()  # Simplify intents to intents.
intents.members = True  # Set intents for members to true. This will require verification if the bot is in more than 100 servers.

# Set the bot prefix, description, intents on, and make it case insensitive.
bot = commands.Bot(command_prefix='?!', description='A simple bot by TechnoShip123 (Thonk)', intents=intents,
                   case_insensitive=True)

# We also want to get our bot token/key from our `token.txt` file. Putting it in directly in the source code would not be safe.
with open('token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')  # Assign the token to a str variable called TOKEN.


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


# MAIN CODE -----------------------------------------------------------------------------------------------------------------------
# Once we have all that set up, we send a message to the console letting us know the bot is ready and what login it uses.
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
        activity=discord.Activity(type=discord.ActivityType.watching, name="your every move | ?!"))
    # await bot.change_presence(activity=discord.Streaming(name="and watching for ?!", url='https://www.twitch.tv/morshu_beatbox'))
    print(bcolors.OKCYAN + "[INFO]: " + bcolors.ENDC + bcolors.OKGREEN + "Bot status added! " + bcolors.ENDC)
    print(
        '----------------------------------------------------------------------')  # Add a little seperator using hyphens (-).


# EVENT - When a new member joins the server say their name and that they joined the server.
@bot.event
async def on_member_join(member):
    # TODO: Make it have a green color and say [SERVER]:
    print(
        bcolors.OKGREEN + "[SERVER]: " + bcolors.ENDC + bcolors.HEADER + f'{member}' + bcolors.ENDC + ' has joined the server!')


# COMMAND - Adds two numbers given by the user and seperated by a space.
@bot.command(name="add", help="Adds two numbers together")
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

    # TODO: Custom Error message for some commands?
    # This one could be: `await ctx.send("Invalid input. Try: `?!add 5 10` to add 5 + 10.")` (don't forget return)


# COMMAND - Saves the command idea given from someone to a file.
@bot.command(name="commandidea", aliases=["csuggest", "command_suggestion", "cidea"],
             help="Suggests a command for me to add to the bot.")
async def command_suggestion(ctx):
    channel = bot.get_channel(816422364681470013)  # Define my suggestion channel.
    await channel.send(ctx.message.content)  # Send the suggestion to my suggestion channel
    await ctx.message.add_reaction('<a:checkmark:806962593457504296>')
    await ctx.send("Your suggestion: ```" + ctx.message.content + "``` has been sent to Thonks idea pastebin!")


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
        await ctx.send('This command does not exist!')  # TODO: Add suggestion command and tell about it here.

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

    # If the command is on cooldown while being asked again from a user.
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
        # TODO: Make it delete the message after a few seconds here.
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
