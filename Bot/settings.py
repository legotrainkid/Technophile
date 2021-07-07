import discord
import asyncio
import pickle

PREFIX = "?"
SERVERS = {821517617016733736 : {862374893503905802: 862374893932249179, 862374895651389502: 862374896159031306, 862374897975558164: 862374898374541342}}


async def NormalOverWrite(channel, channel_role):
    over = discord.PermissionOverwrite()
    over.view_channel = True
    await channel.set_permissions(channel.guild.default_role, overwrite=over)
    await channel.set_permissions(channel_role, overwrite=over)


async def ClosedOverWrite(channel):
    # Function to hide the channel from the default role
    # Create a permission overwrite
    over = discord.PermissionOverwrite()
    # Set the view_channel permission to false
    over.view_channel = False
    # Set the default role permissions to the created permissions
    await channel.set_permissions(channel.guild.default_role, overwrite=over)


def LoadToken():
    # Used to load the token for the bot
    with open("Bot\\token.txt", "r") as file:
        # retrieve the token from the file
        token = file.readline()
    # return the token
    return token


def SaveServers():
    pass


def LoadServers():
    with open("Bot\\servers.data") as file:
        servers = pickle.load(file)

    return servers

