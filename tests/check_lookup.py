#!/usr/bin/env python3
"""Resolve icons through the themes as GTK will, against an installed tree.

check_themes.py reads the files. This asks the question a desktop actually
asks -- "give me an icon for this name" -- and checks which file comes back,
because the interesting failures are all about *which* file wins:

  - Lucid does not draw icons for third-party applications and never will. It
    inherits Lucid-Everything for those. If Inherits= stops being readable,
    every one of them silently falls through to hicolor and the desktop looks
    like a stock Ubuntu with three custom icons.
  - Where Lucid *does* have its own icon, it has to beat the one it inherits.
    Lucid's own folder.svg lost to Lucid-Everything's for as long as
    scalable/places was missing from Directories=.

Needs no display: GtkIconTheme resolves without one.

Usage: check_lookup.py <search path, colon separated>
"""
import sys

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

# theme, icon name, the directory the winning file must be inside, why
CASES = [
    ("Lucid", "org.gnome.Nautilus", "/Lucid/", "Lucid draws this one itself"),
    ("Lucid", "folder", "/Lucid/", "its own folder must beat the inherited one"),
    ("Lucid", "user-home", "/Lucid/", "as above"),
    ("Lucid", "google-chrome", "/Lucid-Everything/", "the inherit chain, which is the whole point of it"),
    ("Lucid", "vscode", "/Lucid-Everything/", "as above"),
    ("Lucid-Dark", "org.gnome.Nautilus", "/Lucid-Dark/", "the dark theme draws this one itself"),
]

# Names that must NOT resolve, so a pass means something. Without this the
# suite would still pass if every lookup silently returned image-missing.
MUST_NOT_RESOLVE = ["lucid-no-such-icon-cdd0e1f2"]


def lookup(theme_name, name, search_path):
    theme = Gtk.IconTheme.new()
    theme.set_search_path(search_path)
    theme.set_theme_name(theme_name)
    paintable = theme.lookup_icon(name, None, 128, 1, Gtk.TextDirection.NONE,
                                  Gtk.IconLookupFlags.FORCE_REGULAR)
    f = paintable.get_file() if paintable else None
    return f.peek_path() if f is not None else None


def main():
    search_path = (sys.argv[1] if len(sys.argv) > 1 else "/usr/share/icons").split(":")
    print(f"resolving against {':'.join(search_path)}")
    failures = 0

    for theme, name, expect, why in CASES:
        path = lookup(theme, name, search_path)
        ok = path is not None and expect in path
        print(f"  [{'ok' if ok else 'FAIL'}] {theme:11} {name:20} -> {path or '(image-missing)'}")
        if not ok:
            print(f"         expected a file inside {expect} -- {why}")
            failures += 1

    for name in MUST_NOT_RESOLVE:
        path = lookup("Lucid", name, search_path)
        ok = path is None
        print(f"  [{'ok' if ok else 'FAIL'}] control     {name:20} -> {path or '(image-missing, as it should be)'}")
        if not ok:
            print("         a name that exists nowhere resolved to a file, so these "
                  "checks cannot be trusted to fail")
            failures += 1

    if failures:
        print(f"\n{failures} lookup(s) resolved to the wrong place")
        return 1
    print("\nevery icon resolves where it should, and a name that exists nowhere still does not")
    return 0


if __name__ == "__main__":
    sys.exit(main())
