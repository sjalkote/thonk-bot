import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

with open("./lib/bot/token.txt", "r", encoding="utf-8") as tokenfile:
    TOKEN = tokenfile.readline()

bot = commands.Bot(command_prefix="?!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("Ready!")


guild_ids = [764981968579461130]  # Put your server ID in this array.


@slash.slash(name="test", guild_ids=guild_ids,
             description="Is thonk cool?",
             options=[
                 create_option(
                     name="option",
                     description="Yes or No.",
                     option_type=3,
                     required=False
                 )
             ])
async def test(ctx, *, option: [str] = None):
    if option is None:
        await ctx.send("Test is working.")
    else:
        if option.lower() == "yes":
            await ctx.send(f"You said {option}, thanks! :D")
        elif option.lower() == "no":
            await ctx.send(f"<:stevegun:815628826767523840> You said {option} :/")
        elif option.lower() == "e":
            await ctx.send(f"<:nice:817119421445046293> **E.**")
        else:
            await ctx.send(f"I have no idea tf you said by `{option}`, but I'm assuming yes! :D")


bot.run(TOKEN)
