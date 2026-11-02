#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
endf_reader.py  (version 1.0)
=============================
Small reader of evaluated nuclear data files in ENDF-6 format (ENDF/B, JEFF, JENDL, CENDL, BROND, TENDL ...),
for plotting the neutron cross sections (File 3, MF=3) over EXFOR data with exfor_plot.py (option --endf).
Only the Python standard library and numpy are needed.

What it reads
-------------
* the header of the material (MF1/MT451): nuclide (ZA), isomeric level, library and version as the file states it
  (for example "ENDF/B-VIII.0"), evaluation date;
* the neutron cross sections of File 3 (MF3), as the tabulated function sigma(E) with all its interpolation
  laws (histogram, lin-lin, lin-log, log-lin, log-log): the curve is expanded between the tabulated points so
  that it can be drawn with straight lines on any axes;
* the limits of the resonance ranges of File 2 (MF2/MT151), to tell where File 3 is complete (see below).

What it does NOT do
-------------------
* It does not reconstruct the resonances.  In an evaluated file the resolved resonance range is stored as
  RESONANCE PARAMETERS (File 2), and File 3 holds only the smooth background there.  Use a pointwise file (PENDF:
  what NJOY/RECONR or PREPRO/RECENT write, or the ".pendf" and "_300K" files that libraries distribute) to see the
  resonances, or draw the curve only above the resonance range, which is the default of exfor_plot.py.
  The same holds for the unresolved range when the file says (LSSF = 0) that File 3 is only a background.
* It does not read angular distributions, spectra, covariances or yields (MF4 - MF40): cross sections only.

Use from Python
---------------
    import endf_reader as ER
    tape = ER.read_endf("n_092-U-238.endf")      # a file may hold several materials
    mat = tape.find(92, 238)                       # Material or None
    print(mat.label, mat.resonance_note())
    E_eV, sigma_barn = mat.sigma(102)              # (n,gamma); E in eV, sigma in barn (None if the file has no such MT)
    print(ER.MT_NAMES[102])

    python endf_reader.py FILE.endf                # prints the materials and their reactions
"""
import re
import sys
from pathlib import Path

import numpy as np

__version__ = "1.0"

# neutron reactions (File 3) that exfor_plot.py can draw: EXFOR reaction type -> MT number
PROCESS_TO_MT = {"TOT": 1, "EL": 2, "NON": 3, "INL": 4, "2N": 16, "3N": 17, "F": 18, "NA": 22, "NP": 28, "4N": 37,
                 "G": 102, "P": 103, "D": 104, "T": 105, "HE3": 106, "A": 107, "2A": 108, "3A": 109, "2P": 111,
                 "PA": 112}
MT_NAMES = {1: "total", 2: "elastic", 3: "non-elastic", 4: "inelastic (sum)", 16: "(n,2n)", 17: "(n,3n)",
            18: "fission", 22: "(n,n+alpha)", 28: "(n,n+p)", 37: "(n,4n)", 102: "(n,gamma)", 103: "(n,p)",
            104: "(n,d)", 105: "(n,t)", 106: "(n,3He)", 107: "(n,alpha)", 108: "(n,2alpha)", 109: "(n,3alpha)",
            111: "(n,2p)", 112: "(n,p+alpha)"}
# MTs that are the sum of others when the file does not tabulate them
SUMS = {18: (19, 20, 21, 38), 4: tuple(range(51, 92)), 3: ()}
# reactions whose cross section in the resonance ranges is stored as resonance parameters
RESONANCE_MTS = {1, 2, 3, 18, 19, 102}

NLIB = {0: "ENDF/B", 1: "ENDF/A", 2: "JEFF", 3: "EFF", 4: "ENDF/B (high energy)", 5: "CENDL", 6: "JENDL",
        31: "INDL/V", 32: "INDL/A", 33: "FENDL", 34: "IRDF", 35: "BROND", 36: "INGDB-90", 37: "FENDL/A",
        41: "BROND-2"}

_FLOAT = re.compile(r"^([+-]?\d*\.?\d*)([+-]\d+)$")


def efloat(field):
    """A number of an ENDF card (11 characters; '1.234567+3' means 1.234567e3)."""
    s = field.strip()
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        m = _FLOAT.match(s)
        if m and m.group(1) not in ("", "+", "-", "."):
            return float(m.group(1) + "e" + m.group(2))
        raise ValueError(f"not an ENDF number: {field!r}")


def eint(field):
    s = field.strip()
    return int(float(s)) if s else 0


def is_int_field(field):
    s = field.strip()
    return bool(s) and s.lstrip("+-").isdigit()


def fields(line):
    return [line[i:i + 11] for i in range(0, 66, 11)]


def cont(line):
    """(C1, C2, L1, L2, N1, N2) of a CONT/HEAD card."""
    f = fields(line)
    return efloat(f[0]), efloat(f[1]), eint(f[2]), eint(f[3]), eint(f[4]), eint(f[5])


class EndfError(Exception):
    pass


def parse_tab1(lines):
    """TAB1 record -> (breaks NBT, laws INT, x, y, (C1, C2, L1, L2) of the head).  Returns also the number of lines used."""
    c1, c2, l1, l2, nr, npts = cont(lines[0])
    n_int = (2 * nr + 5) // 6                       # the interpolation pairs and the points each start on a new card
    n_pts = (2 * npts + 5) // 6
    if len(lines) < 1 + n_int + n_pts:
        raise EndfError("TAB1 record is truncated")
    ivals = [efloat(x) for ln in lines[1:1 + n_int] for x in fields(ln)]
    pvals = np.array([efloat(x) for ln in lines[1 + n_int:1 + n_int + n_pts] for x in fields(ln)][:2 * npts], dtype=float)
    nbt = [int(ivals[2 * i]) for i in range(nr)]
    law = [int(ivals[2 * i + 1]) for i in range(nr)]
    return nbt, law, pvals[0::2], pvals[1::2], (c1, c2, l1, l2), 1 + n_int + n_pts


def expand_tab1(nbt, law, x, y, sub=12):
    """Tabulated function with ENDF interpolation laws -> points (x, y) that straight lines join (any axes).
    Law 1 (histogram) gets the step points; laws 3, 4 and 5 get `sub` points inside each interval; law 2 none.
    Law 6 (charged particles) is treated as linear."""
    n = len(x)
    if n == 0:
        return x, y
    xs, ys = [x[:1]], [y[:1]]
    start = 0
    for end_p, lw in zip(nbt, law):
        end = min(int(end_p) - 1, n - 1)           # NBT is the (1-based) index of the last point of the region
        if end <= start:
            continue
        x0, x1 = x[start:end], x[start + 1:end + 1]
        y0, y1 = y[start:end], y[start + 1:end + 1]
        if lw == 1:                                  # histogram: y0 up to x1, then jump to y1
            px = np.column_stack([x1, x1]).ravel()
            py = np.column_stack([y0, y1]).ravel()
            xs.append(px)
            ys.append(py)
        elif lw in (3, 4, 5) and sub > 0:
            t = (np.arange(1, sub + 1) / (sub + 1.0))[None, :]            # fractions inside the interval
            ok_x = (x0 > 0) & (x1 > x0)
            if lw in (3, 5):                          # ln x
                with np.errstate(all="ignore"):
                    xi = np.where(ok_x[:, None], x0[:, None] * (x1 / np.where(ok_x, x0, 1.0))[:, None] ** t,
                                  x0[:, None] + (x1 - x0)[:, None] * t)
                    f = np.where(ok_x[:, None], np.log(xi / np.where(ok_x, x0, 1.0)[:, None]) /
                                 np.log(np.where(ok_x, x1 / np.where(ok_x, x0, 1.0), 2.0))[:, None], t)
            else:                                     # lin x
                xi = x0[:, None] + (x1 - x0)[:, None] * t
                f = np.broadcast_to(t, xi.shape)
            if lw in (4, 5):                          # ln y: geometric between two positive values, else linear
                pos = (y0 > 0) & (y1 > 0)
                with np.errstate(all="ignore"):
                    yi = np.where(pos[:, None], np.where(pos, y0, 1.0)[:, None] *
                                  (np.where(pos, y1, 1.0) / np.where(pos, y0, 1.0))[:, None] ** f,
                                  y0[:, None] + (y1 - y0)[:, None] * f)
            else:
                yi = y0[:, None] + (y1 - y0)[:, None] * f
            px = np.column_stack([xi, x1]).ravel()
            py = np.column_stack([yi, y1]).ravel()
            xs.append(px)
            ys.append(py)
        else:                                         # lin-lin (2), or sub = 0
            xs.append(x1)
            ys.append(y1)
        start = end
        if start >= n - 1:
            break
    return np.concatenate(xs), np.concatenate(ys)


class Material:
    """One material (MAT) of an ENDF file."""

    def __init__(self, mat, path):
        self.mat = mat
        self.path = path
        self.za = 0
        self.z = self.a = 0
        self.awr = 0.0
        self.liso = 0                  # isomeric state of the target (0 = ground state)
        self.nlib = self.nver = self.lrel = 0
        self.hsub = ""                 # "ENDF/B-VIII.0" as the file writes it
        self.edate = ""
        self.mf3 = {}                  # MT -> lines of the section
        self.mf2 = []                  # lines of MF2/MT151
        self.ranges = []               # [(EL, EH, LRU, LRF)] eV, first isotope only
        self.lssf = None               # LSSF flag of the unresolved range, if any
        self.n_iso = 1
        self._cache = {}

    # ------------------------------------------------------------------
    @property
    def label(self):
        """Library and version, as the file states them ('ENDF/B-VIII.0'); the nuclide name if it does not say."""
        if self.hsub:
            return self.hsub
        lib = NLIB.get(self.nlib)
        if lib:
            return f"{lib}-{self.nver}.{self.lrel}"
        return Path(self.path).stem

    def reactions(self):
        return sorted(self.mf3)

    # ------------------------------------------------------------------
    def _table(self, mt):
        if mt not in self.mf3:
            return None
        nbt, law, x, y, _head, _u = parse_tab1(self.mf3[mt][1:])        # the first card is the HEAD of the section
        return nbt, law, x, y

    def sigma(self, mt, sub=12):
        """(E in eV, sigma in barn) of reaction MT, or None when the file has neither the MT nor the parts it is the sum of.
        Sums (fission: MT19, 20, 21, 38; inelastic: MT51 - 91) are added on the union of the energy grids (lin-lin)."""
        key = (mt, sub)
        if key in self._cache:
            return self._cache[key]
        out = None
        if mt in self.mf3:
            t = self._table(mt)
            out = expand_tab1(*t, sub=sub)
        elif SUMS.get(mt):
            parts = [self.sigma(p, sub) for p in SUMS[mt] if p in self.mf3]
            if parts:
                grid = np.unique(np.concatenate([p[0] for p in parts]))
                tot = np.zeros_like(grid)
                for e, s in parts:
                    tot += np.interp(grid, e, s, left=0.0, right=0.0)
                out = (grid, tot)
        self._cache[key] = out
        return out

    # ------------------------------------------------------------------
    def _read_ranges(self):
        """Energy ranges of the resonance parameters (first isotope): [(EL, EH, LRU, LRF)], and LSSF of the unresolved one.
        The ranges are contiguous (EL of one = EH of the one before), which is how they are found without
        interpreting every resonance format."""
        L = self.mf2
        if len(L) < 3:
            return
        try:
            za, awr, _a, _b, nis, _c = cont(L[0])
            self.n_iso = nis
            if nis != 1:
                return                                # natural element evaluations: not examined
            _zai, _abn, _l1, lfw, ner, _n2 = cont(L[1])
        except (ValueError, EndfError):
            return
        f = fields(L[2])
        try:
            el, eh = efloat(f[0]), efloat(f[1])
            lru, lrf, nro = eint(f[2]), eint(f[3]), eint(f[4])
        except ValueError:
            return
        found = [(el, eh, lru, lrf, 2, nro)]
        prev_eh = f[1]
        for i in range(3, len(L)):
            if len(found) >= ner:
                break
            ff = fields(L[i])
            if not (is_int_field(ff[2]) and is_int_field(ff[3]) and is_int_field(ff[4]) and is_int_field(ff[5])):
                continue
            if ff[0].strip() != prev_eh.strip():
                continue
            try:
                el, eh = efloat(ff[0]), efloat(ff[1])
                lru, lrf, nro = eint(ff[2]), eint(ff[3]), eint(ff[4])
            except ValueError:
                continue
            if eh > el > 0 and lru in (0, 1, 2) and lrf in range(0, 8) and nro in (0, 1):
                found.append((el, eh, lru, lrf, i, nro))
                prev_eh = ff[1]
        self.ranges = [(e0, e1, u, r) for e0, e1, u, r, _i, _n in found]
        for e0, e1, u, r, i, nro in found:
            if u == 2:                                # unresolved range: the card after the header (and the TAB1 of NRO = 1)
                j = i + 1
                try:
                    if nro:
                        _n, _l, _x, _y, _h, used = parse_tab1(L[j:])
                        j += used
                    self.lssf = cont(L[j])[2]
                except (ValueError, EndfError, IndexError):
                    self.lssf = None

    def complete_from(self):
        """Energy (eV) above which File 3 alone is the whole cross section of the reactions in RESONANCE_MTS, and why.
        0 for a pointwise file (PENDF) or one without resonance parameters."""
        self._read_ranges()
        end, why = 0.0, ""
        for e0, e1, u, r in self.ranges:
            if u == 1 and e1 > end:
                end, why = e1, "resolved resonance range (resonance parameters in File 2)"
        for e0, e1, u, r in self.ranges:
            if u == 2 and self.lssf != 1 and e1 > end:
                end, why = e1, "unresolved resonance range (File 3 is only the background there, LSSF = %s)" % (
                    "?" if self.lssf is None else self.lssf)
        return end, why

    def resonance_note(self):
        end, why = self.complete_from()
        if not end:
            return "pointwise or without resonance parameters"
        return f"File 3 complete above {end:.6g} eV: {why}"


class Tape:
    def __init__(self, path):
        self.path = str(path)
        self.materials = []

    def find(self, z, a, liso=0):
        for m in self.materials:
            if (m.z, m.a) == (z, a) and m.liso == liso:
                return m
        return None


def read_endf(path):
    """Read an ENDF-6 file (Files 1, 2 and 3 only are kept)."""
    tape = Tape(path)
    mats, order = {}, []
    with open(path, "r", encoding="latin-1") as fh:
        first = True
        for line in fh:
            if first:                                  # TPID card
                first = False
                continue
            if len(line) < 75:
                continue
            mat, mf, mt = line[66:70].strip(), line[70:72].strip(), line[72:75].strip()
            if mat in ("", "0", "-1") or mt in ("", "0") or mf in ("", "0"):
                continue
            if mf == "3":
                key = (mat, "3", mt)
            elif mf == "1" and mt == "451":
                key = (mat, "1", "451")
            elif mf == "2" and mt == "151":
                key = (mat, "2", "151")
            else:
                continue
            if mat not in mats:
                mats[mat] = {}
                order.append(mat)
            mats[mat].setdefault(key, []).append(line)
    for mat in order:
        parts = mats[mat]
        m = Material(int(mat), path)
        head = parts.get((mat, "1", "451"))
        if head and len(head) >= 4:
            za, awr, lrp, lfi, nlib, nmod = cont(head[0])
            elis, sta, lis, liso, _z, nfor = cont(head[1])
            awi, emax, lrel, _z2, nsub, nver = cont(head[2])
            nwd = cont(head[3])[4]
            m.za, m.awr, m.liso, m.nlib, m.nver, m.lrel = int(za), awr, liso, nlib, nver, lrel
            m.z, m.a = int(za) // 1000, int(za) % 1000
            text = head[4:4 + nwd]
            for t in text:
                mm = re.search(r"-{2,}\s*(\S+)\s+MATERIAL", t[:66])
                if mm:
                    m.hsub = mm.group(1)
                    break
            if len(text) >= 1:
                m.edate = text[0][22:33].strip()
        else:
            continue                                   # a material without a header cannot be identified
        m.mf2 = parts.get((mat, "2", "151"), [])
        for (mt_mat, mf, mt), lines in parts.items():
            if mf == "3":
                m.mf3[int(mt)] = lines
        tape.materials.append(m)
    return tape


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print(__doc__)
        return 1
    for p in argv:
        t = read_endf(p)
        print(f"{p}: {len(t.materials)} material(s)")
        for m in t.materials:
            print(f"  MAT {m.mat}: Z={m.z} A={m.a}{' (isomer %d)' % m.liso if m.liso else ''}  {m.label}  "
                  f"[{m.resonance_note()}]")
            print("    MF3:", ", ".join(f"{mt}" + (f" {MT_NAMES[mt]}" if mt in MT_NAMES else "") for mt in m.reactions()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
