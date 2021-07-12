import Bot
import GameOS


def ResetFiles():
    GameOS.FileSystem.SaveFiles()
    print(GameOS.FileSystem.LoadFiles())
    Bot.settings.Save()
    print(Bot.settings.Load())


def Run():
    game = Bot.Bot()
    game.start_game()


if __name__ == "__main__":
    Run()
    #ResetFiles()
