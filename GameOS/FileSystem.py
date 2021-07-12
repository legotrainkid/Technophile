import pickle
import datetime
import random

ALL_FILES = {}
NEXT_ID = 11111111

DEFAULT_FILES = {"C:" : {"Documents" : {}, "Downloads" : {}, "Software" : {},
                         "System" : {"ConfigFiles" : {}, "Logs" : {}}}}

ALL_IPS = []


def SaveFiles():
    global ALL_FILES, NEXT_ID
    data = {"Files" : ALL_FILES, "ID" : NEXT_ID, "IPS" : ALL_IPS}
    with open("GameOS\\FileSystemData.data", "wb") as file:
        pickle.dump(data, file)
    print(data)


def LoadFiles():
    global ALL_FILES, NEXT_ID, ALL_IPS
    with open("GameOS\\FileSystemData.data", "rb") as file:
        data = pickle.load(file)
    ALL_FILES = data["Files"]
    NEXT_ID = data["ID"]
    ALL_IPS = data["IPS"]
    print(data)


def GenerateFileID():
    global NEXT_ID
    id = NEXT_ID
    NEXT_ID += 1
    return id


def GenerateIpAddress():
    global ALL_IPS
    while True:
        nums = []
        for i in range(10):
            nums.append(str(random.randint(1, 9)))
        ip = "19" + nums[2] + "." + "".join(nums[3:6]) + "." + "".join(nums[7:9]) + "." + nums[9]
        if ip not in ALL_IPS:
            ALL_IPS.append(ip)
            return ip


class FileSystem:
    def __init__(self, id, ip):
        self.id = id
        self.files = DEFAULT_FILES
        self.address = ip
        self.create_config_file("network", {"IP" : ip})

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

    def create_config_file(self, name, data):
        self.files["C:"]["System"]["ConfigFiles"][name+".config"] = File(data, GenerateFileID())

    def load_config_file(self, name):
        path = self.files["C:"]["System"]["ConfigFiles"]
        if name in path:
            return path[name+".config"].data
        else:
            return None


class File:
    def __init__(self, data, id):
        self.data = data
        self.id = id


if __name__ == "__main__":
    print(GenerateIpAddress())
