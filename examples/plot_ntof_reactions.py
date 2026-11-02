#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_ntof_reactions.py
======================
Plots the EXFOR data measured at n_TOF (CERN) for a table of reactions, one plot per target and reaction, and writes a
table of what EXFOR has and what it does not have (coverage_ntof.csv).

Usage, from any folder (needs exfor_retrieve.py and exfor_plot.py, version 2.3 / 1.3, build 2026-10-09 or later):

    python plot_ntof_reactions.py                         # all the reactions of the table below, cross sections
    python plot_ntof_reactions.py --only 5,6,10           # only the reactions number 5, 6 and 10 of the table
    python plot_ntof_reactions.py --also RYL,WID,WID/STR  # besides the cross sections, yields and resonance parameters
    python plot_ntof_reactions.py --list                  # print the table and exit
    python plot_ntof_reactions.py --no-retrieve           # plot from the data already in DATA_DIR

How it works
  1. For every target of the table the data are retrieved with  exfor_retrieve.py --facility ntof --projectiles n
     (only the entries measured at n_TOF; see Section 16.10 of the manual) into DATA_DIR/<target>/.
  2. The datasets of each reaction (target + EXFOR reaction type) are counted. A reaction without datasets is reported
     as "no n_TOF data in EXFOR" and nothing is plotted for it.
  3. exfor_plot.py draws the rest, in OUT_DIR/<number>_<reaction>/<target>/, with the list of references.

The table (REACTIONS) is the one of the request: edit it to add or remove reactions. process is the EXFOR reaction type
(G capture, P (n,p), D (n,d), A (n,alpha), T (n,t), EL elastic, 2N (n,2n), INL inelastic, X (n,xn)); None keeps every
reaction type of the target. natural elements are written C-nat, Pb-nat.

What is and is not there (EXFOR master files of 9 October 2026; run with --coverage-only to check yours)
  The entries of n_TOF found in EXFOR include 6Li(n,t), 14N(n,p), 33S(n,alpha), 35Cl(n,p), (n,gamma) on 50,53Cr,
  54,57Fe, 58,62,63Ni, 90,91,92,94,96Zr, 204,206,207Pb and 209Bi, natC(n,p) and (n,d), and widths of 7Be. Not found as
  n_TOF data: 7Li(n,n't), 9Be(n,2n), 11B(n,el), 52,54Cr, 56Fe, 64Ni and W (n,gamma), Mo, natPb and 208Pb, 50Cr(n,p),
  56Fe(n,n'gamma) and (n,xn), 7Be(n,p) and 7Be(n,alpha) cross sections. The script prints this for your master files.
"""
import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path

# ----------------------------------------------------------------------------------------------------------------
# PATHS: edit these lines
PROGRAMS_DIR = ""     # folder with exfor_retrieve.py and exfor_plot.py: leave "" if the script is in the folder of the programs or in its sub-folder examples/; else e.g. "/home/you/exfor-tools"
DATA_DIR = "data_ntof"        # the retrieved data are in <DATA_DIR>/<target>/
OUT_DIR = "plots_ntof_reactions"              # the plots; a relative path is relative to the folder where you run
MASTER_DIR = None                             # the EXFOR master files; None: the default of exfor_retrieve.py
# ----------------------------------------------------------------------------------------------------------------

# (label, targets, EXFOR reaction type or None for all)
REACTIONS = [
    ("7Li(n,n't)a",           ["Li-7"],                              None),
    ("9Be(n,2n)2a",           ["Be-9"],                              "2N"),
    ("6Li(n,t)a",             ["Li-6"],                              "T"),
    ("11B(n,el)11B",          ["B-11"],                              "EL"),
    ("Cr(n,g)",               ["Cr-50", "Cr-52", "Cr-53", "Cr-54"],  "G"),
    ("Fe(n,g)",               ["Fe-54", "Fe-56", "Fe-57"],           "G"),
    ("56Fe(n,n'g) and (n,xn)", ["Fe-56"],                            "INL,X,N"),
    ("Ni(n,g)",               ["Ni-58", "Ni-62", "Ni-63", "Ni-64"],  "G"),
    ("W(n,g)",                ["W-182", "W-183", "W-184", "W-186"],  "G"),
    ("Zr(n,g)",               ["Zr-90", "Zr-91", "Zr-92", "Zr-94", "Zr-96"], "G"),
    ("Mo(n,g)",               ["Mo-94", "Mo-95"],                    "G"),
    ("natC(n,p) and (n,d)",   ["C-nat"],                             "P,D"),
    ("50Cr(n,p)50V",          ["Cr-50"],                             "P"),
    ("14N(n,p)14C",           ["N-14"],                              "P"),
    ("33S(n,a)30Si",          ["S-33"],                              "A"),
    ("35Cl(n,p)35S",          ["Cl-35"],                             "P"),
    ("Pb(n,g)",               ["Pb-nat", "Pb-204", "Pb-206", "Pb-207", "Pb-208"], "G"),
    ("209Bi(n,g)210mBi/210Po", ["Bi-209"],                           "G"),
    ("7Be(n,p)7Li",           ["Be-7"],                              "P"),
    ("7Be(n,a)4He",           ["Be-7"],                              "A"),
]


def programs_dir():
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--programs-dir")
    given, _ = pre.parse_known_args()
    for c in (given.programs_dir, os.environ.get("EXFOR_PROGRAMS_DIR"), PROGRAMS_DIR,
              str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)):
        if c and (Path(c) / "exfor_retrieve.py").is_file() and (Path(c) / "exfor_plot.py").is_file():
            return Path(c)
    sys.exit("exfor_retrieve.py and exfor_plot.py not found: set PROGRAMS_DIR at the top of this script or use "
             "--programs-dir.")


PROGS = programs_dir()
sys.path.insert(0, str(PROGS))
import exfor_retrieve as X                               # noqa: E402

if getattr(X, "API_LEVEL", 0) < 2:
    sys.exit(f"{PROGS / 'exfor_retrieve.py'} is too old (version {getattr(X, '__version__', '?')}): --facility needs "
             f"exfor_retrieve.py 2.3 and exfor_plot.py 1.3 or later.")


def greek(lab):
    """Reaction label with the Greek letters of the particles (a -> alpha, g -> gamma) for titles."""
    import re
    lab = lab.replace(",a)", ",\u03b1)").replace(",g)", ",\u03b3)").replace("n'g)", "n'\u03b3)")
    return re.sub(r"\)(\d*)a\b", lambda m: ")" + m.group(1) + "\u03b1", lab)


def slug(s):
    return "".join(ch if ch.isalnum() else "_" for ch in s).strip("_")


def datasets_of(data_dir, target):
    """The dataset table written by exfor_retrieve.py for a target (list of dicts), or None if there is none."""
    f = Path(data_dir) / target / f"EXFOR_{target.split('-')[0].upper()}-{target.split('-')[1].upper()}_datasets.csv"
    if not f.is_file():
        cands = sorted((Path(data_dir) / target).glob("EXFOR_*_datasets.csv"))
        if not cands:
            return None
        f = cands[0]
    with open(f, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


_UNITS = {}


def units_of(data_dir, target, qty, procs):
    """EXFOR units of the values of a quantity (and reaction types) in the data table of a target."""
    key = (str(data_dir), target)
    if key not in _UNITS:
        found = set()
        for f in sorted((Path(data_dir) / target).glob("EXFOR_*_data.csv")):
            with open(f, newline="", encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    found.add((r["quantity"], r["process"].upper(), r["value_unit"]))
        _UNITS[key] = found
    return {u for q, pr, u in _UNITS[key] if q == qty and (procs is None or pr in procs)}


def main():
    ap = argparse.ArgumentParser(description="Plot the n_TOF data of EXFOR for a table of reactions.")
    ap.add_argument("--only", help="numbers of the reactions to do, e.g. 5,6,10 (see --list)")
    ap.add_argument("--list", action="store_true", help="print the table of reactions and exit")
    ap.add_argument("--also", default="", help="more quantities besides SIG, e.g. RYL,WID,WID/STR,RI (one plot per quantity)")
    ap.add_argument("--programs-dir", default=None, help="folder of exfor_retrieve.py and exfor_plot.py")
    ap.add_argument("--data-dir", default=DATA_DIR, help="folder of the retrieved data (default DATA_DIR)")
    ap.add_argument("--out", default=OUT_DIR, help="folder of the plots (default OUT_DIR)")
    ap.add_argument("--master", default=MASTER_DIR, help="folder of the EXFOR master files")
    ap.add_argument("--formats", default="png", help="plot formats, e.g. png,pdf")
    ap.add_argument("--dpi", type=int, default=300, help="resolution of the plots (default 300)")
    ap.add_argument("--ms", type=float, default=2.0, help="marker size of the plots (default 2; exfor_plot.py uses 4)")
    ap.add_argument("--keep-superseded", action="store_true", help="also plot the datasets with status SPSDD")
    ap.add_argument("--no-retrieve", action="store_true", help="do not retrieve: use the data in the data folder")
    ap.add_argument("--coverage-only", action="store_true", help="retrieve and write the coverage table, no plots")
    ap.add_argument("--linear", action="store_true", help="linear axes (default: logarithmic energy and cross section)")
    args = ap.parse_args()

    rows = list(enumerate(REACTIONS, 1))
    if args.list:
        for n, (lab, tg, pr) in rows:
            print(f"{n:2d}  {lab:26s} targets {', '.join(tg)}   reaction type {pr or 'all'}")
        return 0
    if args.only:
        want = {int(x) for x in args.only.split(",")}
        rows = [r for r in rows if r[0] in want]
    qtys = ["SIG"] + [q.strip().upper() for q in args.also.split(",") if q.strip()]
    targets = []
    for _, (_, tg, _) in rows:
        for t in tg:
            if t not in targets:
                targets.append(t)
    data_dir = Path(args.data_dir)

    # 1. retrieval: one call per target, in this process (the list of n_TOF entries is read only once)
    if not args.no_retrieve:
        for t in targets:
            print(f"=== retrieve {t} (n_TOF) ===", file=sys.stderr)
            argv = ["--facility", "ntof", "--target", t, "--projectiles", "n", "--quantity", ",".join(qtys),
                    "--out", str(data_dir), "--references"]
            if args.master:
                argv += ["--master", args.master]
            try:
                X.main(argv)
            except SystemExit:
                pass
            except Exception as exc:                      # keep going with the other targets
                print(f"  warning: {t}: {exc}", file=sys.stderr)

    # 2. coverage: datasets of every reaction
    coverage, todo = [], []
    for n, (lab, tg, proc) in rows:
        procs = {p.strip().upper() for p in proc.split(",")} if proc else None
        for t in tg:
            ds = datasets_of(data_dir, t)
            sel = [d for d in (ds or []) if (procs is None or d.get("process", "").upper() in procs)]
            by_q = {}
            for d in sel:
                by_q.setdefault(d["quantity"], set()).add(d["entry"])
            sig = by_q.get("SIG", set())
            coverage.append({"n": n, "reaction": lab, "target": t, "process": proc or "all",
                             "n_datasets": len(sel), "entries": " ".join(sorted({d["entry"] for d in sel})),
                             "quantities": " ".join(f"{q}({len(e)})" for q, e in sorted(by_q.items())),
                             "status": "data" if sel else ("no n_TOF data in EXFOR" if ds is not None else
                                                           "no n_TOF entry for this target")})
            if sel:
                todo.append((n, lab, t, proc, sorted(by_q)))
    fn = Path(args.out) / "coverage_ntof.csv"
    Path(args.out).mkdir(parents=True, exist_ok=True)
    with open(fn, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(coverage[0].keys()))
        w.writeheader()
        w.writerows(coverage)
    print("\nn   reaction                    target    datasets  entries / quantities")
    for c in coverage:
        print(f"{c['n']:<3d} {c['reaction']:27s} {c['target']:9s} {c['n_datasets']:8d}  "
              f"{c['entries'] if c['n_datasets'] else c['status']}   {c['quantities']}")
    print(f"\nCoverage table: {fn.resolve()}")
    if args.coverage_only:
        return 0

    # 3. plots
    plot = str(PROGS / "exfor_plot.py")
    done = 0
    for n, lab, t, proc, have in todo:
        for q in qtys:
            if q not in have:
                continue
            outd = Path(args.out) / f"{n:02d}_{slug(lab)}"
            cmd = [sys.executable, plot, "--data", str(data_dir / t), "--projectiles", "n", "--quantity", q,
                   "--out", str(outd), "--format", args.formats, "--dpi", str(args.dpi), "--ms", str(args.ms), "--references", "--auto-axes"]
            if proc:
                cmd += ["--process", proc]
            if not args.linear:
                cmd += ["--logx"] + (["--logy"] if q in ("SIG", "RYL") else [])
            if not args.keep_superseded:
                cmd += ["--exclude-status", "SPSDD"]
            if q != "SIG":
                cmd += ["--prefix", f"{t}_{slug(q)}"]
            procs = {p.strip().upper() for p in proc.split(",")} if proc else None
            # a "cross section" without area unit (NO-DIM: a ratio to a standard reaction, a complex reaction, as in
            # 6Li(n,t) of Amaducci 2019) is plotted apart, with --include-complex
            runs = [cmd]
            if q == "SIG" and "NO-DIM" in units_of(data_dir, t, q, procs):
                runs.append(cmd + ["--include-complex", "--prefix", f"{t}_ratio",
                             "--title", f"{greek(lab)}: ratios of cross sections that contain this reaction (n_TOF)",
                             "--ylabel", "Ratio to a reference reaction (no unit, see the EXFOR entry)"])
            for c_ in runs:
                print("+ " + " ".join(f'"{c}"' if " " in c else c for c in c_), file=sys.stderr)
                r = subprocess.run(c_)
                done += r.returncode == 0
    print(f"\n{done} plot commands finished; plots in {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
