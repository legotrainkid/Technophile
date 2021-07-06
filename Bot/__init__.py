import discord
import asyncio

import Bot.settings


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.commands = {}

    def start_game(self):
        pass

    async def on_message(self, message):
        if message.content[0:len(settings.PREFIX)] != settings.PREFIX or message.author == self.user:
            return
        arguments = message.content[len(settings.PREFIX):].split(" ")
        if arguments[0] in self.commands:
            await self.commands[arguments[0]](arguments, message)

    async def setup_server(self, arguments : list, message : discord.Message):
        # Command: ?setup number_of_channels
        server = message.guild
        ready_cat = await server.create_category_channel("Available Computer Channels")
        new_server = {}
        for i in range(int(arguments[1])):
            name = "Computer-" + str(i)
            new_channel = await server.create_text_channel(name, category=ready_cat)
            role_name = name+"-User"
            new_role = await server.create_role(name=role_name)
            await settings.NormalOverWrite(new_channel, new_role)
            new_server[new_channel.id] = new_role.id
        print(new_server)
        settings.SERVERS[server.id] = new_server
        await message.channel.send("Your server is now set up!")

