import hashlib
import json
import random
from datetime import *
from typing import Optional

import asyncio
import os
import discord
import requests
from discord.ext import commands
from discord.ext.commands import *


# -------------------------------------------------------------------------------------------------------------------------------


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	# Hit/Bonk command, fun way to 'hit' others for the specified reason (defaults to no reason if nothing is provided).
	@commands.command(name="bonk", aliases=["hit"], help="'Bonk' someone with objects for specified reasons!")
	async def bonk(self, ctx, member: str, *, reason: Optional[str] = "no reason"):
		await ctx.message.delete()  # Delete the user message
		object_list = ["a train", "a bat", "some bees", "an acorn", "a truck", "a bulldozer", "a python", "a ban", "a mute", "a kick",
		               "a pie", "GitHub premium", "Octocat", "ThonkBot documentation", "a car", "Minecraft", "Mojang", "Steve", "Alex",
		               "a villager", "a diamond", "an emerald", "Pylint", "Java", "a cookie", "me", "JavaScript", "PHP", "their C drive",
		               "their computer", "some HTML code", "some CSS code", "discord.py documentation", "a wall", "a plane", "a black hole",
		               "a joke", "a wet towel", "the theory of time", "a clock", "Docker", "the Docker whale", "a turtle", "a stick",
		               "their car keys", "a pokemon"]
		if member == "<@!815078851780542484>":  # Check if it's hitting the bot
			await ctx.send(f"{ctx.author.mention} tried to bonk me, but I dodged and yeeted them!")
		elif member == ctx.author.mention:  # Check if they're hitting themselves
			await ctx.send(f"{ctx.author.mention} bonked themselves with {random.choice(object_list)} for {reason}.")
		else:  # Otherwise continue as normal
			await ctx.send(f"{ctx.author.mention} bonked {member} with {random.choice(object_list)} for {reason}.")
	
	# THE SOUP COMMAND ------------------------------------------------------------------------------------------------------------------
	@commands.command(name="soup")
	async def soup(self, ctx):
		soup_emoji = "<:soup:808428326120063007>"
		choices_no = ["Sorry, we don't have any left :/", "no :gun: :cook: "]
		choices_yes = [
			f"{soup_emoji} Here you go friend! Fresh soup from questionable places of the Mooshroom! {soup_emoji}",
			f"Here's your soup :cook: {soup_emoji}",
			f"Fresh soup! Right out of the... Just take your soup {soup_emoji}",
			f"Here it is sir! {soup_emoji}",
			f"Soup {soup_emoji} :D",
			f"Here, have your very own mooshroom soup {soup_emoji}",
			f"Here you have it {soup_emoji}",
			f"Here it is :flushed: {soup_emoji}",
			f":flushed: This one looks interesting {soup_emoji}",
			f"Soup is pog {soup_emoji}"
		]
		respond_no = random.choice(choices_no)
		respond_yes = random.choice(choices_yes)
		chance = random.randint(1, 100)
		if chance <= 1:  # If they get a 5% chance say no.
			await ctx.message.add_reaction('❌')
			await ctx.reply(respond_no)
		else:  # Have a 95% chance to say yes.
			await ctx.message.add_reaction(f"{soup_emoji}")
			await ctx.send(respond_yes)
	
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
			"It is decidedly so.",
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
			"eh",
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
	
	# ------------------------------------------------------------------------------------------------------------------------------------
	# QUOTE COMMAND, uses a function that looks in a collection of quotes from `ZenQuotes.io` and picks a random one to return to the user.
	@commands.command(name='quote', aliases=(["zenquotes"]))
	async def quote(self, ctx):
		# Get a quote from the API
		response = requests.get("https://zenquotes.io/api/random")
		json_data = json.loads(response.text)
		quote = json_data[0]["q"] + " -" + json_data[0]["a"]
		
		# Check if we're sending too many requests, otherwise send.
		if quote == 'Too many requests. Obtain an auth key for unlimited access. -ZenQuotes.io':
			await ctx.send(
				"Do you seriously need more quotes? Wait 30 seconds please")  # This triggers when we hit the request limit.
		else:
			await ctx.send(quote)  # Send the quote that we randomly chose from ZenQuotes
	
	# SAY COMMAND ------------------------------------------------------------------------------------------------------------------------
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
				newmessage = content.replace("--gifs ", "")
				newmessage = newmessage.replace("sus", "https://tenor.com/view/sus-gif-20302681")
				newmessage = newmessage.replace("slamtable", "https://tenor.com/view/kazuma_kiryu_slams_a_desk_and_leaves-gif-19004286")
				await ctx.send(newmessage)
		# Otherwise, send the message/emojis:
		else:
			# Check for emojis that we support and replace them here.
			newmessage = content.replace(":thonkhmm:", "<a:thonkhmm:820738912917520424>")
			newmessage = newmessage.replace(":stevedance:", "<a:stevedance:820417132432588812>")
			newmessage = newmessage.replace(":thonksplode:", "<a:thonksplode:820738463828934678>")
			newmessage = newmessage.replace(":stevegun:", "<:stevegun:815628826767523840>")
			newmessage = newmessage.replace(":thonkgoodbye:", "<:stevegun:815628826767523840>")
			newmessage = newmessage.replace(":nice:", "<:nice:817119421445046293>")
			newmessage = newmessage.replace(":mcgrassblock:", "<a:mcgrassblock:820298284228542484>")
			newmessage = newmessage.replace(":discordload:", "<a:discordload:801598729240444928>")
			
			await ctx.send(newmessage)
	
	# ------------------------------------------------------------------------------------------------------------------------------------
	
	@commands.command(name="ai")
	async def ai(self, ctx, *, content: str):
		# THANKS TO EGGO-PLANT FOR THE UNIQUE UUID CODE
		from lib.bot.__init__ import api_key, brain_id
		author = str(
			ctx.message.author.id).encode()  # You can provide a unique identification for users, in this case it's a hash of their ID.
		hashed_author = (hashlib.sha256(author)).hexdigest()  # Hash the Discord user ID
		user_input = content.replace(" ", "%20")
		response = requests.get(f'http://api.brainshop.ai/get?bid={brain_id}&key={api_key}&uid={hashed_author}&msg={user_input}').json()
		
		bot_response = response['cnt']
		async with ctx.message.channel.typing():
			await asyncio.sleep(0.5, 2)
		await ctx.reply(bot_response)
	
	# ------------------------------------------------------------------------------------------------------------------------------------
	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")
			# print(Bcolors.print_cog + Bcolors.print_spec + "Fun " + Bcolors.ENDC + "cog started!")


def setup(bot):  # Define the cog
	bot.add_cog(Fun(bot))  # Add the cog to the main class (Fun).
