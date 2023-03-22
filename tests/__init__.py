
import sys
from os.path import dirname

def setup_project_path():
    sys.path.append(dirname(dirname(__file__)))
