import subprocess
import csv
import os
import shutil
import sys
import uuid
from dotenv import dotenv_values
import os
import stat

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)      


PYTHON_EXE = sys.executable
SCRIPTS = {}


def getScripts():
    with open('discord/bots/bots.txt', 'r', newline='', encoding='utf-8') as botFile:
        reader = csv.reader(botFile, delimiter=":")
        for bot in reader:
            id = bot[0]
            name = bot[1]
            description = bot[2]
            filepath = bot[3]
            if os.path.isfile(filepath):
                SCRIPTS[id] = (name, description, filepath)
                print(f"Loaded [{id}] {name} - {description} at {filepath}")
            else:
                print(f"Could not find script {filepath}. Skipping")

def updateScriptsFile():
    with open('discord/bots/bots.txt', "w", newline='', encoding='utf-8') as botFile:
        writer = csv.writer(botFile, delimiter=":")
        for id in SCRIPTS:
            (name, description, path) = SCRIPTS[id]
            writer.writerow([id, name, description, path])

getScripts()

def saveEnvConfig(envPath, envConfig):
    with open(envPath, 'w', encoding='utf-8') as envFile:
        envFile.write(envConfig)

def readEnvConfig(envPath):
    with open(envPath, 'r', encoding='utf-8') as envFile:
        return envFile.read()

class BotProcess:
    def __init__(self, script_key: str):
        if script_key in SCRIPTS:
            self.id = script_key
            (self.name, self.description, self.cmd) = SCRIPTS[script_key]
            self.subproc = None
        else:
            self.cmd = ""
            self.name = "Unauthorized"
            self.subproc = None

    def __str__(self):
        return f"[{self.id}] {self.name} : {self.description}"

    def is_running(self):
        if self.subproc is None:
            return False
        self.subproc.poll()
        return self.subproc.returncode is None

    def start(self):
        if self.is_running():
            return
        self.subproc = subprocess.Popen(
            args=[PYTHON_EXE, self.cmd], shell=False)

    def kill(self):
        if self.subproc is None:
            return
        if self.is_running():
            self.subproc.kill()
            self.subproc.wait()

    def restart(self):
        if self.subproc is None:
            self.start()
        else:
            self.kill()
            self.start()


bots = {}
for id in SCRIPTS:
    bots[id] = BotProcess(id)

def add_bot(github_url : str, bot_name : str, bot_description : str, entry_file : str, env_config):
    bot_name = bot_name.replace(":", " ").replace("/", "").replace("<", "").replace(">", "").replace("\"", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace("\n", " ")
    bot_description.replace(":", " ").replace("\n", " ")
    if "/" in entry_file or "\\" in entry_file:
        raise ValueError
    
    clone = subprocess.run(["git", "-C", "./discord/bots", "clone", github_url, bot_name])
    clone.check_returncode()

    id = str(uuid.uuid4())
    path = "./discord/bots/" + bot_name + "/"
    SCRIPTS[id] = (bot_name, bot_description, path + entry_file)
    updateScriptsFile()
    
    saveEnvConfig(path + ".env", env_config)
    
    bots[id] = BotProcess(id)

def pull_bot(id):
    name = bots[id].name
    path = "./discord/bots/" + name
    pull = subprocess.run(["git", "-C", path, "pull"])
    pull.check_returncode()

    if bots[id].is_running():
        bots[id].restart()

def update_env(id, envConfig):
    name = bots[id].name
    path = "./discord/bots/" + name + "/.env"
    saveEnvConfig(path, envConfig)

    if bots[id].is_running():
        bots[id].restart()

def get_env(id):
    name = bots[id].name
    path = "./discord/bots/" + name + "/.env"
    return readEnvConfig(path)

def remove_bot(id):
    name = bots[id].name
    path = "./discord/bots/" + name

    kill(id)
    del bots[id]
    del SCRIPTS[id]
    updateScriptsFile()

    rmtree(path)


def get_bots():
    return bots.values()


def kill(id):
    if str(id) in bots:
        bots[str(id)].kill()


def start(id):
    if str(id) in bots:
        bots[str(id)].start()


def killall():
    for bot in bots.values():
        bot.kill()
