import os
import sys
from commands import get_command
from parser import parse
from vfs import VfsError

class Shell:
    def __init__(self, vfs, vfs_path):
        self.vfs = vfs
        self.vfs_path = vfs_path
        self.cwd = []
        self.running = True

    def prompt(self):
        name = os.path.basename(self.vfs_path) or "vfs"
        cwd = "/" + "/".join(self.cwd)
        return f"{name}:{cwd}$ "

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
        try:
            handler(self, args)
        except (VfsError, ValueError) as exc:
            print(f"{cmd}: {exc}", file=sys.stderr)

    def run_script(self, path):
        try:
            with open(path, encoding="utf-8") as stream:
                lines = stream.readlines()
        except OSError as exc:
            print(f"script error: {exc}", file=sys.stderr)
            return
        for line in lines:
            if not self.running:
                break
            text = line.rstrip("\n")
            if not text.strip() or text.lstrip().startswith("#"):
                continue
            print(f"{self.prompt()}{text}")
            self.execute(text)

    def repl(self):
        while self.running:
            try:
                line = input(self.prompt())
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)