![Library - Discord.py](https://img.shields.io/badge/Library-Discord.py-informational?style=for-the-badge&logo=discord&logoColor=blurple&link=https://github.com/Rapptz/discord.py)
![Lines of code](https://img.shields.io/tokei/lines/github/TechnoShip123/thonk-bot?style=for-the-badge&label=Total%20Lines&logo=pycharm&logoColor=lightgreen)
![GitHub language count](https://img.shields.io/github/languages/count/TechnoShip123/thonk-bot?label=Languages&logo=python&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/TechnoShip123/thonk-bot?logo=gnu&style=for-the-badge)
[![Website](https://img.shields.io/website?down_color=lightgrey&down_message=Offline&label=Website&logo=html5&style=for-the-badge&up_color=green&up_message=Online&url=https%3A%2F%2Fthonkbot.zetasj.com)](https://thonkbot.zetasj.com)

# Thonk Bot

### About
The source code for a Discord bot built on Python and run on Docker, that I am creating to learn more about the 
[discord.py](https://discordpy.readthedocs.io/en/latest/) rewrite, ~~as well as an excuse to do something when I'm
bored.~~

I'm mainly using the [discord.py library](https://pypi.org/project/discord.py/), and experimenting with 
[PyNaCl](https://pypi.org/project/PyNaCl/) for voice support.


As of right now, **I do *not* plan on making my bot for public use**, so I will not be providing a link to invite the 
bot to servers. However, this may change later on.


If you would like to see more projects from me, make sure to check out my [GitHub](https://github.com/TechnoShip123)!

The bot's documentation can be found [here](https://thonkbot.zetasj.com).

### Running with Docker

#### Dockerfile
I have already created a [`Dockerfile`](https://github.com/TechnoShip123/thonk-bot/blob/master/Dockerfile) that can be
used to build the Docker container which will run the bot. It does the following:
1) Pulls the Python 3 Base Image from the Docker Repository. 
2) Sets the working directory to `/usr/src/app`. 
3) Copies all the program files to the working directory.
4) Installs all the package dependencies required for the project 
   (See [`requirements.txt`](https://github.com/TechnoShip123/thonk-bot/blob/master/requirements.txt))
5) The `CMD` and `ENTRYPOINT` instructions tell the container to run the bot
   ([`launcher.py`](https://github.com/TechnoShip123/thonk-bot/blob/master/launcher.py)) when the container starts.

#### Building & Running
First check if docker is installed with `docker --version` (`docker-compose --version` or `docker ps` might be needed
instead.) In case Docker is not installed, install it with [this guide](https://docs.docker.com/engine/install/). Once
it is installed, you can use the 
[`docker_setup.sh`](https://github.com/TechnoShip123/thonk-bot/blob/master/docker_setup.sh) or 
[`docker_setup.bat`](https://github.com/TechnoShip123/thonk-bot/blob/master/docker_setup.bat) scripts that I have 
created to automatically build the image, create a `thonk-bot` container, and run container.

### Running the bot
#### Prerequisites & Dependencies
- [Python 3.9.0+](https://www.python.org/downloads/release/python-3-9-0) 
  ([3.8.5+](https://www.python.org/downloads/release/python-3-8-5) may work but is not recommended)
- All packages listed in [`requirements.txt`](https://github.com/TechnoShip123/thonk-bot/blob/master/requirements.txt)
- [Docker/Docker.io](https://docs.docker.com/engine/install/) (_Optional_, used for 
  [running with docker](https://github.com/TechnoShip123/thonk-bot#running-with-docker))



All private bot & API info are stored in an Environment file (`.env`). Create it in `thonk-bot/lib/bot/.env` and make
sure that the following are available in the file:
- Token
- Prefix
- Brainshop API (API KEY)
- Brainshop API (BRAIN ID)

If you're unsure of what to do, just paste the following into the file (make sure to replace the placeholders with the proper information!):

```python
TOKEN="<TOKEN GOES HERE>"
PREFIX="<PREFIX GOES HERE>"
API_KEY="<BRAINSHOP API KEY GOES HERE>"
BRAIN_ID="<BRAINSHOP BRAIN ID GOES HERE>"
```

The `TOKEN` is the bot key that you generate from your application in the Discord Developer page. This bot will also
contain code for slash-commands, so you will need to make sure your bot app has access to them.


### License/Modification
If you plan on using part of or even all of this code for your own bots, you are welcome to do so and modify it as well.
However, I ask that you credit me and keep the `LICENSE` file intact to comply with the 
[GNU GPL v3 license](https://github.com/TechnoShip123/Thonk-Bot/blob/master/LICENSE). It may seem annoying, but it helps
ensure that the work I put into this does not go to waste. Thank you for understanding!
