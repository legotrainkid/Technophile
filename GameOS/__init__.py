from GameOS import FileSystem


def CreateComputer(account):
    if "file_id" in account.data:
        files = LoadFiles(account.data["file_id"])
    else:
        id = FileSystem.GenerateFileID()
        files = FileSystem.FileSystem(id)
        account.data["file_id"] = id
    return Computer(account, files)


def LoadFiles(sys_id):
    return FileSystem.ALL_FILES[sys_id]


class Account:
    def __init__(self, member_id, username, password):
        self.member_id = member_id
        self.username = username
        self.password = password
        self.data = {}


class Computer:
    def __init__(self, account, files):
        self.account = account
        self.FILESYSTEM = files

    def SaveFiles(self):
        FileSystem.ALL_FILES[self.account.data["file_id"]] = self.FILESYSTEM
        FileSystem.SaveFiles()
