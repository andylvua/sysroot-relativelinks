#!/usr/bin/python3

import sys
import os

# Take a sysroot directory and turn all the absolute symlinks and turn them into
# relative ones such that the sysroot is usable within another system.

if len(sys.argv) != 2:
    print("Usage is " + sys.argv[0] + "<directory>")
    sys.exit(1)

top_dir = sys.argv[1]
top_dir = os.path.abspath(top_dir)


def handle_link(file_path, sub_dir):
    link = os.readlink(file_path)
    if link[0] != "/":
        return
    if link.startswith(top_dir):
        return

    new_link = os.path.relpath(top_dir + link, sub_dir)

    print("\t%s replacing %s => %s" % (file_path, link, new_link))
    os.unlink(file_path)
    os.symlink(new_link, file_path)


for subdir, dirs, files in os.walk(top_dir):
    for file in files:
        filePath = os.path.join(subdir, file)
        if os.path.islink(filePath):
            handle_link(filePath, subdir)
