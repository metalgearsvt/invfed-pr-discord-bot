import discord
from discord import app_commands
import sqlite3
import username_update
import datalayer as dl

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
dl.checkDb(conn)

DISCORD_ID = 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Called when the Discord client is connected to the server and prepared to receive.
@client.event
async def on_ready():
        print(f'Logged on as {client.user}!')
        await tree.sync(guild=discord.Object(id=DISCORD_ID))

# Called when a server member's profile is updated in any way.
@client.event
async def on_member_update(before, after):
        await username_update.username_update_check(conn, client, before, after)

@tree.command(
    name="outputchannel",
    description="Select the channel to output all username history to when it happens.",
    guild=discord.Object(id=DISCORD_ID)
)
@app_commands.describe(channel="The text channel to send username changes to.")
async def outputChannel(interaction: discord.Interaction, channel: discord.TextChannel):
        dl.updateNickChannel(conn, channel.id)
        await interaction.response.send_message(f"Updated the output channel to <#{channel.id}>")

@tree.command(
        name="namehistory",
        description="Prints the history of a users nicknames.",
        guild=discord.Object(id=DISCORD_ID)
)
@app_commands.describe(user="The user to fetch the nickname history for.")
async def nameHistory(interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message(f"Retrieving <@{user.id}>'s nickname history.")
        await username_update.buildAndSendAllEmbed(conn, client, interaction.channel_id, user)

client.run('')