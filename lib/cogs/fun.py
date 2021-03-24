import discord
import asyncio
import random
import requests
import json
from datetime import *
from discord.ext.commands.cooldowns import *
from typing import Optional
from discord.ext.commands import *
from discord.ext import commands
from discord.ext import tasks
from lib.bot.__init__ import bcolors
from lib.bot.__init__ import print_info, print_spec, print_cog, print_scheduler, print_warn
# -------------------------------------------------------------------------------------------------------------------------------


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hit/Bonk command, fun way to 'hit' others for the specified reason (defaults to no reason if nothing is provided).
    # TODO: Custom error handling for member not found, make it so that it's allowed. Also add custom reasons if no reason.
    @commands.command(name="bonk", help="'Bonk' someone with objects for specified reasons!")
    async def hit(self, ctx, member: str, *, reason: Optional[str] = "no reason"):
        await ctx.message.delete()  # Delete the user message
        object_list = ["a train", "a bat", "some bees", "an acorn", "a truck", "a bulldozer", "a python", "a ban", "a mute", "a kick", "a pie", "GitHub premium", "Octocat",
                       "ThonkBot documentation", "a car", "Minecraft", "Mojang", "Steve", "Alex", "a villager", "a diamond", "an emerald", "Pylint", "Java", "a cookie",
                       "me", "JavaScript", "PHP", "their C drive", "their computer", "some HTML code", "some CSS code", "discord.py documentation", "a wall", "a plane",
                       "a black hole", "a joke", "a wet towel", "the theory of time", "a clock", "Docker", "the Docker whale", "a turtle", "a stick", "their car keys", "a pokemon"]
        if member == "<@!815078851780542484>":  # Check if it's hitting the bot
            await ctx.send(f"{ctx.author.mention} tried to hit me, but I dodged and yeeted them!")
        elif member == ctx.author.mention:  # Check if they're hitting themseleves
            await ctx.send(f"{ctx.author.mention} themseleves with {random.choice(object_list)} for {reason}.")
        else:  # Otherwise continue as normal
            await ctx.send(f"{ctx.author.mention} hit {member} with {random.choice(object_list)} for {reason}.")

# THE SOUP COMMAND ------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="soup")
    async def soup(self, ctx):
        choices_no = ["Sorry, we dont have any left :/", "no :gun: :cook: "]
        choices_yes = [
            "<:soup:808428326120063007> Here you go friend! Fresh soup from questionable places of the Mooshroom! <:soup:808428326120063007>",
            "Heres your soup :cook: <:soup:808428326120063007>",
            "Fresh soup! Right out of the... Just take your soup <:soup:808428326120063007>",
            "Here it is sir! <:soup:808428326120063007>",
            "Soup <:soup:808428326120063007> :D",
            "Here, have your very own shroom soup <:soup:808428326120063007>",
            "Here you have it <:soup:808428326120063007>",
            "Here it is :flushed: <:soup:808428326120063007>",
            ":flushed: This one looks interesting <:soup:808428326120063007>",
            "Soup is pog <:soup:808428326120063007>"
        ]
        respond_no = random.choice(choices_no)
        respond_yes = random.choice(choices_yes)
        chance = random.randint(1, 100)
        if chance <= 1:  # If they get a 5% chance say no.
            await ctx.message.add_reaction('❌')
            await ctx.reply(f"{respond_no}")
        else:  # Have a 95% chance to say yes.
            await ctx.message.add_reaction('<:soup:808428326120063007>')
            await ctx.send(f'{respond_yes}')

# ------------------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="eightball", aliases=["8ball"], help="Just like a real 8 ball!")
    async def eightball(self, ctx):
        color = int("{:06x}".format(random.randint(0, 0xFFFFFF)), 16)  # RANDOM EMBED COLOR! Makes the embed color random each time!

        print("{} issued .8ball 🎱".format(ctx.author))  # TODO: Implement in all commands and prettify

        choices = [
            "heck no",
            "wtf no way",
            "Once you grow a braincell, yes",
            "I don't care lol",
            "Not a chance",
            "better not tell you now >:)",
            "Concentrate and ask again.",
            "Don't count on it. Can you count?",
            "It is certain!",
            "It is decidely so.",
            "Most likely",
            "no, just like the amount of brain cells you have",
            "My (totally accurate) sources say no",
            "Outlook not so good",
            "Outlook good",
            "Reply hazy, try again",
            "Signs point to a YES!",
            "Very doubtful",
            "without a doubt",
            "yep",
            "yes - definitely, yep, i think so, maybe, no",
            "you may rely on it i guess",
            "Yes.................",
            "No",
            "Take a wild guess...",
            "Very doubtful",
            "Sure why not",
            "Without a doubt",
            "Most likely",
            "Might be possible",
            "You'll be the judge",
            "no... (╯°□°）╯︵ ┻━┻",
            "pink is the impostor! wait... what do you mean this is an 8 ball command??",
            "**E**",
            "IDK not my problem",
            r"¯\_(ツ)_/¯"
        ]

        aaaaa = random.choice(choices)

        embed = discord.Embed(
            title="The Magic 8-Ball",
            description=f"**🎱8-ball:** {aaaaa}",
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Requested by: " + ctx.author.name)
        await ctx.reply(embed=embed)

# ------------------------------------------------------------------------------------------------------------------------------------------------------
    # QUOTE COMMAND, uses a function that looks in a GIANT collection of quotes from `ZenQuotes.io` and picks a random one to return to the user.
    @commands.command(name='quote', help="Gives a random inspirational quote from a giant collection provided by ZenQuotes.io")
    async def quote(self, ctx):
        # Get a quote from the API
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]["q"] + " -" + json_data[0]["a"]

        # Check if we're sending too many requests, otherwise send.
        if quote == 'Too many requests. Obtain an auth key for unlimited access. -ZenQuotes.io':
            await ctx.send(
                "Do you seriously need more quotes? Wait 30 seconds please")  # Since there is a limit on requests, this is added to notify that it needs 30 seconds
        else:
            await ctx.send(quote)  # Send the quote that we randomly chose from ZenQuotes

# ------------------------------------------------------------------------------------------------------------------------------------------------------
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

            # We can comment this out later if needed.
            print(print_cog + print_spec + "Fun " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Fun(bot))  # Add the cog to the main class (Fun).
