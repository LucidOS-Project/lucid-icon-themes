# Licensing

This repository ships three icon themes under **two different licences**. The
root `LICENSE` file is the text of one of them, not a statement about all of
them; this file is the map.

| Path | Licence | Copyright |
|---|---|---|
| `Lucid/` | CC-BY-NC-SA-4.0 | 2025-2026 Javid Medina / Lucid Devices |
| `Lucid-Dark/` | CC-BY-NC-SA-4.0 | 2025-2026 Javid Medina / Lucid Devices |
| `Lucid-Everything/` | **GPL-3.0** | vinceliuice and contributors |
| certain icons inside `Lucid/` and `Lucid-Dark/` | **neither** -- used by permission | oviotti |
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

**The files this covers are not yet enumerated here, and they need to be.** A
licence map that says "some icons in these directories" is not something a
packager or a redistributor can act on, which is the entire purpose of this
file. Until the list exists, treat `Lucid/` and `Lucid-Dark/` as containing
material under two different arrangements and contact the author about the
oviotti icons, as the README says.

## Why the root licence cannot cover all of it

The GPL-3.0 does not permit adding restrictions to the work it covers.
"NonCommercial" is a restriction. So a single root CC-BY-NC-SA file applied to
the whole tree would not relicense `Lucid-Everything` -- it would simply be a
term the GPL forbids, which is why the two are stated separately here and in
`debian/copyright` rather than in one place with one answer.

## The fallback chain

    Lucid  ->  Lucid-Everything  ->  hicolor

Only the first link is LucidOS's own work, and it is the only link the LucidOS
artwork licence describes.

---

*Not legal advice. This file records what the tree contains and under which
terms each part was received, so that a packager or a redistributor can act on
it.*
