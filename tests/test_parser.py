import sys
import os

# Чтобы тесты видели папку src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from parser import parse

def test_simple():
    assert parse("ls") == ("ls", [])

def test_with_args():
    assert parse("cd /home") == ("cd", ["/home"])

def test_blank():
    assert parse("   ") == (None, [])