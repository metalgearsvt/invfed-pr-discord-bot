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
    return message.author.guild_permissions.administrator and message.content[0] == '!'

async def processCommand(client, message):
    """
    Processes an administrative command sent to the bot.

    Parameters
    ----------
    client : discord.Client
        The Discord client.
    message : Message
        The message to process.
    """
    await message.channel.send('Testing!')