import datalayer as dl
import re

PREFIX = '!'

CHANNEL = "nickchannel"
CHANNEL_DOC = f'{CHANNEL} command: Updates the channel to output nickname changes to. Usage: !{CHANNEL} #channel-to-use'
async def updateChannel(conn, message, channel):
    # Check to make sure the user linked a channel.
    # Channels are linked like this in plaintext <#12345678901234567>
    if not bool(re.match(r'^<\#\d*\>$', channel)):
        await message.channel.send(CHANNEL_DOC)
        return
    # Remove all characters from channel that are not digits 0-9.
    channel_num = ''.join(filter(str.isdigit, channel))
    dl.updateNickChannel(conn, channel_num)
    await message.channel.send(f'Updated nick channel to {channel}')

NICKHISTORY = "nickhistory"
NICKHISTORY_DOC = f'{NICKHISTORY} command: Prints a history of the tagged users nick history. Usage: !{NICKHISTORY} @user123'
async def usernameHistory(conn, message, user):
    await message.channel.send(f'Printing nick history for {user}')

def checkCommandMessage(message):
    """
    Checks a Discord Message object to see if it was sent from
    an administrator, and the message starts with !.

    Parameters
    ----------
    message : Message
        The message to check.

    Returns
    -------
    bool
        True if the message starts with ! and sent by an administrator.
    """
    return message.author.guild_permissions.administrator and message.content[0] == PREFIX

async def processCommand(conn, client, message):
    """
    Processes an administrative command sent to the bot.

    Parameters
    ----------
    conn : sqlite3.Connection
        The database connection.
    client : discord.Client
        The Discord client.
    message : Message
        The message to process.
    """
    # Remove the prefix from the command.
    full_command = message.content[1:]
    # Split the command into tokens separated by spaces.
    command_list = full_command.split()
    # Check to make sure there are actually commands here.
    if command_list:

        # Check if the command sent was the "channel" command.
        # !channel 907543980579384
        if command_list[0].lower() == CHANNEL:
            # Send command info if the improper amount of args are supplied.
            if len(command_list) != 2:
                await message.channel.send(CHANNEL_DOC)
                return
            # Pass the first argument as the channel.
            await updateChannel(conn, message, command_list[1])

        # Check if the command sent was the "history" command.
        # !nickhistory @poop
        elif command_list[0].lower() == NICKHISTORY:
            if len(command_list) != 2:
                await message.channel.send(NICKHISTORY_DOC)
                return
            # Pass the first argument as the user.
            usernameHistory(conn, message, command_list[1])