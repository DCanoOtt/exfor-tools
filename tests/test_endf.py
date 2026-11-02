#!/usr/bin/env python3
"""Tests of endf_reader.py and of the --endf option of exfor_plot.py, with SYNTHETIC ENDF files (tests/make_test_endf.py)
and a few real EXFOR points of U-238 (tests/data_endf).  Run from the folder of the scripts:

    python tests/test_endf.py
"""
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
import endf_reader as ER          # noqa: E402
import make_test_endf             # noqa: E402

TMP = tempfile.TemporaryDirectory()
ENDF = Path(TMP.name) / "n_092-U-238_test.endf"
PENDF = Path(TMP.name) / "n_092-U-238_test.pendf"
make_test_endf.build(ENDF)
make_test_endf.build(PENDF, pointwise=True)


def formula(nbt, law, x, y, e):
    """ENDF interpolation of one point, written out independently of the reader."""
    for i in range(len(x) - 1):
        if x[i] <= e <= x[i + 1] and x[i + 1] > x[i]:
            lw = next(l for nb, l in zip(nbt, law) if i + 1 <= nb - 1)
            x0, x1, y0, y1 = (float(v) for v in (x[i], x[i + 1], y[i], y[i + 1]))
            if lw == 1:
                return y0
            if lw == 2:
                return y0 + (y1 - y0) * (e - x0) / (x1 - x0)
            if lw == 3:
                return y0 + (y1 - y0) * math.log(e / x0) / math.log(x1 / x0)
            if lw == 4:
                return y0 * (y1 / y0) ** ((e - x0) / (x1 - x0))
            if lw == 5:
                return y0 * (y1 / y0) ** (math.log(e / x0) / math.log(x1 / x0))
    return None


class Reader(unittest.TestCase):
    def setUp(self):
        self.mat = ER.read_endf(ENDF).materials[0]

    def test_header(self):
        m = self.mat
        self.assertEqual((m.z, m.a, m.liso), (92, 238, 0))
        self.assertEqual(m.label, "ENDF/B-VIII.0")
        self.assertEqual(m.reactions(), [1, 2, 16, 19, 20, 102])

    def test_interpolation_laws(self):
        for mt in (1, 2, 102):                       # lin-lin + log-log, lin-log, log-lin + lin-lin + histogram
            nbt, law, x, y = self.mat._table(mt)
            ex, ey = ER.expand_tab1(nbt, law, x, y)
            self.assertFalse(np.isnan(ey).any())
            n = 0
            for e, v in zip(ex, ey):
                if e in x:
                    continue
                ref = formula(nbt, law, x, y, e)
                self.assertAlmostEqual(v, ref, delta=1e-9 * max(abs(ref), 1e-30), msg=f"MT{mt} E={e}")
                n += 1
            self.assertGreater(n, 20)

    def test_fission_sum(self):
        e, s = self.mat.sigma(18)                    # the file has MT19 and MT20, no MT18
        self.assertAlmostEqual(float(np.interp(7e6, e, s)), 0.55 + 0.05 * 1e6 / 1.4e7 + 0.2 * 0.5e6 / 3.5e6, places=9)
        self.assertIsNone(self.mat.sigma(999))
        self.assertIsNone(self.mat.sigma(4))

    def test_resonance_ranges(self):
        end, why = self.mat.complete_from()
        self.assertEqual(end, 2.0e4)
        self.assertIn("resolved", why)
        pw = ER.read_endf(PENDF).materials[0]
        self.assertEqual(pw.complete_from()[0], 0.0)

    def test_agrees_with_endf_parserpy(self):
        try:
            from endf_parserpy import EndfParserPy
        except ImportError:
            self.skipTest("endf-parserpy is not installed (pip install endf-parserpy): independent check skipped")
        d = EndfParserPy().parsefile(str(ENDF), include=[3])
        for mt in self.mat.reactions():
            t = d[3][mt]["xstable"]
            nbt, law, x, y = self.mat._table(mt)
            self.assertEqual(list(t["NBT"]), nbt)
            self.assertEqual(list(t["INT"]), law)
            self.assertTrue(np.allclose(t["E"], x) and np.allclose(t["xs"], y), f"MT{mt}")


class Plot(unittest.TestCase):
    def test_draw_endf(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import exfor_plot as P
        args = P.argparse.Namespace(endf_lib=P.EndfLibrary([str(ENDF), str(PENDF)], ["param", "pointwise"]),
                                    endf_full=False, endf_lw=1.4, endf_sub=12, xlim=None, emin=None, emax=None)
        rows = [{"process": "F", "E_MeV": e, "value": 500.0, "product_state": ""} for e in (1.0, 5.0, 10.0)]
        key = ("n", "none", "SIG", "f", "92-U-238", "", "", "")
        fig, ax = plt.subplots()
        n = P.draw_endf(ax, key, rows, "mb", args, {"logy": False, "logx": False, "xlim": None, "ylim": None})
        self.assertEqual(n, 2)
        line = ax.get_lines()[0]
        x, y = line.get_data()
        self.assertLessEqual(min(x), 1.0)                        # the line covers the data, a little wider
        self.assertGreaterEqual(max(x), 10.0)
        self.assertAlmostEqual(float(np.interp(7.0, x, y)), 1000 * (0.55 + 0.05 * 1e6 / 1.4e7 + 0.2 * 0.5e6 / 3.5e6), places=6)
        # a plot of another quantity or a natural target gets no line
        self.assertEqual(P.draw_endf(ax, ("n", "none", "DA", "f", "92-U-238", "", "", ""), rows, "mb", args,
                                     {"logy": False, "logx": False, "xlim": None, "ylim": None}), 0)
        plt.close(fig)

    def test_command_line(self):
        with tempfile.TemporaryDirectory() as out:
            r = subprocess.run([sys.executable, str(ROOT / "exfor_plot.py"), "--data", str(ROOT / "tests" / "data_endf" / "U-238"),
                                "--projectiles", "n", "--out", out, "--logx", "--logy", "--endf", str(ENDF), str(PENDF),
                                "--endf-label", "parameters", "pointwise"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            files = sorted(p.name for p in Path(out).rglob("*.png"))
            self.assertEqual(files, ["U-238_n_239U.png", "U-238_n_none_F.png"])
            self.assertIn("ENDF n_092-U-238_test.endf: ENDF/B-VIII.0", r.stderr)
            self.assertNotIn("Traceback", r.stderr)

    def test_endf_label_without_endf(self):
        r = subprocess.run([sys.executable, str(ROOT / "exfor_plot.py"), "--data", str(ROOT / "tests" / "data_endf" / "U-238"),
                            "--endf-label", "x"], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--endf-label needs --endf", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
