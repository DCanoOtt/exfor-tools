#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_neutron_emission.py
========================
All the neutron spectra and neutron yields that EXFOR has for a reaction (x,n) on a given isotope, in three kinds of
plots:

    exclusive   the reaction to the residual nucleus, (x,n)R, for example 27Al(alpha,n)30P
    inclusive   the neutron emission, (x,xn), with the neutron as product
    combined    the two in one plot (only when both exist), the legend gives the product of each series

Usage, from any folder (the programs are exfor_retrieve.py and exfor_plot.py, build 2026-10-07 or later):

    python plot_neutron_emission.py Al-27                  # alpha particles, the default
    python plot_neutron_emission.py Be-9 --projectile a --out plots_Be9
    python plot_neutron_emission.py Al-27 --dry-run        # only list the plots that would be made

The paths are set in the four constants below (PROGRAMS_DIR, DATA_DIR, OUT_DIR, MASTER_DIR); each can be replaced on
the command line with --programs-dir, --data-dir, --out and --master. If PROGRAMS_DIR is empty or does not exist, the folder of this
script and its parent folder are tried, so that the script works in the examples folder and next to the programs.

Why a script is needed: EXFOR codes the same kind of measurement in several ways. The neutron as product (inclusive)
has the quantities DA/DE, PY/DA/DE, PY, TTY ...; the reaction to the residual nucleus (exclusive) has MLT/DA/DE,
MLT/DE, MLT, KE ... (MLT = neutron multiplicity). A search with only the neutron as product misses the second kind.
The script retrieves both, sorts the datasets into families (spectra at several angles, spectra integrated over the
angles, angular distributions, yields, mean energy) and plots each family. Nothing is mixed that has a different
unit: the plot program makes a separate plot for each unit.

At the end it writes coverage.csv: every dataset that was retrieved, and the plots it is in, or why it is in none
(superseded, complex reaction, no incident energy, quantity that is not handled).
"""
import argparse
import collections
import csv
import os
import re
import subprocess
import sys
from pathlib import Path

# ----------------------------------------------------------------------------------------------------------------
# PATHS: edit these four lines
PROGRAMS_DIR = ""     # folder with exfor_retrieve.py and exfor_plot.py: leave "" if the script is in the folder of the programs or in its sub-folder examples/; else e.g. "/home/you/exfor-tools"
DATA_DIR = "data"             # the retrieved data are in <DATA_DIR>/<target>/ (CSV files, references)
OUT_DIR = "plots_neutron_emission"            # the plots; a relative path is relative to the folder where you run
MASTER_DIR = None                             # the EXFOR master files; None: the default of exfor_retrieve.py
# ----------------------------------------------------------------------------------------------------------------


def _programs_dir():
    """Folder of exfor_retrieve.py and exfor_plot.py: --programs-dir, the variable EXFOR_PROGRAMS_DIR, PROGRAMS_DIR,
    or the folder of this script, the first one that has both files."""
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--programs-dir")
    given, _ = pre.parse_known_args()
    tried = [given.programs_dir, os.environ.get("EXFOR_PROGRAMS_DIR"), PROGRAMS_DIR,
             str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parent.parent)]
    for c in tried:
        if c and (Path(c) / "exfor_retrieve.py").is_file() and (Path(c) / "exfor_plot.py").is_file():
            return Path(c).resolve()
    sys.exit("exfor_retrieve.py and exfor_plot.py were not found in: " + ", ".join(str(c) for c in tried if c)
             + "\nSet PROGRAMS_DIR at the top of this script, or give --programs-dir.")


PROGRAMS = _programs_dir()
sys.path.insert(0, str(PROGRAMS))
import exfor_retrieve as X

# projectile code -> (Z, A); the residual nucleus of (x,n) has Z + Zx, A + Ax - 1
PROJECTILES = {"a": (2, 4), "he3": (2, 3), "p": (1, 1), "d": (1, 2), "t": (1, 3)}

# family -> (EXFOR quantity codes, plot options)
FAMILIES = collections.OrderedDict([
    ("spectra_angles", (["DA/DE", "PY/DA/DE", "MLT/DA/DE", "TTY/PY/DA/DE"],
                        "spectrum at several angles, one plot for each incident energy")),
    ("spectra_integrated", (["DE", "PY/DE", "MLT/DE", "TTY/PY/DE"], "spectrum integrated over the angles")),
    ("angular", (["DA", "PY/DA", "MLT/DA", "TTY/PY/DA"], "angular distribution")),
    ("yield", (["PY", "TTY", "MLT", "TTY/PY"], "neutron yield against the incident energy")),
    ("mean_energy", (["KE"], "mean neutron energy against the incident energy")),
])
CROSS_SECTION = ("cross_section", (["SIG"], "cross section against the incident energy"))


def residual(target, proj):
    m = re.fullmatch(r"([A-Za-z]{1,2})-(\d{1,3})", target)
    if not m:
        sys.exit(f"{target}: give an isotope such as Al-27 (the residual nucleus cannot be worked out for a natural "
                 f"element)")
    z = X.Z_OF[m.group(1).upper()]
    zr, ar = z + PROJECTILES[proj][0], int(m.group(2)) + PROJECTILES[proj][1] - 1
    sym = X.ELEMENTS[zr - 1]
    return zr, ar, f"{sym}-{ar}"


def unit_family(u):
    return re.sub(r"^(PRD|PRT|PT)(?=/)", "P", (u or "").upper()) if u else ""


def tofloat(t):
    try:
        return float(t)
    except (TypeError, ValueError):
        return None


def clusters(values, rel=0.02):
    """Energies that differ by less than rel are one energy; returns [(representative, [members])]."""
    out = []
    for v in sorted(values):
        if out and v - out[-1][1][-1] <= rel * max(abs(v), 1e-9) + 1e-9:
            out[-1][1].append(v)
        else:
            out.append([v, [v]])
    return [(sorted(m)[len(m) // 2], m) for _, m in out]


def main():
    ap = argparse.ArgumentParser(description="Neutron spectra and yields of (x,n) reactions: exclusive, inclusive, "
                                             "combined")
    ap.add_argument("target", help="isotope, for example Al-27")
    ap.add_argument("--projectile", default="a", choices=sorted(PROJECTILES), help="a (default), he3, p, d or t")
    ap.add_argument("--out", default=OUT_DIR, help=f"folder of the plots (default {OUT_DIR})")
    ap.add_argument("--data-dir", default=DATA_DIR, help=f"folder of the retrieved data (default {DATA_DIR})")
    ap.add_argument("--programs-dir", default=None,
                    help=f"folder of exfor_retrieve.py and exfor_plot.py (default {PROGRAMS_DIR}; used: {PROGRAMS})")
    ap.add_argument("--formats", default="png,pdf")
    ap.add_argument("--master", default=MASTER_DIR, help="folder of the EXFOR master files (default: MASTER_DIR, "
                                                         "else the default of exfor_retrieve.py)")
    ap.add_argument("--keep-superseded", action="store_true", help="do not leave out superseded data (SPSDD)")
    ap.add_argument("--with-cross-sections", action="store_true", help="also plot the cross sections (SIG)")
    ap.add_argument("--ascii", action="store_true", help="also write one ASCII file for each dataset")
    ap.add_argument("--dry-run", action="store_true", help="list the plots without making them")
    ap.add_argument("--no-retrieve", action="store_true", help="use the data already in the data folder")
    args = ap.parse_args()

    fams = collections.OrderedDict(FAMILIES)
    if args.with_cross_sections:
        fams[CROSS_SECTION[0]] = CROSS_SECTION[1]
    zr, ar, res = residual(args.target, args.projectile)
    all_q = [q for qs, _ in fams.values() for q in qs]
    here = PROGRAMS
    py = sys.executable
    args.out = str(Path(args.out).resolve())
    args.data_dir = str(Path(args.data_dir).resolve())
    master = ["--master", args.master] if args.master else []
    print(f"{args.target}({args.projectile},n): exclusive = the reaction to {res}, inclusive = the neutron as product")

    # 1. retrieve once, both kinds, with the references
    data_dir = Path(args.data_dir) / args.target
    if not args.no_retrieve:                       # also with --dry-run: the plan needs the data
        cmd = [py, str(here / "exfor_retrieve.py"), "--target", args.target, "--projectiles", args.projectile,
               "--product", f"n,{res}", "--quantity", ",".join(all_q), "--references", "--ref-format", "txt,bib",
               "--out", args.data_dir] + master + (["--ascii"] if args.ascii else [])
        print("retrieving:", " ".join(cmd[2:]))
        subprocess.run(cmd, check=True)
    try:
        dsets = list(csv.DictReader(open(next(data_dir.glob("EXFOR_*_datasets.csv")), encoding="utf-8")))
        points = list(csv.DictReader(open(next(data_dir.glob("EXFOR_*_data.csv")), encoding="utf-8")))
    except StopIteration:
        sys.exit(f"no data in {data_dir}: run without --no-retrieve")

    # 2. what each dataset has: energies, angles, outgoing energies, unit
    info = collections.defaultdict(lambda: {"E": set(), "angle": set(), "Eout": [], "unit": ""})
    for p in points:
        d = info[p["dataset"]]
        e, a, eo = tofloat(p["E_MeV"]), tofloat(p["angle_deg"]), tofloat(p["E_out_MeV"])
        if e is not None:
            d["E"].add(e)
        if a is not None:
            d["angle"].add(round(a, 1))
        if eo is not None:
            d["Eout"].append(eo)
        d["unit"] = d["unit"] or p["value_unit"]

    fam_of = {q: f for f, (qs, _) in fams.items() for q in qs}
    recs, reason = [], {}
    for d in dsets:
        d["info"] = info[d["dataset"]]
        d["family"] = fam_of.get(d["quantity"])
        zp, ap_ = tofloat(d.get("product_Z")), tofloat(d.get("product_A"))
        d["kind"] = ("exclusive" if (zp, ap_) == (zr, ar) else
                     "inclusive" if d.get("product_label") == "n" else None)
        if d["kind"] is None or d["family"] is None:
            reason[d["dataset"]] = "quantity or product not handled"
        elif "SPSDD" in (d.get("status") or "").upper() and not args.keep_superseded:
            reason[d["dataset"]] = "superseded (SPSDD)"
        elif d.get("reaction_type") == "complex":
            reason[d["dataset"]] = "complex reaction (sum or ratio)"
        elif d["family"] != "mean_energy" and not d["info"]["E"] and not d["info"]["Eout"]:
            reason[d["dataset"]] = "no incident energy"
        else:
            recs.append(d)

    # 3. plan the plots
    runs = []
    base = ["--data", str(data_dir), "--projectiles", args.projectile, "--format", args.formats]
    if not args.keep_superseded:
        base += ["--exclude-status", "SPSDD"]

    def add(family, kind, recs_, extra, tag=""):
        qs = sorted({r["quantity"] for r in recs_})
        prods = {"exclusive": [res], "inclusive": ["n"], "combined": ["n", res]}[kind]
        argv = base + ["--product", ",".join(prods), "--quantity", ",".join(qs)] + extra
        argv += ["--merge-products"]            # the quantities of one unit in one plot; the two products in combined
        out = Path(args.out) / family / (kind + (f"/{tag}" if tag else ""))
        runs.append({"family": family, "kind": kind, "argv": argv + ["--out", str(out)], "ids": {r["dataset"] for r in recs_},
                     "out": out})

    for fam in fams:
        by_kind = {k: [r for r in recs if r["family"] == fam and r["kind"] == k] for k in ("exclusive", "inclusive")}
        if not by_kind["exclusive"] and not by_kind["inclusive"]:
            continue
        if fam == "spectra_angles":
            allE = {e for k in by_kind.values() for r in k for e in r["info"]["E"]}
            for rep, members in clusters(allE):
                lo, hi = min(members), max(members)
                tol = max(0.02 * rep, 0.01) + (hi - lo) / 2
                center = (hi + lo) / 2
                sel = {k: [r for r in v if any(lo - 1e-9 <= e <= hi + 1e-9 for e in r["info"]["E"])] for k, v in by_kind.items()}
                eo = [x for k in sel.values() for r in k for x in r["info"]["Eout"]]
                logx = ["--logx"] if eo and min(eo) > 0 and max(eo) / min(eo) >= 30 else []
                extra = ["--x", "Eout", "--at-energy", f"{center:g}", "--tol", f"{tol:g}", "--angle-labels",
                         "--stack", "10", "--logy"] + logx
                # subentries of one entry with the same angles at one energy are different configurations (for
                # example target thicknesses): each in a plot of its own
                split = set()
                for k, v in sel.items():
                    ent = collections.defaultdict(list)
                    for r in v:
                        ent[r["entry"]].append(r)
                    for e_, rs in ent.items():
                        if len(rs) > 1 and len({frozenset(r["info"]["angle"]) for r in rs}) == 1:
                            split.add(e_)
                tag = f"E{rep:g}MeV"
                for k in ("exclusive", "inclusive"):
                    rest = [r for r in sel[k] if r["entry"] not in split]
                    if rest:
                        add(fam, k, rest, extra + (["--exclude-entries", ",".join(sorted(split))] if split else []), tag)
                    for r in sel[k]:
                        if r["entry"] in split:
                            add(fam, k, [r], extra + ["--entries", r["subentry"]], f"{tag}_{r['subentry']}")
                both = [r for k in ("exclusive", "inclusive") for r in sel[k] if r["entry"] not in split]
                if sel["exclusive"] and sel["inclusive"] and {r["kind"] for r in both} == {"exclusive", "inclusive"}:
                    add(fam, "combined", both, extra + (["--exclude-entries", ",".join(sorted(split))] if split else []), tag)
            continue
        if fam == "spectra_integrated":
            extra = ["--x", "Eout", "--energy-labels", "--stack", "10", "--logy"]
        elif fam == "angular":
            extra = ["--x", "angle", "--energy-labels", "--stack", "10", "--logy"]
        elif fam == "mean_energy":
            extra = []
        else:                                       # yields and cross sections against the incident energy
            extra = ["--logy", "--logx"]
        if fam in ("spectra_integrated", "angular"):
            n_e = len({e for k in by_kind.values() for r in k for e in r["info"]["E"]})
            if n_e > 20 and "--stack" in extra:                 # too many energies to stack: draw them unscaled
                i_ = extra.index("--stack")
                del extra[i_:i_ + 2]
        for k in ("exclusive", "inclusive"):
            if by_kind[k]:
                add(fam, k, by_kind[k], extra)
        if by_kind["exclusive"] and by_kind["inclusive"]:
            add(fam, "combined", by_kind["exclusive"] + by_kind["inclusive"], extra)

    print(f"\n{len(runs)} plot commands planned ({len({(r['family'], r['kind']) for r in runs})} family/kind pairs):")
    cnt = collections.Counter((r["family"], r["kind"]) for r in runs)
    for (f, k), n in cnt.items():
        print(f"  {f:20} {k:10} {n:3} command(s)")
    if args.dry_run:
        return

    # 4. make them
    log = open(Path(args.out + "_log.txt"), "w", encoding="utf-8")
    plotted = collections.defaultdict(list)
    n_png = 0
    for run in runs:
        cmd = [py, str(here / "exfor_plot.py")] + run["argv"]
        res_ = subprocess.run(cmd, capture_output=True, text=True)
        log.write("$ " + " ".join(cmd) + "\n" + res_.stdout + res_.stderr + "\n")
        if run["kind"] == "combined" and res_.returncode == 0:
            # a unit that only one kind has gives a plot of that kind alone: it is the exclusive or the inclusive plot
            for f in Path(run["out"]).rglob("*"):
                if f.is_file() and "+" not in f.name.split("_")[2]:
                    f.unlink()
        made = list(Path(run["out"]).rglob("*.png")) if res_.returncode == 0 else []
        n_png += len(made)
        if made:
            for i in run["ids"]:
                plotted[i].append(str(run["out"]))
        elif run["kind"] == "combined" and res_.returncode == 0:
            for i in run["ids"]:                  # the two kinds have no unit in common
                reason.setdefault(i, "")
        else:
            reason_txt = "plot command failed or drew nothing"
            for i in run["ids"]:
                reason.setdefault(i, reason_txt)
    log.close()

    # 5. coverage
    cov = Path(args.out) / "coverage.csv"
    cov.parent.mkdir(parents=True, exist_ok=True)
    with open(cov, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["kind", "family", "quantity", "unit", "entry", "subentry", "author", "year", "E_min_MeV",
                    "E_max_MeV", "points", "plotted_in", "reason_if_not_plotted"])
        for d in dsets:
            pl = plotted.get(d["dataset"], [])
            w.writerow([d["kind"] or "", d["family"] or "", d["quantity"], d["info"]["unit"], d["entry"], d["subentry"],
                        d["first_author"], d["year"], d["E_min_MeV"], d["E_max_MeV"], d["n_points"], "; ".join(pl),
                        "" if pl else reason.get(d["dataset"], "not selected in any plot")])
    n_ok = sum(1 for d in dsets if plotted.get(d["dataset"]))
    print(f"\n{n_png} plots written in {args.out}/ ({', '.join(args.formats.split(','))} for each); "
          f"{n_ok} of {len(dsets)} datasets are in a plot.")
    why = collections.Counter(reason.get(d["dataset"], "not selected in any plot") for d in dsets if not plotted.get(d["dataset"]))
    for t, n in why.most_common():
        print(f"  not plotted: {n} dataset(s), {t}")
    print(f"coverage: {cov};  references: {data_dir}/EXFOR_*_references.txt;  log of the plot commands: {args.out}_log.txt")


if __name__ == "__main__":
    main()
