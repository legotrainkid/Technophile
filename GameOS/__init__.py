from GameOS import FileSystem

COMPUTERS = []


def CreateComputer(account):
    if "file_id" in account.data:
        files = LoadFiles(account.data["file_id"])
    else:
        id = FileSystem.GenerateFileID()
        files = FileSystem.FileSystem(id, FileSystem.GenerateIpAddress())
        account.data["file_id"] = id
    new = Computer(account, files)
    COMPUTERS.append(new)
    return new


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
        self.ip = files.address

    def SaveFiles(self):
        FileSystem.ALL_FILES[self.account.data["file_id"]] = self.FILESYSTEM
        FileSystem.SaveFiles()
