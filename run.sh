#!/usr/bin/env bash

# Start the script and display the title.
figlet Thonk-Bot Updater -f smslant

# Go to the directory with the bot if running from outside it
# cd thonk-bot || echo "Project not found!" && git clone https://github.com/TechnoShip123/thonk-bot

# UPDATER STARTS: Update the bot's code from the repository.

# If there are new changes, pull the latest and overwrite the local files (DB should be safe).
if [[ -n $(git status -s) ]]; then
    echo -e "[UPDATER]:\033[1;32 Changes found\033[0m. Retrieving changes and overwriting local files..."
    git fetch --all && git reset --hard origin/master
# Otherwise, if there aren't any new changes.
else
    echo -e "[UPDATER]:\033[1;31m No changes found\033[0m. New code was not pulled."
fi
# cd ..  # Go back to the directory outside the bot


# VALIDATOR STARTS: Check that the necessary files exist to run the bot.

# Check if the token is in the file
if [ "$(find "lib/bot" -name "token.txt")" ]; then
    echo -e "\033[0;32m[VALIDATOR]:\033[0m Token file (\033[0;36mtoken.txt\033[0m) was found!"
else
    echo -e "\033[0;31m[WARNING]: Token file (token.txt) not found!\033[0m"
    sleep 2
    exit 1
fi

# Run the bot.
echo -e "Running the bot, make sure to use\033[1;34m CTRL +\033[0m\033[1;31m A\033[0m, then type\033[1;31m D\033[0m. This will keep the screen running detached."
sleep 3  # Dramatic pause lol
screen python3.9 launcher.py || echo -e "\033[0;31m[WARNING]: Screen not detected\033[0m for running in background! Running the bot in foreground..." && python3.9 launcher.py
