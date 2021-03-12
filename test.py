# THIS COMMAND IS NOT GOING TO BE AVAILABLE YET
# Until I make cogs in the main bot, this command will not be usable, I'm just keeping it here for when the time comes.

from discord.ext import commands
import discord.ext.tasks
from datetime import *
import discord
import asyncio

bot = commands.Bot(command_prefix='?!', description='A simple bot by TechnoShip123 (Thonk).', case_insensitive=True)

with open("./lib/bot/token.txt", "r", encoding="utf-8") as tokenfile:
    TOKEN = tokenfile.read()


@bot.command(name="remind")
async def remind(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = "<@!" + str(ctx.author.id) + ">"
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(text="Requested by: " + "<@!" + str(ctx.author.id) + ">", icon_url=f"{bot.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')  # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} day(s)"  # TODO: If the result is 1 then send as day otherwise as days.
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
                        value='Please specify a proper duration, `?!remind <time> <name>`. For example, `?!remind 5s Coding` for a reminder in 5 seconds.')
    elif seconds < 5:
        embed.add_field(name='Duration Too Small!',
                        value='You have specified a too short duration!\nThe minimum duration is 5 seconds.')
    elif seconds > 604800:
        embed.add_field(name='Duration Too Large!', value='You have specified too long of a duration!\nThe maximum duration is 7 days.')
    else:
        await ctx.reply(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hey {user}, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)


bot.run(TOKEN)
