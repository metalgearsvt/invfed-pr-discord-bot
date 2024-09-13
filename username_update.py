import datalayer as dl
import discord
import datetime

async def username_update_check(conn, client: discord.Client, before, after):
    """
    This is run when a member is updated.
    The purpose is to:
        - Check that the username was updated.
        - Store old username in database.
        - Send a message with the relevant info in the configured channel.

    Parameters
    ----------
    conn : sqlite3.Connection
        The DB connection.
    client : Discord.client
        The Discord client.
    before : Discord.Member
        The previous state of the member.
    after : Discord.Member
        The current state of the member.
    """
    # If the nickname was not updated, then we can exit.
    # This was some other type of user update, and not a nickname change.
    if before.nick == after.nick:
        return
    # Store old value to database.
    dl.addNameHistory(conn, before.id, before.nick)
    # Here below, we have a nickname change event.
    nickChannel = dl.fetchConfigValue(conn, dl.CONFIG_NICK_CHANNEL)
    # If the config is not set, return.
    if not nickChannel:
        print(f'Could not fetch {dl.CONFIG_NICK_CHANNEL} value in the {dl.TABLE_CONFIG} table.')
        return
    await buildAndSendEmbed(conn, client, nickChannel, before, after)

async def buildAndSendEmbed(conn, client: discord.Client, nickChannel, before, after):
    # Fetch the channel for sending the message.
    channel = await client.fetch_channel(nickChannel)

    # Fetch the previous nicknames and format them into a string for the embed.
    previousNicks = dl.fetchLimitedNameHistory(conn, before.id)
    formattedNickList = ""
    for name in previousNicks:
        if name[0]:
            formattedNickList = formattedNickList + name[0] + "\n"

    # Build the Discord embed.
    embed = discord.Embed(description=f"**<@{before.id}>'s nickname has been updated.**\n\n**New Nickname:**\n{after.nick}\n\n**Previous Nicknames:**\n{formattedNickList}",
                      colour=0x236d9f, timestamp=datetime.datetime.now())
    embed.set_author(name=f"{before.name}", icon_url=f"{before.avatar.url}")
    embed.set_footer(text="INVICTUS INTERGALACTIC FEDERATION",
                     icon_url="https://cdn.discordapp.com/attachments/1248019126002258042/1248019142447988778/invfed.png?ex=666223e6&is=6660d266&hm=3437d4252c4aa9a6c3d98256064b59760e382739aca3b36e8d6cf4a0a712a690&")
    await channel.send(embed=embed)

async def buildAndSendAllEmbed(conn, client: discord.Client, nickChannel, user: discord.Member):
    # Fetch the channel for sending the message.
    channel = await client.fetch_channel(nickChannel)

    # Fetch the previous nicknames and format them into a string for the embed.
    previousNicks = dl.fetchUnlimitedNameHistory(conn, user.id)
    formattedNickList = ""
    for name in previousNicks:
        if name[0]:
            formattedNickList = formattedNickList + name[0] + "\n"

    # Build the Discord embed.
    embed = discord.Embed(description=f"**<@{user.id}>'s nickname history.**\n\n**Previous Nicknames:**\n{formattedNickList}",
                      colour=0x236d9f, timestamp=datetime.datetime.now())
    embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar.url}")
    embed.set_footer(text="INVICTUS INTERGALACTIC FEDERATION",
                     icon_url="https://cdn.discordapp.com/attachments/1248019126002258042/1248019142447988778/invfed.png?ex=666223e6&is=6660d266&hm=3437d4252c4aa9a6c3d98256064b59760e382739aca3b36e8d6cf4a0a712a690&")
    await channel.send(embed=embed)