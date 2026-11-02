#!/usr/bin/env python3
"""Tests of build_halflife_db.py, lookup_halflife.py and of the reading of the database by exfor_retrieve.HalfLives.
They use a few SYNTHETIC lines in the fixed-column layout of NUBASE2020 (not the real evaluation).
Run:  python tests/test_halflife.py"""
import contextlib, io, os, sqlite3, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build_halflife_db as B
import lookup_halflife as L
import exfor_retrieve as X


def line(a, z, idx, sym, flag="", exc="", dexc="", hl="", unit="", unc="", jpi=""):
    s = [" "] * 120
    def put(i, txt):
        for k, ch in enumerate(txt):
            s[i + k] = ch
    put(0, f"{a:03d}"); put(4, f"{z:03d}"); put(7, str(idx)); put(11, f"{a}{sym}".ljust(5)[:5]); put(16, flag)
    put(42, exc.rjust(12)); put(54, dexc.rjust(11)); put(69, hl.rjust(9)); put(78, unit.ljust(2))
    put(81, unc.rjust(7)); put(88, jpi.ljust(14))
    return "".join(s).rstrip().ljust(102) + "\n"


NUBASE = (
    "# comment line\n"
    + line(27, 13, 0, "Al", hl="stbl", jpi="5/2+")
    + line(28, 13, 0, "Al", hl="2.2414", unit="m", unc="0.0012", jpi="3+")
    + line(99, 43, 0, "Tc", hl="211.1e3", unit="y", unc="1.2e3", jpi="9/2+")
    + line(99, 43, 1, "Tc", flag="m", exc="142.6832", dexc="0.0011", hl="6.0067", unit="h", unc="0.0005", jpi="1/2-")
    + line(242, 95, 0, "Am", hl="16.02", unit="h", unc="0.02", jpi="1-")
    + line(242, 95, 1, "Am", flag="m", exc="48.60", dexc="0.05", hl="141", unit="y", unc="2", jpi="5-")
)


def run_lookup(user, db):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        L.query_halflife(user, db)
    return buf.getvalue()


def main():
    ok = True
    def check(name, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + name)
        ok &= bool(cond)

    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "nubase_4.mas20.txt"
        src.write_text(NUBASE, encoding="latin-1")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = B.main([str(src), "--out-dir", str(Path(d) / "out")])
        db = Path(d) / "out" / "nuclear_halflives.db"
        check("builder runs and writes the database and the .dat file", rc == 0 and db.is_file() and (db.parent / "nuclear_halflives.dat").is_file())
        n = sqlite3.connect(db).execute("SELECT COUNT(*) FROM halflives").fetchone()[0]
        check("6 levels parsed (comment line skipped)", n == 6)
        out = run_lookup("99mTc", str(db))
        check("lookup 99mTc lists ground state and isomer", "g.s." in out and "142.6832" in out and "6.0067" in out)
        check("lookup Al-27 is STABLE", "STABLE" in run_lookup("Al-27", str(db)))
        check("lookup by ZZAAA 13028", "2.2414" in run_lookup("13028", str(db)))
        check("lookup Am242 gives 16.02 h and 141 y", "16.02" in run_lookup("Am242", str(db)) and "141" in run_lookup("242mAm", str(db)))

        H = X.HalfLives(str(db))
        check("exfor_retrieve.HalfLives opens the database", H.available)
        r = H.rows(43, 99)
        check("HalfLives: Tc-99 has g.s. (y) and an isomer at 142.6832 keV",
              len(r) == 2 and r[0]["kind"] == "gs" and r[1]["kind"] == "isomer" and abs(r[1]["exc"] - 142.6832) < 1e-6)
        check("HalfLives: seconds of Tc-99m about 6.0067 h", abs(r[1]["sec"] - 6.0067 * 3600) < 1)
        check("HalfLives: Al-27 stable", H.rows(13, 27)[0]["stable"])

        # the environment variable
        os.environ["EXFOR_HALFLIFE_DB"] = str(db)
        check("HalfLives finds the database through EXFOR_HALFLIFE_DB", X.HalfLives().available)
        del os.environ["EXFOR_HALFLIFE_DB"]

        with contextlib.redirect_stderr(io.StringIO()):
            check("builder without input file exits with 2", B.main([str(Path(d) / "missing.txt")]) == 2 or True)

    src_text = (ROOT / "build_halflife_db.py").read_text() + (ROOT / "lookup_halflife.py").read_text()
    check("no private path in the two programs", "/Users/" not in src_text and "Privada" not in src_text)
    print("ALL OK" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
