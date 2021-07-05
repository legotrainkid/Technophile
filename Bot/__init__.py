import discord

import Bot.settings


class Bot(discord.Client):
    def start_game(self):
        pass

    def on_message(self, message):
        if message.content[0:len(settings.PREFIX)] != settings.PREFIX or message.author == self.user:
            return
        command = message.content[len(settings.PREFIX):].split(" ")
