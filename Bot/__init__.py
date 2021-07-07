import discord
import asyncio

import Bot.settings


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.commands = {"setup" : self.setup_server, "use" : self.claim_channel, "shutdown" : self.unclaim_channel}

    def start_game(self):
        self.run(settings.LoadToken())

    async def on_ready(self):
        print("Ready")

    async def on_message(self, message):
        print(message.content)
        if message.content[0:len(settings.PREFIX)] != settings.PREFIX or message.author == self.user:
            print("Command not recognized")
            return
        arguments = message.content[len(settings.PREFIX):].split(" ")
        print(arguments[0])
        if arguments[0] in self.commands:
            print("Running Command: " + arguments[0])
            await self.commands[arguments[0]](arguments, message)

    async def setup_server(self, arguments : list, message : discord.Message):
        # Command: ?setup number_of_channels
        server = message.guild
        ready_cat = await server.create_category_channel("Available Computer Channels")
        new_server = {}
        for i in range(int(arguments[1])):
            name = "Computer-" + str(i+1)
            new_channel = await server.create_text_channel(name, category=ready_cat)
            role_name = name+"-User"
            new_role = await server.create_role(name=role_name)
            await settings.NormalOverWrite(new_channel, new_role)
            new_server[new_channel.id] = new_role.id
        print(new_server)
        settings.SERVERS[server.id] = new_server
        await message.channel.send("Your server is now set up!")

    async def claim_channel(self, arguments, message):
        # Command: ?use
        server = message.guild
        print(3)
        print(server.id)
        print(settings.SERVERS)
        if server.id in settings.SERVERS:
            print(1)
            if message.channel.id in settings.SERVERS[server.id]:
                print(2)
                await message.author.add_roles(server.get_role(settings.SERVERS[server.id][message.channel.id]))
                await settings.ClosedOverWrite(message.channel)
                await message.channel.send("You have claimed this channel!")

    async def unclaim_channel(self, arguments, message):
        server = message.guild
        if server.id in settings.SERVERS:
            print(1)
            if message.channel.id in settings.SERVERS[server.id]:
                print(2)
                await message.author.remove_roles(server.get_role(settings.SERVERS[server.id][message.channel.id]))
                await message.channel.purge(limit=1000)
                await settings.NormalOverWrite(message.channel, server.get_role(settings.SERVERS[server.id][message.channel.id]))
                await message.channel.send("Channel available to use! Type `?use` to claim this channel!")


