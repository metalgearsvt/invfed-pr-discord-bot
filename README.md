# invfed-pr-discord-bot

Discord bot for the INVFED Discord.

# Bot Creation
* Go here https://discord.com/developers/applications
* Create a new application.
* Set the name / avatar to whatever.
* Installation tab: User + Guild Install, Discord Provided Link, default permissions: applications.commands, Guild install: applications.commands & bot, bot permissions: send messages.
* Bot tab: SERVER MEMBERS INTENT, MESSAGE CONTENT INTENT
* Bot tab: Reset token, enter your 2FA, copy the bot token, you will need it for the installation steps, DO NOT SHARE THIS.
* Go back to the installation tab, and copy the Discord provided link, go to it, and add it to your server.
* Make sure the bot in your server has a role that will let it see + send messages + embed in the channel you want it to spit out to.

# Installation
* Edit invfedprbot.py, client.run('') at the bottom, paste the token you got from the steps above, save file.
* Install python3
* In command, run: `python -m pip install -U discord.py`
* In command, navigate to the folder where the source code is and run: `python invfedprbot.py`

### Optional config
* In user_command.py you can edit the PREFIX variable to be whatever single character you would like. It is currently ! by default. This will determine what your messages need to start with.

# Commands
* !nickchannel #channel-name: Sets the channel that nickname changes should be sent to.