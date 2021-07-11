import discord
import asyncio
import pickle
import GameOS

PREFIX = "?"
SERVERS = {821517617016733736 : {862374893503905802: 862374893932249179,
                                 862374895651389502: 862374896159031306,
                                 862374897975558164: 862374898374541342}}
ACCOUNTS = {}
USERS = {}

command_help = [["?claim", "Claims a computer channel so that only you can see it"],
                ["?unclaim", "Purges the computer channel you are using and reopens it"],
                ["?create [username] [password]",
                 "Creates and account with the given username and password. You cannot create multiple accounts"],
                ["?login [username] [password]", "Logins to the given account (if the credentials are correct)."],
                ["?logout", "Logs out of the account you are currently logged into."],
                ["?mydrive",
                 "View the drive of the account you are currently logged into. Only works if you are logged in"],
                ["?chdir [path]",
                 "Change the directory you are in, only works if you have a drive  open"]]

EMOJIS = {"folder" : "📁", "file" : "📄"}


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


def Save():
    data = {"SERVERS": SERVERS, "ACCOUNTS": ACCOUNTS, "USERS": USERS}
    with open("Bot\\files.data", "wb") as file:
        pickle.dump(data, file)


def Load():
    with open("Bot\\files.data", "rb") as file:
        servers = pickle.load(file)

    return servers


if __name__ == "__main__":
    Save({"SERVERS": SERVERS, "ACCOUNTS": ACCOUNTS, "USERS": USERS})
    print(Load())
