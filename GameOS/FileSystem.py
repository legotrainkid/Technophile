import pickle
import datetime

ALL_FILES = {}
NEXT_ID = 11111111

DEFAULT_FILES = {"C:" : {"Documents" : {}, "Downloads" : {}, "Software" : {},
                         "System" : {"ConfigFiles" : {}, "Logs" : {}}}}


def SaveFiles():
    data = {"Files" : ALL_FILES, "ID" : NEXT_ID}
    with open("GameOS\\FileSystemData.data", "wb") as file:
        pickle.dump(data, file)


def LoadFiles():
    global ALL_FILES, NEXT_ID
    with open("GameOS\\FileSystemData.data", "rb") as file:
        data = pickle.load(file)
    ALL_FILES = data["Files"]
    NEXT_ID = data["ID"]
    print(ALL_FILES)


def GenerateFileID():
    global NEXT_ID
    id = NEXT_ID
    NEXT_ID += 1
    return id


class FileSystem:
    def __init__(self, id):
        self.id = id
        self.files = DEFAULT_FILES

    def return_files(self, path):
        files = {"Folders" : [], "Files" : []}
        path_dir = self.files
        for folder in path:
            path_dir = path_dir[folder]
        for file in path_dir:
            if type(path_dir[file]) is dict:
                files["Folders"].append(file)
            else:
                files["Files"].append(file)
        return files

    def is_valid_path(self, path):
        path = path.split("\\")
        if path[-1] == "":
            path = path[:-1]
        exists = True
        path_dir = self.files
        for folder in path:
            if folder in path_dir:
                path_dir = path_dir[folder]
            else:
                exists = False
                break
        return exists

    def create_log(self, command):
        time = str(datetime.datetime.now())
        text = command + " : " + time
        new = File(text, GenerateFileID())
        name = time + ".log"
        self.files["C:"]["System"]["Logs"][name] = new


class File:
    def __init__(self, data, id):
        self.data = data
        self.id = id


LoadFiles()

if __name__ == "__main__":
    SaveFiles()
    LoadFiles()
