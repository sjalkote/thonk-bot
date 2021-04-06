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


# -------------------------------------------------------------------------------------------------------------------------------


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hit/Bonk command, fun way to 'hit' others for the specified reason (defaults to no reason if nothing is provided).
    @commands.command(name="bonk", aliases=["hit"], help="'Bonk' someone with objects for specified reasons!")
    async def bonk(self, ctx, member: str, *, reason: Optional[str] = "no reason"):
        await ctx.message.delete()  # Delete the user message
        object_list = ["a train", "a bat", "some bees", "an acorn", "a truck", "a bulldozer", "a python", "a ban", "a mute", "a kick", "a pie", "GitHub premium", "Octocat",
                       "ThonkBot documentation", "a car", "Minecraft", "Mojang", "Steve", "Alex", "a villager", "a diamond", "an emerald", "Pylint", "Java", "a cookie",
                       "me", "JavaScript", "PHP", "their C drive", "their computer", "some HTML code", "some CSS code", "discord.py documentation", "a wall", "a plane",
                       "a black hole", "a joke", "a wet towel", "the theory of time", "a clock", "Docker", "the Docker whale", "a turtle", "a stick", "their car keys", "a pokemon"]
        if member == "<@!815078851780542484>":  # Check if it's hitting the bot
            await ctx.send(f"{ctx.author.mention} tried to bonk me, but I dodged and yeeted them!")
        elif member == ctx.author.mention:  # Check if they're hitting themseleves
            await ctx.send(f"{ctx.author.mention} bonked themselves with {random.choice(object_list)} for {reason}.")
        else:  # Otherwise continue as normal
            await ctx.send(f"{ctx.author.mention} bonked {member} with {random.choice(object_list)} for {reason}.")

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
    @commands.command(name="8ball", aliases=["eightball"], help="Just like a real 8 ball!")
    async def eightball(self, ctx, *question):
        color = int("{:06x}".format(random.randint(0, 0xFFFFFF)), 16)  # RANDOM EMBED COLOR! Makes the embed color random each time!

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
            "yes - definitely, yep, I think so, maybe, no",
            "you may rely on it I guess",
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
            "red is the impostor! wait... what do you mean this is an 8 ball command??",
            "**E.**",
            "IDK not my problem",
            r"¯\_(ツ)_/¯"
        ]

        ball_choice = random.choice(choices)

        # Make sure they actually asked a question, otherwise say that they didn't.
        if not question:
            embed = discord.Embed(
                title="The Magic 8-Ball",
                description=f"**🎱8-ball:** If you have the sense to ask a question then I'll consider answering you.",
                color=color,
                timestamp=datetime.utcnow()
            )
        else:
            embed = discord.Embed(
                title="The Magic 8-Ball",
                description=f"**🎱8-ball:** {ball_choice}",
                color=color,
                timestamp=datetime.utcnow()
            )

        embed.set_footer(text="Requested by: " + ctx.author.name)
        await ctx.reply(embed=embed)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    # QUOTE COMMAND, uses a function that looks in a GIANT collection of quotes from `ZenQuotes.io` and picks a random one to return to the user.
    @commands.command(name='quote', aliases=(["zenquotes"]))
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

    # SAY COMMAND ------------------------------------------------------------------------------------------------------------------------------------------
    @commands.command(name="say", aliases=["nitro", "emoji", "gif"])
    async def say(self, ctx, *, content: str):  # Put the wildcard before content to capture everything after the prefix
        await ctx.message.delete()
        avail_emojis = "<a:thonkhmm:820738912917520424> <a:stevedance:820417132432588812> <a:thonksplode:820738463828934678> " \
                       "<:stevegun:815628826767523840> <:nice:817119421445046293> <a:mcgrassblock:820298284228542484> " \
                       "<a:discordload:801598729240444928>"
        avail_gifs = "`sus`, `slamtable`"

        # If it's listing emojis
        if content == "--emojis":
            embed = discord.Embed(title="Emojis", url="https://thonkbot.zetasj.com", color=0x73ff00)
            embed.add_field(name="Available Emojis: ", value=avail_emojis)
            embed.set_footer(text="Requested by: " + str(ctx.author))
            await ctx.send(embed=embed)
        # If it's a gif:
        elif content.startswith("--gifs"):
            # If it's listing the available gifs:
            if content == "--gifs":
                embed = discord.Embed(title="Gifs", url="https://thonkbot.zetasj.com", color=0x00bfff)
                embed.add_field(name="Available Gifs:", value=avail_gifs)
                embed.set_footer(text="Requested by: " + str(ctx.author))
                await ctx.send(embed=embed)
            # Otherwise, get the gif they want to send and send it.
            else:
                newMessage = content.replace("--gifs ", "")
                newMessage = newMessage.replace("sus", "https://tenor.com/view/sus-gif-20302681")
                newMessage = newMessage.replace("slamtable", "https://tenor.com/view/kazuma_kiryu_slams_a_desk_and_leaves-gif-19004286")
                await ctx.send(newMessage)
        # Otherwise, send the message/emojis:
        else:
            # Check for emojis that we support and replace them here.
            newMessage = content.replace(":thonkhmm:", "<a:thonkhmm:820738912917520424>")
            newMessage = newMessage.replace(":stevedance:", "<a:stevedance:820417132432588812>")
            newMessage = newMessage.replace(":thonksplode:", "<a:thonksplode:820738463828934678>")
            newMessage = newMessage.replace(":stevegun:", "<:stevegun:815628826767523840>")
            newMessage = newMessage.replace(":thonkgoodbye:", "<:stevegun:815628826767523840>")
            newMessage = newMessage.replace(":nice:", "<:nice:817119421445046293>")
            newMessage = newMessage.replace(":mcgrassblock:", "<a:mcgrassblock:820298284228542484>")
            newMessage = newMessage.replace(":discordload:", "<a:discordload:801598729240444928>")

            await ctx.send(newMessage)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
            # print(bcolors.print_cog + bcolors.print_spec + "Fun " + bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
    bot.add_cog(Fun(bot))  # Add the cog to the main class (Fun).
