"""Protein-change names from VEP HGVSp tokens: the single matching rule for the project.

Fixed 2026-10-29 (docs/AUDIT_RECORD.md, Corrections 14). The old rule took the
first match of p\\.([A-Z][a-z]{2}\\d+[A-Z][a-z]{2}) anywhere in a VCF line, so a
frameshift such as p.Lys163ArgfsTer3 yielded the name Lys163Arg. The fixed
rule accepts a name only when the HGVSp token is complete: p.Xxx123Yyy with
nothing after it. Complete nonsense tokens such as p.Gly542Ter are complete
and still accepted; truncated tokens (fs, ext, del, ins, dup, delins) are not.

Per VCF line, the name is taken from the first HGVSp token on the line, as
before. If that token is truncated, the line contributes no name, and its
coordinates are never used for that name.
"""

from __future__ import annotations

import re

PROTEIN_RE = re.compile(r"p\.([A-Z][a-z]{2}\d+[A-Z][a-z]{2})")
_DELIM = set("|,;\t \n\r")


def is_complete_at(text: str, match: re.Match) -> bool:
    """True when the matched HGVSp token ends right after the second residue."""
    end = match.end()
    return end == len(text) or text[end] in _DELIM


def name_from_line(line: str, fixed: bool = True) -> str | None:
    """Return the protein-change name a VCF line contributes, or None.

    fixed=False replays the pre-2026-10-29 rule (first match, complete or not)
    and exists only so rebuild scripts can show they reproduce the old files.
    """
    m = PROTEIN_RE.search(line)
    if not m:
        return None
    if fixed and not is_complete_at(line, m):
        return None
    return m.group(1)


def name_from_hgvsp_field(field: str, fixed: bool = True) -> str | None:
    """Return the name in one CSQ HGVSp field (e.g. ENSP...:p.Ser13Phe), or None."""
    m = PROTEIN_RE.search(field)
    if not m:
        return None
    if fixed and not is_complete_at(field, m):
        return None
    return m.group(1)
