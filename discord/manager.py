import subprocess
import csv
import os
import sys

PYTHON_EXE = sys.executable
SCRIPTS = {}


def getScripts():
    with open('discord/bots.txt', 'r') as botFile:
        reader = csv.reader(botFile, delimiter=":")
        for bot in reader:
            id = bot[0]
            name = bot[1]
            description = bot[2]
            filepath = bot[3]
            if os.path.isfile(filepath):
                SCRIPTS[id] = (name, description, filepath)
                print(f"Loaded [{id}] {name} at {filepath}")
            else:
                print(f"Could not find script {filepath}. Skipping")


getScripts()


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

    def restart(self):
        if self.subproc is None:
            self.start()
        else:
            self.kill()
            self.start()


bots = {}
for id in SCRIPTS:
    bots[id] = BotProcess(id)


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
