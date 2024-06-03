import discord
import sqlite3
import util
import datalayer as dl

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        dl.checkDb(conn)

    async def on_message(self, message):
        if util.checkCommandMessage(message):
            await util.processCommand(self, message)
        print(f'Message from {message.author}: {message.content}')

    async def on_member_update(self, before, after):
        print(f'User {before.name} (id: {before.id}) updated name from {before.nick} to {after.nick}')
        channel = self.get_channel(1247015124573884515)
        await channel.send(f'User {before.name} (id: {before.id}) updated name from {before.nick} to {after.nick}')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = DiscordClient(intents=intents)
client.run('')