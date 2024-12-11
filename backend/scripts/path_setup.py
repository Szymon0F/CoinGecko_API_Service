from pathlib import Path
import sys

def setup_path():
    current_dir = Path(__file__).resolve().parent
    parent_dir = str(current_dir.parent)
    sys.path.append(parent_dir)

setup_path()