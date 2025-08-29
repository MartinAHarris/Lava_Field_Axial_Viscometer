"""Registers penetrometer recorder file in /etc/rc.local so that it starts
after boot. The recorder file has to be passed as command line argument. If a
line containing the same file name (but not necessarily in the same folder) is
found, the recorder file will not be registered and cleanupo needs to be done
manually.
"""
import argparse
from pathlib import Path
import os

user_id = os.getuid()
if user_id != 0:
    raise SystemError("This scipt requires root privileges")

parser = argparse.ArgumentParser()
parser.add_argument(
    "penrecorder",
    help="File to register to run at startup. (Must be an absolute path.)"
)

args = parser.parse_args()
recfile = Path(args.penrecorder).absolute()
if not recfile.exists():
    raise FileNotFoundError(f"Cannot find file {recfile}.")
fname = recfile.name

found = False
with open("/etc/rc.local", "r") as f:
    for line in f:
        if line.rstrip().endswith(fname):
            found = True
            print(
                f"register_pencode:\n"
                f"  Found {fname} in /etc/rc.local. "
                f"Will not add it a second time.\n"
            )
            break

if not found:
    with open("/etc/rc.local", "a") as f:
        print(
            f"register_pencode:\n"
            f"  Appending {str(recfile)} to /etc/rc.local"
        )
        f.write(str(recfile) + "\n")
