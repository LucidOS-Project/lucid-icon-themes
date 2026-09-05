# Licensing

This repository ships three icon themes under **two different licences**. The
root `LICENSE` file is the text of one of them, not a statement about all of
them; this file is the map.

| Path | Licence | Copyright |
|---|---|---|
| `Lucid/` | CC-BY-NC-SA-4.0 | 2025-2026 Javid Medina / Lucid Devices |
| `Lucid-Dark/` | CC-BY-NC-SA-4.0 | 2025-2026 Javid Medina / Lucid Devices |
| `Lucid-Everything/` | **GPL-3.0** | vinceliuice and contributors |
| the two `scalable/devices/drive-harddisk.svg` | **neither** -- used by permission | oviotti |
| everything else (packaging, docs) | CC-BY-NC-SA-4.0 | 2025-2026 Javid Medina / Lucid Devices |

`LICENSE` at the root is the CC-BY-NC-SA-4.0 text. It applies to `Lucid`,
`Lucid-Dark` and the packaging -- not to `Lucid-Everything`, and not to the
icons contributed by oviotti, which sit inside the first two directories under
their author's own terms.

## Why the split exists

`Lucid` and `Lucid-Dark` are original LucidOS artwork. They do not, and never
will, cover the thousands of third-party applications a desktop has to draw
icons for, so `Lucid` inherits `Lucid-Everything`, which does.

`Lucid-Everything` is not LucidOS artwork. It is a renamed copy of
[WhiteSur-icon-theme](https://github.com/vinceliuice/WhiteSur-icon-theme) by
vinceliuice, which is GPL-3.0. See `Lucid-Everything/COPYING` for the licence
and `Lucid-Everything/AUTHORS` for the attribution and the list of changes.

## Icons used by permission rather than by licence

The README credits the "Aquatic Drives" icons to
[oviotti](https://www.deviantart.com/oviotti), included with the author's
express permission, and states that they are not covered by the LucidOS
artwork licence. That is a third arrangement, not a third licence: permission
given to this project is not a grant to everyone who receives a copy of it, and
the CC-BY-NC-SA-4.0 text at the root cannot speak for work whose author has not
placed it under those terms.

It is two files, and they are the same artwork twice:

    Lucid-Dark/scalable/devices/drive-harddisk.svg   oviotti's, unmodified
    Lucid/scalable/devices/drive-harddisk.svg        the same drive, with the
                                                    LucidOS mark laid over it

The second is a derivative, not a separate work -- same body, same chrome base,
same indicator, rendered side by side to check. A derivative is still governed
by the terms the original was received under, so both lines are listed rather
than only the untouched one.

Nothing else in `Lucid/` or `Lucid-Dark/` is affected. The other three device
icons -- `drive-multidisk`, `drive-optical`, `drive-removable-media` -- are
LucidOS's own and are covered by the root licence like the rest of those
directories.

## Why the root licence cannot cover all of it

The GPL-3.0 does not permit adding restrictions to the work it covers.
"NonCommercial" is a restriction. So a single root CC-BY-NC-SA file applied to
the whole tree would not relicense `Lucid-Everything` -- it would simply be a
term the GPL forbids, which is why the two are stated separately here and in
`debian/copyright` rather than in one place with one answer.

## The split is a package boundary, not just a paragraph

This file describes the licences. `debian/` enforces them, by building two
binary packages along the same line:

| Package | Contains | Licence |
|---|---|---|
| `lucidos-icon-themes` | `Lucid`, `Lucid-Dark` | CC-BY-NC-SA-4.0 (plus the oviotti files above) |
| `lucid-everything-icon-theme` | `Lucid-Everything` | GPL-3.0 |

The first **depends** on the second rather than recommending it, because `Lucid`
inherits it: without it every third-party application falls through to hicolor,
which is a broken desktop rather than a reduced one.

Splitting them is what makes the licence statement operative. A single package
containing both would be one `.deb` whose `debian/copyright` claims two
incompatible licences over one payload, and NonCommercial cannot be applied to
GPL-3.0 material by putting it in the same archive. CI asserts that neither
package contains the other's theme, so the boundary is checked on every push
rather than remembered.

It also means a distribution that cannot accept a NonCommercial package can
still ship the GPL one, and that anyone redistributing either knows which terms
they are under from the package name alone.

## The fallback chain

    Lucid  ->  Lucid-Everything  ->  hicolor

Only the first link is LucidOS's own work, and it is the only link the LucidOS
artwork licence describes.

---

*Not legal advice. This file records what the tree contains and under which
terms each part was received, so that a packager or a redistributor can act on
it.*
