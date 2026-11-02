#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_nuclide_chart.py
=====================
Chart of the nuclides (N on the horizontal axis, Z on the vertical axis) with the number of experimental data sets that
EXFOR has for a reaction channel of each target nuclide. The default is the neutron capture (n,g).

Usage, from any folder (needs exfor_retrieve.py, version 2.2 or later, in PROGRAMS_DIR or next to this script):

    python plot_nuclide_chart.py                          # (n,g), cross sections, all targets
    python plot_nuclide_chart.py --process F --out nf     # neutron-induced fission (n,f)
    python plot_nuclide_chart.py --projectile p --process G   # proton capture (p,g)
    python plot_nuclide_chart.py --no-zoom                # only the full chart (the default adds 5 zoomed charts by Z)
    python plot_nuclide_chart.py --quantity ALL           # every quantity, not only the cross section SIG
    python plot_nuclide_chart.py --metric entries         # number of EXFOR entries instead of data sets
    python plot_nuclide_chart.py --zmin 20 --zmax 60 --nmin 20 --nmax 80    # zoom

What is counted
  A data set is one reaction record of a subentry with a data table (the unit of the 'datasets' table of
  exfor_retrieve.py). Reactions that are sums or ratios (complex reactions) are not counted. natural targets (A = 0)
  are listed in the CSV but cannot be placed on the chart. Superseded data sets (status SPSDD) are counted unless
  --exclude-superseded is given. The count of entries, data sets and points of every target is written to
  <out>/nuclide_counts_<projectile>_<process>.csv.
"""
import argparse
import csv
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# ----------------------------------------------------------------------------------------------------------------
# PATHS: edit these lines
PROGRAMS_DIR = ""     # folder with exfor_retrieve.py: leave "" if the script is in the folder of the programs or in its sub-folder examples/; else e.g. "/home/you/exfor-tools"
MASTER_DIR = None                             # the EXFOR master files; None: the default of exfor_retrieve.py
OUT_DIR = "nuclide_chart"                     # the plots and the table; relative to the folder where you run
# ----------------------------------------------------------------------------------------------------------------


def _programs_dir():
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--programs-dir")
    given, _ = pre.parse_known_args()
    for c in (given.programs_dir, os.environ.get("EXFOR_PROGRAMS_DIR"), PROGRAMS_DIR,
              str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)):
        if c and (Path(c) / "exfor_retrieve.py").is_file():
            return Path(c)
    sys.exit("exfor_retrieve.py not found: set PROGRAMS_DIR at the top of this script or use --programs-dir.")


sys.path.insert(0, str(_programs_dir()))
import exfor_retrieve as X                                    # noqa: E402

ELEMENTS = {}                                                 # Z -> symbol
for _sym, _z in X.Z_OF.items():
    ELEMENTS[_z] = _sym.capitalize()


def scan_file(job):
    """Counts of one entry file: {target: [datasets, points, status_superseded]} for the requested channel."""
    path, proj, proc, qty, exclude_sps = job
    try:
        raw = open(path, "rb").read()
    except OSError:
        return None
    if f"({proj},{proc})".encode() not in raw.upper() and f"({proj},{proc}".encode() not in raw.upper():
        return None
    lines = raw.decode("latin-1").splitlines()
    entry = None
    out = {}
    buf, matches, status = None, [], ""
    for line in lines:
        if line.startswith("ENTRY"):
            entry = line.split()[1]
        elif line.startswith("SUBENT"):
            buf, matches, status = None, [], ""
        elif line.startswith("STATUS"):
            status = line[11:66]
        elif line.startswith("REACTION"):
            buf = [line[10:66]]
        elif buf is not None and line.startswith("           ") and not line.startswith("DATA"):
            buf.append(line[10:66])
        else:
            if buf is not None:
                text = "".join(x.strip() + " " for x in buf)
                n_terms = max(len(X.RX.findall(text)), len(X.RX_TERM.findall(text)))
                if n_terms == 1:
                    for tgt, pj, pc, prod, rest in X.RX.findall(text):
                        parts = (rest.split(",")[1:] if rest else []) + ["", ""]
                        if X.canon_code(pj) != proj or pc.upper() != proc:
                            continue
                        if qty and parts[1] not in qty:
                            continue
                        matches.append(tgt)
                buf = None
            if line.startswith("DATA ") and matches:
                tok = line.split()
                nl = int(tok[2]) if len(tok) > 2 and tok[2].isdigit() else 0
                if not (exclude_sps and "SPSDD" in status):
                    for tgt in matches:
                        d = out.setdefault(tgt, [0, 0, set()])
                        d[0] += 1
                        d[1] += nl
                        d[2].add(entry)
                matches = []
    return {t: [d[0], d[1], sorted(d[2])] for t, d in out.items()} or None


def main():
    ap = argparse.ArgumentParser(description="Nuclide chart with the number of EXFOR data sets of a reaction channel.")
    ap.add_argument("--projectile", default="n", help="projectile code, default n")
    ap.add_argument("--process", default="G", help="EXFOR process: G capture (default), F fission, 2N, P, A, INL, EL ...")
    ap.add_argument("--quantity", default="SIG", help="EXFOR quantity code(s), default SIG; ALL for all of them")
    ap.add_argument("--metric", choices=["datasets", "entries", "points"], default="datasets",
                    help="what is counted and coloured (default datasets)")
    ap.add_argument("--exclude-superseded", action="store_true", help="leave out the data sets with status SPSDD")
    ap.add_argument("--master", default=MASTER_DIR, help="folder of the EXFOR master files")
    ap.add_argument("--programs-dir", default=None, help="folder of exfor_retrieve.py")
    ap.add_argument("--out", default=OUT_DIR, help="folder of the plot and the table")
    ap.add_argument("--formats", default="png,pdf", help="plot formats (default png,pdf)")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--zmin", type=int, default=None)
    ap.add_argument("--zmax", type=int, default=None)
    ap.add_argument("--nmin", type=int, default=None)
    ap.add_argument("--nmax", type=int, default=None)
    ap.add_argument("--vmax", type=float, default=None, help="value of the top of the colour scale")
    ap.add_argument("--linear-scale", action="store_true", help="linear colour scale (default: logarithmic)")
    ap.add_argument("--no-zoom", action="store_true", help="only the full chart, not the zoomed charts by ranges of Z")
    ap.add_argument("--no-numbers", action="store_true", help="do not write the counts in the cells")
    ap.add_argument("--jobs", type=int, default=min(8, os.cpu_count() or 1))
    args = ap.parse_args()

    proj = X.canon_code(args.projectile)
    proc = args.process.upper()
    qty = None if args.quantity.upper() == "ALL" else {q.strip().upper() for q in args.quantity.split(",")}
    master = X.ensure_master(args.master or X.default_master(), update=False)
    files = sorted(str(p) for p in (master / "exforall").rglob("*.x4"))
    jobs = [(f, proj, proc, qty, args.exclude_superseded) for f in files]
    stats = {}
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        for res in ex.map(scan_file, jobs, chunksize=100):
            for tgt, (nd, npts, ents) in (res or {}).items():
                s = stats.setdefault(tgt, {"datasets": 0, "points": 0, "entries": set()})
                s["datasets"] += nd
                s["points"] += npts
                s["entries"].update(ents)
    print(f"{len(files)} EXFOR entries scanned (master files of {X.master_date(master) or 'unknown date'}); "
          f"{len(stats)} targets with ({proj.lower()},{proc.lower()}) data sets.", file=sys.stderr)

    rows, cells, natural = [], {}, []
    for tgt, s in stats.items():
        z_s, sym, a_s = tgt.split("-")[:3]
        z, a = int(z_s), (int(a_s) if a_s.isdigit() else 0)
        val = {"datasets": s["datasets"], "points": s["points"], "entries": len(s["entries"])}
        rows.append([z, sym.capitalize(), a, a - z if a else "", s["datasets"], len(s["entries"]), s["points"]])
        if a:
            cells[(a - z, z)] = val[args.metric]
        else:
            natural.append((f"nat{sym.capitalize()}", val[args.metric]))
    rows.sort(key=lambda r: (r[0], r[2]))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = f"{proj.lower()}_{proc.lower()}" + ("" if args.quantity.upper() == "SIG" else "_" + args.quantity.upper().replace("/", "-").replace(",", "-"))
    csvf = out / f"nuclide_counts_{tag}.csv"
    with open(csvf, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Z", "element", "A", "N", "datasets", "entries", "points"])
        w.writerows(rows)
    print(f"Table: {csvf.resolve()}", file=sys.stderr)
    if not cells:
        sys.exit("No data sets with a mass number: nothing to plot.")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize
    from matplotlib.patches import Rectangle

    what = {"datasets": "data sets", "entries": "EXFOR entries", "points": "data points"}[args.metric]
    qtxt = "" if args.quantity.upper() == "SIG" else f", quantity {args.quantity.upper()}"
    base = plt.get_cmap("Blues")                      # pale blue (few) to dark blue (many): no yellow, visible on grey
    cmap = LinearSegmentedColormap.from_list("blues_t", [base(0.28 + 0.72 * i / 255) for i in range(256)])
    vmax_all = args.vmax or max(cells.values())
    formats = [f.strip().lower().lstrip(".") for f in args.formats.split(",") if f.strip()]
    ntot = (sum(cells.values()) if args.metric != "entries" else sum(len(s["entries"]) for s in stats.values()))

    def chart(z0, z1, n0, n1, name, full):
        """One chart of the range Z z0..z1, N n0..n1. The full chart has small cells with big labels; the zoomed
        charts have big cells with the numbers inside."""
        vis = {k: v for k, v in cells.items() if n0 <= k[0] <= n1 and z0 <= k[1] <= z1}
        if not vis:
            return
        norm = Normalize(vmin=0, vmax=vmax_all) if args.linear_scale else LogNorm(vmin=1, vmax=max(vmax_all, 2))
        span_n, span_z = n1 - n0 + 1, z1 - z0 + 1
        cell_in = 0.115 if full else min(0.6, 17.0 / max(span_n, 1))             # inches per cell
        wd, ht = span_n * cell_in + 3.2, span_z * cell_in + 2.4
        fig, ax = plt.subplots(figsize=(wd, ht))
        ax.set_facecolor("0.95")
        for (n, z), v in vis.items():
            ax.add_patch(Rectangle((n - 0.5, z - 0.5), 1, 1, fc=cmap(norm(v)), ec="white", lw=0.4))
        if not args.no_numbers and not full:
            fs = max(8.0, min(22.0, cell_in * 72 * 0.5))                  # two digits fill about the cell width
            for (n, z), v in vis.items():
                ax.text(n, z, str(v), ha="center", va="center", fontsize=fs * (0.75 if v >= 100 else 1.0),
                        color="white" if norm(v) > 0.5 else "black", fontweight="bold")
        for m in (2, 8, 20, 28, 50, 82, 126):                                      # magic numbers
            if n0 <= m <= n1:
                ax.axvline(m, color="0.45", lw=0.6, ls=":", zorder=0)
            if z0 <= m <= z1:
                ax.axhline(m, color="0.45", lw=0.6, ls=":", zorder=0)
        ax.set_xlim(n0 - 0.5, n1 + 0.5)
        ax.set_ylim(z0 - 0.5, z1 + 0.5)
        ax.set_aspect("equal")
        big = 16 if full else 13
        ax.set_xlabel("Neutron number N", fontsize=big)
        ax.set_ylabel("Proton number Z", fontsize=big)
        step = 1 if span_z <= 30 else 5
        zt = [z for z in range(max(z0, 1), z1 + 1) if z in ELEMENTS and z % step == 0]
        ax.set_yticks(zt)
        ax.set_yticklabels([f"{ELEMENTS[z]} {z}" for z in zt], fontsize=big - 3)
        ax.set_xticks([n for n in range(n0, n1 + 1) if n % (10 if span_n > 60 else 5 if span_n > 30 else 2) == 0])
        ax.tick_params(axis="x", labelsize=big - 3)
        ax.set_title(f"Number of {what} in EXFOR: ({proj.lower()},{proc.lower()}) on each target nuclide{qtxt}\n"
                     f"{len(cells)} nuclides, {ntot} {what} in total (EXFOR master files of "
                     f"{X.master_date(master) or 'unknown date'})", fontsize=big)
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        cb = fig.colorbar(sm, ax=ax, fraction=0.03 if full else 0.04, pad=0.02, shrink=0.7)
        cb.set_label(f"Number of {what}", fontsize=big - 2)
        cb.ax.tick_params(labelsize=big - 3)
        if natural and full:
            note = "Natural targets (not on the chart): " + ", ".join(f"{n} ({v})" for n, v in sorted(natural))
            fig.text(0.01, 0.005, note, fontsize=9, color="0.3", ha="left", va="bottom", wrap=True)
        fig.tight_layout(rect=(0, 0.04 if (natural and full) else 0, 1, 1))
        for fmt in formats:
            fn = out / f"nuclide_chart_{tag}_{args.metric}{name}.{fmt}"
            fig.savefig(fn, dpi=args.dpi, bbox_inches="tight")
            print(f"Plot: {fn.resolve()}", file=sys.stderr)
        plt.close(fig)

    ns = [n for n, _ in cells]
    zs = [z for _, z in cells]
    n0 = args.nmin if args.nmin is not None else min(ns) - 1
    n1 = args.nmax if args.nmax is not None else max(ns) + 1
    z0 = args.zmin if args.zmin is not None else min(zs) - 1
    z1 = args.zmax if args.zmax is not None else max(zs) + 1
    zoomed = args.zmin is not None or args.zmax is not None or args.nmin is not None or args.nmax is not None
    chart(z0, z1, n0, n1, "" if not zoomed else "_zoom", full=not zoomed)
    if not zoomed and not args.no_zoom:                       # zoomed charts with the numbers in the cells
        for lo, hi in ((1, 28), (29, 50), (51, 70), (71, 82), (83, 100)):
            if hi >= z0 and lo <= z1:
                sub = [n for (n, z) in cells if lo <= z <= hi]
                if sub:
                    chart(lo - 1, hi + 1, min(sub) - 1, max(sub) + 1, f"_Z{lo}-{hi}", full=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
