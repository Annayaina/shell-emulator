from vfs import VfsError

def ls(shell, args):
    if len(args) > 1:
        raise VfsError("too many arguments")
    target = args[0] if args else "."
    parts = shell.vfs.resolve(shell.cwd, target)
    node = shell.vfs.get_node(parts)
    if not node.is_dir:
        print(node.name)
        return
    for name in sorted(node.children):
        child = node.children[name]
        print(f"{name}/" if child.is_dir else name)