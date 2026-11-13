import argparse
import sys
from shell import Shell

def build_parser():
    parser = argparse.ArgumentParser(description="UNIX-like shell emulator")
    parser.add_argument("--vfs", required=True, help="path to the VFS file")
    parser.add_argument("--script", default=None, help="path to startup script")
    parser.add_argument("--debug", action="store_true", help="print parameters")
    return parser

def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.debug:
        print(f"vfs    = {args.vfs}")
        print(f"script = {args.script}")
    shell = Shell(vfs_path=args.vfs)
    if args.script:
        shell.run_script(args.script)
    if shell.running:
        shell.repl()
    return 0

if __name__ == "__main__":
    sys.exit(main())