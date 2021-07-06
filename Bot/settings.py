import discord
import asyncio

PREFIX = "?"
SERVERs = {}


def NormalOverWrite(channel, channel_role):
    over = discord.PermissionOverwrite()
    over.general()
    await channel.set_permisions(channel.guild.default_role, overwrite=over)
    await channel.set_permisions(channel_role, overwrite=over)


async def ClosedOverWrite(channel):
    over = discord.PermissionOverwrite()
    over.pair(view_channel=False)
    await channel.set_permisions(channel.guild.default_role, overwrite=over)

