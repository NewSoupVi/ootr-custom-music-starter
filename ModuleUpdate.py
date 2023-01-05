import os
import sys
import subprocess
import pkg_resources

local_dir = os.path.dirname(__file__)
file = os.path.join(local_dir, 'requirements.txt')

if sys.version_info < (3, 0, 0):
    raise RuntimeError("Incompatible Python Version. Use python 3.")

required = set()
    
with open(file, "r") as f:
    for line in f.readlines():
        line = line.strip()
        
        required.add(line)
        
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])