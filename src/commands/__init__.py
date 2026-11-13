from commands.ls import ls
from commands.cd import cd

COMMANDS = {
    "ls": ls,
    "cd": cd,
}

def get_command(name):
    return COMMANDS.get(name)