import discord
import asyncio

import Bot.settings
import GameOS


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.commands = {"setup" : self.setup_server,
                         "claim" : self.claim_channel,
                         "unclaim" : self.unclaim_channel,
                         "create" : self.create_account,
                         "login" : self.user_login,
                         "logout" : self.user_logout,
                         "help" : self.help}
        self.data = {}

    def start_game(self):
        data = settings.Load()
        settings.SERVERS = data["SERVERS"]
        settings.ACCOUNTS = data["ACCOUNTS"]
        settings.USERS = data["USERS"]
        self.run(settings.LoadToken())

    def save(self):
        settings.Save({"SERVERS": settings.SERVERS, "ACCOUNTS": settings.ACCOUNTS, "USERS": settings.USERS})

    async def on_ready(self):
        print("Ready")

    async def on_message(self, message):
        if message.content[0:len(settings.PREFIX)] != settings.PREFIX or message.author == self.user:
            return

        arguments = message.content[len(settings.PREFIX):].split(" ")

        print("Running Command: " + arguments[0])
        if arguments[0] in self.commands:
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
        self.save()
        await message.channel.send("Your server is now set up!")

    async def claim_channel(self, arguments, message):
        # Command: ?use
        server = message.guild

        if server.id in settings.SERVERS:
            if message.channel.id in settings.SERVERS[server.id]:
                await message.author.add_roles(server.get_role(settings.SERVERS[server.id][message.channel.id]))
                await settings.ClosedOverWrite(message.channel)
                await message.channel.send("You have claimed this channel!")

    async def unclaim_channel(self, arguments, message):
        server = message.guild
        if server.id in settings.SERVERS:
            if message.channel.id in settings.SERVERS[server.id]:
                await message.author.remove_roles(server.get_role(settings.SERVERS[server.id][message.channel.id]))
                await message.channel.purge(limit=1000)
                await settings.NormalOverWrite(message.channel,
                                               server.get_role(settings.SERVERS[server.id][message.channel.id]))
                await message.channel.send("Channel available to use! Type `?use` to claim this channel!")

    async def create_account(self, arguments, message):
        if message.author.id not in settings.USERS:
            print("Creating account")
            account = GameOS.Account(message.author.id, arguments[1], arguments[2])
            settings.ACCOUNTS[arguments[1]] = account
            settings.USERS[message.author.id] = arguments[1]
            await message.channel.send("Account successfully created! Welcome " + arguments[1])
            await self.user_login(arguments, message)
        else:
            await message.channel.send(
                "You already have an account created! Your username is " + settings.USERS[message.author.id])
        self.save()

    async def user_login(self, arguments, message):
        logged_in = False
        if arguments[1] in settings.ACCOUNTS:
            print(1)
            account = settings.ACCOUNTS[arguments[1]]
            if account.password == arguments[2]:
                print(2)
                self.data[message.author.id] = {"ACCOUNT" : account}
                await message.channel.send("Successfully logged in! Welcome back!")
                logged_in = True
        if not logged_in:
            await message.channel.send("Your username or password is incorrect!")

    async def user_logout(self, arguments, message):
        if message.author.id in self.data:
            del self.data[message.author.id]
            await message.channel.send("You have been logged out!")
        else:
            await message.channel.send("You aren't logged in to any accounts!")

    async def help(self, arguments, message):
        embed = discord.Embed()
        for comnd in settings.command_help:
            embed.add_field(name=comnd[0], value=comnd[1], inline=False)
        await message.channel.send(embed=embed)


