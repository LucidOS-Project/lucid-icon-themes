#!/usr/bin/env python3
"""Check the themes as files, before anything packages or installs them.

An icon theme is a set of directories plus an index into them, and the index is
the part that goes wrong silently. index.theme was once written with backslash
line continuations, which the key-file format does not have: GKeyFile rejected
the whole file, so Directories= AND Inherits= were both unreadable and every
icon fell through to hicolor. Nothing reported an error -- the theme simply
stopped working.

So this parses the index the way GTK does, with GKeyFile, rather than with a
tolerant parser that would accept what GTK rejects.

Usage: check_themes.py <tree root>
"""
import os
import sys

import gi
from gi.repository import GLib

THEMES = ("Lucid", "Lucid-Dark", "Lucid-Everything")

failures = []


def fail(msg):
    failures.append(msg)
    print(f"  FAIL {msg}")


def check_index(root, theme):
    path = os.path.join(root, theme, "index.theme")
    if not os.path.isfile(path):
        fail(f"{theme}: no index.theme")
        return
    kf = GLib.KeyFile()
    try:
        kf.load_from_file(path, GLib.KeyFileFlags.NONE)
    except GLib.Error as e:
        fail(f"{theme}: GKeyFile rejects index.theme: {e.message}")
        return
    try:
        dirs = [d.strip() for d in kf.get_string("Icon Theme", "Directories").split(",") if d.strip()]
    except GLib.Error:
        fail(f"{theme}: index.theme has no readable Directories=")
        return
    try:
        inherits = kf.get_string("Icon Theme", "Inherits")
    except GLib.Error:
        inherits = ""

    missing = [d for d in dirs if not os.path.isdir(os.path.join(root, theme, d))]
    print(f"  {theme:18} {len(dirs):>3} directories, "
          f"{len(missing)} missing, Inherits={inherits or '(none)'}")
    if not dirs:
        fail(f"{theme}: Directories= is empty")
    for d in missing[:10]:
        fail(f"{theme}: Directories= names {d}, which does not exist")

    # Every directory must also declare a size, or GTK warns and the entries in
    # it are not usable at the size that was asked for.
    for d in dirs:
        if not kf.has_group(d):
            fail(f"{theme}: {d} is listed in Directories= but has no [{d}] group")
            continue
        icons = [n for n in os.listdir(os.path.join(root, theme, d))
                 if n.lower().endswith((".svg", ".png", ".xpm"))] \
            if os.path.isdir(os.path.join(root, theme, d)) else []
        if not icons:
            # An empty directory is not merely useless here. Two of them only
            # ever held macOS metadata, so they existed on the machine that
            # generated this list and not in a fresh clone -- which is a check
            # that passes locally and fails in CI, the least useful kind.
            fail(f"{theme}: {d} is declared but contains no icons")
        try:
            kf.get_integer(d, "Size")
        except GLib.Error:
            # This is what GTK complains about at every application start:
            # "Theme directory 16x16/ of theme Lucid has no size field".
            fail(f"{theme}: [{d}] has no readable Size field")


def check_files(root):
    """Two kinds of file that must never ship.

    Zero-filled: four icons were the right length and entirely NUL, which is
    what an interrupted write leaves behind. They are not images and nothing
    reports them as broken until something tries to draw one.

    macOS metadata: these assets have passed through a Mac, and debian/install
    copies whole directories, so an AppleDouble sidecar beside every file ends
    up in the .deb.
    """
    zero, junk, total = [], [], 0
    for theme in THEMES:
        for dirpath, _, names in os.walk(os.path.join(root, theme)):
            for n in names:
                p = os.path.join(dirpath, n)
                if os.path.islink(p):
                    continue
                total += 1
                if n.startswith("._") or n == ".DS_Store":
                    junk.append(p)
                    continue
                try:
                    with open(p, "rb") as fh:
                        data = fh.read()
                except OSError as e:
                    fail(f"unreadable: {p}: {e}")
                    continue
                if data and not any(data):
                    zero.append(p)
    print(f"  {total} files checked (symlinks excluded)")
    for p in zero[:10]:
        fail(f"zero-filled: {os.path.relpath(p, root)}")
    for p in junk[:10]:
        fail(f"macOS metadata: {os.path.relpath(p, root)}")
    if len(zero) > 10:
        fail(f"...and {len(zero) - 10} more zero-filled files")
    if len(junk) > 10:
        fail(f"...and {len(junk) - 10} more macOS metadata files")


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"checking themes under {os.path.abspath(root)}")
    for theme in THEMES:
        check_index(root, theme)
    check_files(root)
    if failures:
        print(f"\n{len(failures)} problem(s)")
        return 1
    print("\nall themes parse, every declared directory exists, no unshippable files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
