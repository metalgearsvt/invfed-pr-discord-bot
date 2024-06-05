import discord
import sqlite3
import user_command
import username_update
import datalayer as dl

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
dl.checkDb(conn)

class DiscordClient(discord.Client):
    # Called when the Discord client is connected to the server and prepared to receive.
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    # Called when any message is sent the bot can see.
    async def on_message(self, message):
        if user_command.checkCommandMessage(message):
            await user_command.processCommand(conn, self, message)
        print(f'Message from {message.author}: {message.content}')

    # Called when a server member's profile is updated in any way.
    async def on_member_update(self, before, after):
        await username_update.username_update_check(conn, self, before, after)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = DiscordClient(intents=intents)
client.run('')