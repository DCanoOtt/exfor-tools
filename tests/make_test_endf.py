#!/usr/bin/env python3
"""Writes SYNTHETIC ENDF-6 files for testing endf_reader.py and the --endf option of exfor_plot.py.
The numbers are invented (they only have the structure of a real evaluation); do not use them as physics.

    python tests/make_test_endf.py OUTFOLDER      ->  n_092-U-238_test.endf  (resonance parameters + File 3)
                                                      n_092-U-238_test.pendf (pointwise: File 3 only)
"""
import sys
from pathlib import Path


def f11(x):
    """ENDF 11-character number."""
    if isinstance(x, int):
        return f"{x:11d}"
    s = f"{x:.9e}"
    mant, exp = s.split("e")
    e = int(exp)
    digits = 11 - 1 - len(f"{abs(e)}") - 1                    # characters left for the mantissa
    m = f"{float(mant):.{max(digits - 2, 1)}f}"
    if len(m) > 9 + (1 if x < 0 else 0) and False:
        pass
    out = f"{m}{'-' if e < 0 else '+'}{abs(e)}"
    return out.rjust(11)


class Writer:
    def __init__(self, mat):
        self.mat = mat
        self.lines = []

    def card(self, vals, mf, mt):
        vals = list(vals) + [0] * (6 - len(vals))
        self.lines.append("".join(f11(v) for v in vals) + f"{self.mat:4d}{mf:2d}{mt:3d}{0:5d}")

    def text(self, s, mf, mt):
        self.lines.append(f"{s:66s}{self.mat:4d}{mf:2d}{mt:3d}{0:5d}")

    def numbers(self, nums, mf, mt):
        for i in range(0, len(nums), 6):
            self.card(nums[i:i + 6], mf, mt)

    def tab1(self, qm, qi, lr, regions, xs, ys, mf, mt):
        """regions: [(NBT, INT)]"""
        self.card([qm, qi, 0, lr, len(regions), len(xs)], mf, mt)
        flat = [v for r in regions for v in r]
        self.numbers(flat, mf, mt)
        pts = [v for xy in zip(xs, ys) for v in xy]
        self.numbers(pts, mf, mt)

    def send(self, mf):
        """end of a section (SEND)"""
        self.lines.append(f"{'':66s}{self.mat:4d}{mf:2d}{0:3d}{0:5d}")

    def fend(self):
        """end of a file (FEND)"""
        self.lines.append(f"{'':66s}{self.mat:4d}{0:2d}{0:3d}{0:5d}")

    def mend(self):
        """end of the material (MEND)"""
        self.lines.append(f"{'':66s}{0:4d}{0:2d}{0:3d}{0:5d}")

    def head3(self, mt):
        self.card([92238.0, 236.0058, 0, 0, 0, 0], 3, mt)


def build(path, pointwise=False, mat=9237):
    w = Writer(mat)
    # MF1 / MT451
    w.card([92238.0, 236.0058, 1, 0, 0, 0], 1, 451)
    w.card([0.0, 1.0, 0, 0, 0, 6], 1, 451)
    w.card([1.0, 2.0e7, 0, 0, 12, 8], 1, 451)
    w.card([0.0, 0.0, 0, 0, 4, 0], 1, 451)
    w.text(" 92-U -238 TEST      SYNTH     EVAL-JAN26 SYNTHETIC TEST DATA", 1, 451)
    w.text("                    DIST-JAN26                       20260101", 1, 451)
    w.text("----ENDF/B-VIII.0     MATERIAL  9237", 1, 451)
    w.text("-----INCIDENT NEUTRON DATA", 1, 451)
    w.send(1)
    w.fend()
    # MF2 / MT151
    w.card([92238.0, 236.0058, 0, 0, 1, 0], 2, 151)
    w.card([92238.0, 1.0, 0, 0 if pointwise else 0, 1 if pointwise else 2, 0], 2, 151)
    if pointwise:
        w.card([1.0e-5, 2.0e7, 0, 0, 0, 0], 2, 151)                    # LRU = 0: no resonance parameters
        w.card([0.0, 0.9, 0, 0, 0, 0], 2, 151)
    else:
        w.card([1.0e-5, 2.0e4, 1, 3, 0, 0], 2, 151)                    # resolved range, Reich-Moore
        w.card([0.0, 0.94, 0, 0, 1, 0], 2, 151)
        w.card([236.0, 0.94, 0, 0, 6, 1], 2, 151)
        w.numbers([6.674, 1.0, 0.5, 0.0023, 0.0, 0.0], 2, 151)
        w.card([2.0e4, 1.5e5, 2, 1, 0, 0], 2, 151)                     # unresolved range, File 3 complete (LSSF = 1)
        w.card([0.0, 0.94, 1, 0, 1, 0], 2, 151)
        w.card([236.0, 0.0, 0, 0, 6, 1], 2, 151)
        w.numbers([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], 2, 151)
    w.send(2)
    w.fend()
    # MF3
    e_lo = 1.0e-5
    # total: lin-lin up to 2e4 eV, then log-log (INT = 5) up to 2e7 eV
    xs = [e_lo, 1.0, 100.0, 2.0e4, 1.0e5, 1.0e6, 2.0e7]
    ys = [20.0, 12.0, 11.0, 11.5, 10.0, 7.0, 4.6]
    w.head3(1)
    w.tab1(0.0, 0.0, 0, [(4, 2), (7, 5)], xs, ys, 3, 1)
    w.send(3)
    # elastic: lin-log
    xs = [e_lo, 1.0, 1.0e3, 1.0e6, 2.0e7]
    ys = [9.0, 9.0, 9.2, 4.0, 2.5]
    w.head3(2)
    w.tab1(0.0, 0.0, 0, [(5, 3)], xs, ys, 3, 2)
    w.send(3)
    # first- and second-chance fission as MT19 + MT20 (the sum is MT18)
    xs = [1.0e6, 6.0e6, 2.0e7]
    w.head3(19)
    w.tab1(0.0, -1.0e6, 0, [(3, 2)], xs, [0.0, 0.55, 0.60], 3, 19)
    w.send(3)
    xs = [6.5e6, 1.0e7, 2.0e7]
    w.head3(20)
    w.tab1(0.0, -1.0e6, 0, [(3, 2)], xs, [0.0, 0.2, 0.55], 3, 20)
    w.send(3)
    # capture: log-lin (INT = 4) then histogram (INT = 1) in the last region
    xs = [e_lo, 1.0, 1.0e3, 1.0e5, 1.0e6, 2.0e7]
    ys = [30.0, 0.3, 0.05, 0.002, 0.0004, 0.0001]
    w.head3(102)
    w.tab1(0.0, 4.806e6, 0, [(4, 4), (5, 2), (6, 1)], xs, ys, 3, 102)
    w.send(3)
    # (n,2n): threshold at 6.2 MeV
    xs = [6.2e6, 7.0e6, 1.2e7, 2.0e7]
    w.head3(16)
    w.tab1(-6.18e6, -6.18e6, 0, [(4, 2)], xs, [0.0, 0.3, 0.9, 0.5], 3, 16)
    w.send(3)
    w.fend()
    w.mend()
    w.lines.append(f"{'':66s}{-1:4d}{0:2d}{0:3d}{0:5d}")
    tpid = f"{'SYNTHETIC TEST TAPE':66s}{1:4d}{0:2d}{0:3d}{0:5d}"
    Path(path).write_text(tpid + "\n" + "\n".join(w.lines) + "\n")


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    out.mkdir(parents=True, exist_ok=True)
    build(out / "n_092-U-238_test.endf")
    build(out / "n_092-U-238_test.pendf", pointwise=True)
    print("written to", out)
