import sys
from commands import get_command
from parser import parse

class Shell:
    def __init__(self, vfs_name="vfs"):
        self.vfs_name = vfs_name
        self.cwd = "/"
        self.running = True

    def prompt(self):
        return f"{self.vfs_name}:{self.cwd}$ "

    def execute(self, line):
        cmd, args = parse(line)
        if cmd is None:
            return
        if cmd == "exit":
            self.running = False
            return
        handler = get_command(cmd)
        if handler is None:
            print(f"{cmd}: command not found", file=sys.stderr)
            return
        handler(self, args)

    def repl(self):
        while self.running:
            try:
                line = input(self.prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)