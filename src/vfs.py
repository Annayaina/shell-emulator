"""In-memory virtual file system loaded from XML."""
import base64
import xml.etree.ElementTree as ET

DEFAULT_FILE_MODE = 0o644
DEFAULT_DIR_MODE = 0o755

class VfsError(Exception):
    """Raised on VFS-related failures."""

class Node:
    """A node (file or directory) of the VFS tree."""
    
    def __init__(self, name, is_dir=False):
        self.name = name
        self.is_dir = is_dir
        self.mode = DEFAULT_DIR_MODE if is_dir else DEFAULT_FILE_MODE
        self.children = {}
        self.content = b""

class VFS:
    """Virtual file system kept entirely in memory."""
    
    def __init__(self):
        self.root = Node("/", is_dir=True)

    def load(self, path):
        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            raise VfsError(f"file not found: {path}")
        except ET.ParseError as exc:
            raise VfsError(f"invalid XML: {exc}")
        self.root = Node("/", is_dir=True)
        self._populate(self.root, tree.getroot())

    def _populate(self, node, element):
        for child in element:
            if child.tag == "dir":
                sub = Node(child.get("name"), is_dir=True)
                self._populate(sub, child)
                node.children[sub.name] = sub
            elif child.tag == "file":
                sub = Node(child.get("name"))
                sub.content = self._decode(child)
                node.children[sub.name] = sub

    @staticmethod
    def _decode(element):
        text = element.text or ""
        if element.get("encoding") == "base64":
            return base64.b64decode(text)
        return text.encode()

    def resolve(self, cwd_parts, path):
        parts = [] if path.startswith("/") else list(cwd_parts)
        for part in path.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)
        return parts

    def get_node(self, parts):
        current = self.root
        for part in parts:
            if not current.is_dir:
                raise VfsError(f"not a directory: {part}")
            if part not in current.children:
                raise VfsError(f"no such file or directory: {part}")
            current = current.children[part]
        return current