from vfs import VfsError

def cd(shell, args):
    if len(args) > 1:
        raise VfsError("too many arguments")
    target = args[0] if args else "/"
    parts = shell.vfs.resolve(shell.cwd, target)
    node = shell.vfs.get_node(parts)
    if not node.is_dir:
        raise VfsError(f"not a directory: {target}")
    shell.cwd = parts