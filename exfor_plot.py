#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exfor_plot.py  (version 1.4)
============================
Plot EXFOR data selected with exfor_retrieve.py: excitation functions (cross
section against incident energy) with error bars, one panel per reaction
product, one curve per dataset (author, year, entry).

Two ways to use it
------------------
1) Retrieve and plot in one step.  The same selection options as exfor_retrieve.py
   (--target, --projectiles, --product, --quantity, --emin, --emax, --master, --update):

     python exfor_plot.py --target Nb-93 --projectiles d --product 92mNb,89Zr,90Nb
     python exfor_plot.py --target Cu-nat --projectiles d --product Zn-65,Zn-63,Zn-62,Cu-64 --vline 40
     python exfor_plot.py --target U-238 --projectiles n --product none --process F --logx --logy --emin 1e-6

2) Plot files already written by exfor_retrieve.py (no EXFOR master files needed):

     python exfor_plot.py --data data/Nb-93 --product "Zr-*" --logy
     python exfor_plot.py --data data/Nb-93/EXFOR_NB-93_data.csv --projectiles d,p --format png,pdf

If a --data path does not exist yet (the data were not retrieved), the program retrieves them: the target is
taken from the path (data/Rb-93, data/Ti-nat, data/Nb-93/EXFOR_NB-93_data.csv), the selection from the
options of the command line, and the data are saved at that path before the plots are made.  Without
--projectiles the retrieval default d,p,he3,a is used (add --projectiles all for everything).

In the first mode the retrieved data are also saved, as exfor_retrieve.py would write them, in
data/<target name>/ (EXFOR_<target>_data.csv and _datasets.csv; --data-dir, --data-prefix and
--no-save-data change this), so the plots can be redone later with --data data/Nb-93 without the
EXFOR master files.  The plots go to plots/<target name>/.

Keep exfor_plot.py in the same folder as exfor_retrieve.py (it uses its parsers).
Requires Python 3.8+ and matplotlib (pip install matplotlib).

What is plotted
---------------
* One panel per (projectile, product, quantity).  Default quantity: SIG (cross sections, mb).
* With --data every projectile found in the file is plotted unless --projectiles restricts it;
  with --target the default is d,p,he3,a, as in exfor_retrieve.py.
* One series per EXFOR subentry, labelled "Author year" (with the branch, e.g. CUM, when given).
  The same entry has the same colour and marker in every panel.  Data digitised from
  a curve (status CURVE) are drawn with open markers.
* Reactions without a product (fission, total, elastic, ...) get one panel per reaction type
  (--by-process does the same for any product); --process F keeps one type, for example fission.
* Legend: up to --max-legend series (default 12) the legend is inside the plot; with more series
  there is no room, so the labels are written to the right of the plot, in columns (24 per column).
  With --combine a panel with more series than that has no legend (use --legend figure).
* Reactions of type "complex" (ratios, sums) are left out unless --include-complex is given.
* Cross sections that EXFOR gives multiplied by the energy (units B*EV, B*KEV, B*MEV, MB*MEV: sigma x E)
  or by its square root (B*RT-EV: sigma x sqrt(E)) are divided by it and plotted in mb, using the
  incident energy; --no-convert-units leaves them out.
* Cross sections (SIG) are plotted in one unit, mb (or --unit); points in other units are dropped and
  counted in the messages.  Every other quantity (spectra, yields, probabilities, ...) gets one plot per
  unit, with the unit in the file name (for example ..._PN_DE_ARB-UNITS.png), unless --unit is given.
* --branch DL keeps the delayed-neutron data (DL, DL/GRP, ...), --branch PR the prompt ones.
* Points without the plotted coordinate (for example no incident energy) are dropped and counted.

References (--references)
-------------------------
--references also writes the list of references of the datasets that are plotted, for each target, in the
folder of its plots: <target>_references.txt (numbered citations with title, DOI, EXFOR entry and the data
used), <target>_references.bib (BibTeX) and, with --ref-format txt,bib,csv, a CSV table.  The titles and DOIs
come from the *_datasets.csv file next to the data file (written by exfor_retrieve.py and by this program).

Many points (--ms, --alpha, --hollow, --no-xerr, --no-yerr, --no-errorbars)
---------------------------------------------------------------------------
When there are many points the markers hide each other.  Series with many points are drawn first and the
sparse ones on top, so that small datasets are not hidden.  Make the markers smaller (--ms 2, or 1), transparent
(--alpha 0.4: dense regions look darker), open (--hollow) and leave out the error bars (--no-xerr, --no-yerr or
--no-errorbars), alone or together, for example  --ms 2 --alpha 0.5 --no-xerr.  The program prints a note when
a plot has more than 1500 points.

Automatic axes (--auto-axes)
----------------------------
--auto-axes chooses, for each panel, a linear or logarithmic scale for each axis and sets
adequate limits from the data (explicit --logx/--logy/--linx/--liny/--xlim/--ylim always win):
  x (energy)  logarithmic when the bulk of the points (5th to 95th percentile) spans a factor of
              50 or more, linear otherwise; angles are always linear (0-180 deg).
  y           logarithmic when the bulk of the positive values spans 3 decades or more, or when
              the maximum is 100 times the median (resonances); linear otherwise.
  limits      linear x starts at 0 when the data start near zero; log axes are rounded to whole
              decades; linear y starts at 0 and ends just above the highest point.
  outliers    a few points far outside the bulk (more than 3 times the 95th percentile in x, more
              than 4 times the 98th percentile in y; at most 5% / 3% of the points) are left out of
              the range, so that one wrong value does not flatten the plot; each panel then says
              how many points are outside the range.  Use --xlim/--ylim to see them.
With --sharex/--sharey the decision is made on all panels of the figure together.
Each decision is printed (and shown by --list).

Other x variables:  --x angle  (angular distributions, quantity DA)  and  --x Eout  (spectra).
Spectra and double-differential data (DE, DA/DE, PY/DA/DE, ...) usually hold several incident energies
and angles.  Select one with --at-energy E --tol T (incident energy within T MeV of E) and
--at-angle A --angle-tol T (angle within T degrees of A), or get one plot for each with --by-energy
and --by-angle.  A plot that mixes energies or angles is reported.  --max-plots (default 200) stops
the program before it writes a very large number of plots.
Several angles in one plot: --angle-labels draws every angle as a distribution with its angle written on
top of it (--energy-labels does the same for the incident energies of angular distributions, --x angle);
--stack 10 multiplies the distributions by 10, 100, 1000 ... in the order of the labels so that they do not
overlap (the label then says "x10^i").  2D maps instead: --map2d draws two variables (--axes, default
Eout,angle: outgoing energy against angle) with the value as colour; --plot3d draws the value as the height
of a 3D surface (--style surface), of 3D bars (bars) or as 3D points (scatter).  --axes can be any two of
E (incident energy), Eout (outgoing energy) and angle, for example E,Eout.  One plot is written for each
dataset and each value of the third variable (--ebins, --logz, --zlim, --cmap, --elev, --azim).
Example, neutron spectra of Be-9(p,n) at 30 degrees:
     python exfor_plot.py --target Be-9 --projectiles p --product n --quantity DA/DE --x Eout --at-angle 30 --logy

Evaluated data over the EXFOR data (--endf)
-------------------------------------------
--endf FILE ... draws the cross section of an evaluated nuclear data file in ENDF-6 format (ENDF/B, JEFF, JENDL,
CENDL, BROND, TENDL ...) as a line over the EXFOR points of the same target and reaction, for neutron-induced
cross sections (quantity SIG, incident energy on the x axis):

     python exfor_plot.py --target U-238 --projectiles n --product none --process F --logx --logy \\
            --endf n_092-U-238.endf --endf-label "ENDF/B-VIII.0"
     python exfor_plot.py --data data/Fe-56 --projectiles n --process TOT,EL --endf endf-b8/ jeff33/Fe056.jeff

* --endf takes files, wildcards and folders (a folder: only the files whose first material is the target of a plot
  are read).  Several files give several lines: compare evaluations.  Each line is labelled with the library and
  version that the file states ("ENDF/B-VIII.0"); --endf-label gives the names (one per file, in the order of the
  files).  A file may hold several materials; the one of the plotted target is used.
* The reaction type of the plot selects the cross section (File 3, MT number):  TOT 1, EL 2, NON 3, INL 4 (the
  sum of MT51-91 if the file has no MT4), 2N 16, 3N 17, F 18 (the sum of MT19, 20, 21, 38 if there is no MT18),
  G 102, P 103, D 104, T 105, HE3 106, A 107 ...  Plots of other quantities, angles, spectra, natural targets or
  isomeric products get no line (a note says why).  The line is in the unit of the plot (mb by default).
* RESONANCES.  An evaluated file stores the resolved resonance range as resonance parameters (File 2); File 3 holds
  only the smooth background there.  The program does not reconstruct the resonances, so by default the line
  starts where File 3 is the whole cross section: above the resolved range, and above the unresolved range when
  the file says that File 3 is only a background there (LSSF = 0).  A note tells where.  To see the resonances use a
  POINTWISE file (PENDF: what NJOY or PREPRO write after reconstructing and Doppler broadening; its resonance range
  is tabulated in File 3), which is drawn over the full range.  --endf-full draws the File 3 line over the whole
  range also for a file with resonance parameters (then only the background in the resonance range, as the legend says).
* The line covers the energy range of the plotted data (a little wider), or --emin/--emax/--xlim; --endf-full uses
  the whole file.  --endf-lw sets the line width; --endf-sub the number of points inserted in each interval that is
  not linear-linear (default 12).  The y range still comes from the EXFOR data (--auto-axes) or --ylim; on a linear
  y axis the peaks of an evaluation can be far above the data.

Output
------
One file per plot: every combination of target, projectile and product (and quantity) gets its
own figure.  The plots of each target are written to a folder named after the target, inside
--out (default: ./plots), that is ./plots/<target name>/:

    plots/Nb-93/Nb-93_d_92mNb.png
    plots/Nb-93/Nb-93_d_89Zr.png
    plots/Nb-93/Nb-93_p_92mNb.png
    plots/Cu-nat/Cu-nat_d_65Zn.png      (natural targets are named Cu-nat, Ti-nat, ...)

Files named like <target>_<projectile>_<product>[_<quantity>][_<process>].<format>; the quantity
is added when it is not SIG and the reaction type for reactions without a product (plots/U-238/U-238_n_none_F.png).
Formats: PNG (default), PDF, SVG or any format of matplotlib: --format png,pdf.
--combine puts several panels in one figure instead (--cols, --max-panels, --sharex, --sharey);
the combined figures of a target are named <target>_p1.png, <target>_p2.png ... or one multi-page PDF.
--list prints the plots (with their file names) and exits.
"""
import argparse
import collections
import csv
import glob
import math
import os
import re
import sys
from pathlib import Path

import numpy as np

__version__ = "1.4"
__build__ = "2026-10-27"       # date of the last change

try:
    import matplotlib
except ImportError:
    sys.exit("exfor_plot.py needs matplotlib:  pip install matplotlib")

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import exfor_retrieve as X
except ImportError:
    sys.exit("exfor_plot.py needs exfor_retrieve.py in the same folder.")
try:
    import endf_reader as ER                          # only needed with --endf
except ImportError:
    ER = None
if getattr(X, "API_LEVEL", 0) < 2:                 # the two scripts are updated together
    sys.exit(f"exfor_plot.py {__version__ if '__version__' in globals() else ''} needs the matching exfor_retrieve.py "
             f"in the same folder, but the one it finds is older: {getattr(X, '__version__', '?')} "
             f"(build {getattr(X, '__build__', 'none')}), file {getattr(X, '__file__', '?')}.\n"
             f"Replace both scripts with the current pair; python exfor_retrieve.py --version and "
             f"python exfor_plot.py --version must show the same build date.")

NUMERIC = {"projectile_Z", "projectile_A", "product_Z", "product_A", "E_MeV", "dE_MeV", "E_per_u_MeV", "value",
           "dvalue", "raw_value", "err_stat", "err_sys", "angle_deg", "E_out_MeV"}
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*", "h", "<", ">", "p"]
# Colours of the series: dark enough to be seen on a white background (contrast ratio of at least 3.9 against white),
# no yellow, and as different from each other as possible; the first ones are the ones used most.
PALETTE = ["#d62728", "#1f77b4", "#2e7d32", "#000000", "#c51b7d", "#542788", "#8c510a", "#666666", "#00838f",
           "#d55e00"]


# --------------------------------------------------------------------------
# reading and filtering
# --------------------------------------------------------------------------
def classify_data_args(patterns):
    """Split the --data items into those that exist and those that are missing (not retrieved yet)."""
    existing, missing = [], []
    for pat in patterns:
        if glob.has_magic(pat):
            existing.append(pat)
        elif os.path.isdir(pat):
            (existing if glob.glob(os.path.join(pat, "*_data.csv")) else missing).append(pat)
        elif os.path.exists(pat):
            existing.append(pat)
        else:
            missing.append(pat)
    return existing, missing


def target_from_path(path):
    """EXFOR target code named by a --data path (data/Rb-93, data/Ti-nat/EXFOR_TI-0_data.csv), or None."""
    base = os.path.basename(path.rstrip("/\\"))
    cands = []
    m = re.fullmatch(r"EXFOR_(.+)_data\.csv", base)
    if m:
        cands.append(m.group(1))
    cands.append(os.path.basename(os.path.dirname(path.rstrip("/\\"))) if base.lower().endswith(".csv") else base)
    for c in cands:
        try:
            return X.parse_target(c)
        except ValueError:
            continue
    return None


def save_location(path):
    """Folder and file prefix in which the data for a missing --data path are saved."""
    base = os.path.basename(path.rstrip("/\\"))
    if base.lower().endswith(".csv"):
        stem = base[:-4]
        return os.path.dirname(path) or ".", (stem[:-5] if stem.endswith("_data") else stem)
    return path, None


def no_data_message(path, is_dir):
    """Explain why --data found nothing and cannot retrieve it either."""
    here = os.getcwd()
    if is_dir:
        return (f"The folder '{path}' has no *_data.csv files and its name does not identify a target. Name the "
                f"folder after the target (data/Rb-93, data/Ti-nat) and the data are retrieved automatically, or run "
                f"exfor_retrieve.py for the target first.")
    if glob.has_magic(path):
        return f"No file matches '{path}' (current folder: {here})."
    msg = (f"'{path}' does not exist (current folder: {here}) and its name does not identify a target, so the data "
           f"cannot be retrieved automatically.\n"
           f"A data path named after the target, such as data/Rb-93 or data/Ti-nat, is retrieved automatically "
           f"when it does not exist; or retrieve the data first with exfor_retrieve.py for the target you need, "
           f"for example:\n    python exfor_retrieve.py --target <TARGET> --projectiles d --quantity SIG")
    parent = os.path.dirname(path.rstrip("/\\")) or "."
    if os.path.isdir(parent):
        names = sorted(d for d in os.listdir(parent) if os.path.isdir(os.path.join(parent, d)))
        if names:
            msg += f"\nFolders found in '{parent}': {', '.join(names)}"
    flat = sorted(glob.glob("EXFOR_*_data.csv"))
    if flat:
        msg += f"\nData files found in the current folder (older versions of exfor_retrieve.py): {', '.join(flat)}"
    return msg


T12_BY_ZAS = {}          # (Z, A, state) -> half-life text, from the datasets file, the retrieval or the database
_HL_DB = {"obj": None}


def halflife_on(args):
    return bool(getattr(args, "halflife", False) or getattr(args, "halflife_db", None))


def t12_text(args, z, a, state):
    """Half-life text of a nuclide for the titles: from the datasets file or the retrieval, else from the database."""
    if not halflife_on(args) or z is None or not a:
        return ""
    key = (int(z), int(a), state or "")
    if key in T12_BY_ZAS:
        return T12_BY_ZAS[key]
    if _HL_DB["obj"] is None:
        _HL_DB["obj"] = X.HalfLives(getattr(args, "halflife_db", None))
        if not _HL_DB["obj"].available:
            print(f"--halflife: no half-life database ({_HL_DB['obj'].error}). Give it with --halflife-db or the "
                  f"variable EXFOR_HALFLIFE_DB (Section 10.2 of the manual).", file=sys.stderr)
    h = _HL_DB["obj"]
    r = h.assign(*key) if h.available else None
    T12_BY_ZAS[key] = (r["text"] + ("?" if r["ambiguous"] else "")) if r else ""
    return T12_BY_ZAS[key]


def product_t12_par(args, r0):
    """' (T1/2 = ...)' or ' (stable)' for the product of a row (also n, p, d, t, 3He and alpha), '' if none."""
    if r0.get("product_Z") in (None, "") or not r0.get("product_A"):
        return ""
    try:
        z, a = int(float(r0.get("product_Z"))), int(float(r0.get("product_A")))
    except (TypeError, ValueError):
        return ""
    return t12_par(t12_text(args, z, a, r0.get("product_state") or ""))


def t12_par(text):
    """' (stable)' or ' ($T_{1/2}$ = 10.116 d)' for a title, '' when there is no half-life."""
    if not text:
        return ""
    return " (stable)" if text.lower().startswith("stable") else rf" ($T_{{1/2}}$ = {text})"


def register_t12(d):
    if d.get("product_Z") in (None, "") or not d.get("product_A"):
        return
    try:
        z, a = int(float(d.get("product_Z"))), int(float(d.get("product_A")))
    except ValueError:
        return
    if a and d.get("product_T12"):
        T12_BY_ZAS.setdefault((z, a, d.get("product_state") or ""), d["product_T12"])


def read_dataset_meta(patterns):
    """Dataset metadata (title, DOI, authors ...) by EXFOR entry from the *_datasets.csv files that sit next to the
    data files named in --data."""
    meta = {}
    for pat in patterns:
        if os.path.isdir(pat):
            pat = os.path.join(pat, "*_data.csv")
        for p in sorted(glob.glob(pat)):
            sib = re.sub(r"_data\.csv$", "_datasets.csv", p)
            if sib == p or not os.path.exists(sib):
                continue
            with open(sib, encoding="utf-8", newline="") as fh:
                for r in csv.DictReader(fh):
                    meta.setdefault(r["entry"], r)
                    register_t12(r)
    return meta


def write_plot_ascii(rows, args):
    """Write each selected dataset as an ASCII file with the units in the first row, one folder per target."""
    by_target = collections.OrderedDict()
    for r in rows:
        by_target.setdefault(r.get("target", ""), []).append(r)
    for tcode, rs in by_target.items():
        if args.ascii_dir:
            folder = Path(args.ascii_dir) / (target_dirname(tcode) if len(by_target) > 1 else "")
        else:
            folder = Path(args.data_dir) / target_dirname(tcode) / "ascii"
        w = X.AsciiWriter(folder, not args.ascii_no_errors, args.max_ascii, args.ascii_format, not args.ascii_no_blanks,
                          t12=(lambda z, a, st: t12_text(args, z, a, st)) if halflife_on(args) else None)
        w.add(rs)
        n = w.finish()
        print(f"  ASCII files: {n} files ({args.ascii_format} format) for {target_dirname(tcode)} written to "
              f"{folder} (with index.csv)", file=sys.stderr)
        if getattr(w, "no_unc", 0):
            print(f"  {w.no_unc} of the {n} files have no uncertainty column because EXFOR gives none for those data "
                  f"(column uncertainty of index.csv)", file=sys.stderr)
        if w.skipped:
            print(f"  warning: the limit of {args.max_ascii} ASCII files was reached; {w.skipped} datasets have no "
                  f"file. Use --ascii-format entry or quantity, restrict the selection, or raise --max-ascii.",
                  file=sys.stderr)


def write_plot_references(rows, meta, args, root, prefix_of, ref_formats):
    """Write the reference list of the datasets that are plotted, one file set per target."""
    by_target = collections.OrderedDict()
    agg = {}
    for r in rows:
        k = (r.get("target", ""), r["entry"], r.get("projectile", ""), r.get("product_label", ""), r.get("quantity", ""))
        a = agg.setdefault(k, {"entry": r["entry"], "projectile": k[2], "product": k[3], "quantity": k[4], "e_lo": None,
                               "e_hi": None, "n": 0, "first_author": r.get("first_author", ""), "year": r.get("year", ""),
                               "reference": r.get("reference", "")})
        a["n"] += 1
        e = r.get("E_MeV")
        if e is not None:
            a["e_lo"] = e if a["e_lo"] is None else min(a["e_lo"], e)
            a["e_hi"] = e if a["e_hi"] is None else max(a["e_hi"], e)
        by_target.setdefault(k[0], {})[k] = a
    written, missing_meta = [], 0
    for tcode, ag in by_target.items():
        usage = list(ag.values())
        missing_meta += len({u["entry"] for u in usage if u["entry"] not in meta})
        recs = X.reference_records(usage, meta, args.ref_authors)
        names = X.write_references(root / target_dirname(tcode), prefix_of(tcode), recs, ref_formats,
                                   f"in the plots of {target_dirname(tcode)} (projectiles {args.projectiles}, "
                                   f"product {args.product}, quantity {args.quantity})")
        written += [f"{target_dirname(tcode)}/{n}" for n in names]
        print(f"  references: {len(recs)} EXFOR entries for {target_dirname(tcode)}", file=sys.stderr)
    if missing_meta:
        print(f"  note: for {missing_meta} entries the datasets file was not found, so the references have only the "
              f"first author, the year and the EXFOR reference code (no title or DOI). Retrieve the data again, or "
              f"keep the *_datasets.csv file next to the data file.", file=sys.stderr)
    return written


def read_csv_files(patterns):
    paths = []
    for pat in patterns:
        is_dir = os.path.isdir(pat)
        orig = pat
        if is_dir:                                  # a folder written by exfor_retrieve.py: all its data files
            pat = os.path.join(pat, "*_data.csv")
        found = sorted(glob.glob(pat))
        if not found:
            sys.exit(no_data_message(orig, is_dir))
        paths += found
    rows = []
    for p in paths:
        rstr = {}
        dpath = p[:-len("_data.csv")] + "_datasets.csv" if p.endswith("_data.csv") else ""
        if dpath and os.path.isfile(dpath):              # the reaction text of each dataset, for complex reactions
            with open(dpath, encoding="utf-8", newline="") as fh:
                for d_ in csv.DictReader(fh):
                    rstr[d_.get("dataset", "")] = d_.get("reaction_string", "")
        with open(p, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                r["reaction_string"] = rstr.get(r.get("dataset", ""), "")
                for k in NUMERIC:
                    v = r.get(k)
                    if k in r:
                        try:
                            r[k] = float(v) if v not in (None, "") else None
                        except ValueError:
                            r[k] = None
                if not r.get("product_label"):             # files written by exfor_retrieve.py 2.0 have no product columns
                    pi = X.parse_product(r.get("product", ""))
                    r["product_label"], r["product_state"] = pi["label"], pi["state"]
                    r["product_Z"], r["product_A"] = pi["Z"], pi["A"]
                rows.append(r)
    return rows


def retrieve_rows(args, target_text=None, projectiles=None):
    """Retrieve the data of a target with the selection options of the command line."""
    target = X.parse_target(target_text or args.target)
    selection = X.Selection(projectiles or args.projectiles)
    psel = X.ProductSelection(args.product, exact=args.product_exact)
    quantities = None if args.quantity.upper() == "ALL" else {q.strip().upper() for q in args.quantity.split(",")}
    master = X.ensure_master(args.master, update=args.update)
    n_files, hits = X.find_candidate_files(master, X.build_prefilter(target), args.jobs, getattr(args, "facility", None))
    print(f"Scanned {n_files} EXFOR entries (master files of {X.master_date(master) or 'unknown date'}): "
          f"{len(hits)} contain {target} as target.", file=sys.stderr)
    rows, datasets = [], []
    for f in hits:
        try:
            ds, pts, _ = X.extract(f, target, selection, quantities, args.emin, args.emax, psel)
        except Exception as exc:
            print(f"  warning: could not parse {f}: {exc}", file=sys.stderr)
            continue
        rows += pts
        datasets += ds
    _rs = {d_.get("dataset"): d_.get("reaction_string", "") for d_ in datasets}
    for r_ in rows:
        r_["reaction_string"] = _rs.get(r_.get("dataset"), "")
    if halflife_on(args):
        hl = X.HalfLives(getattr(args, "halflife_db", None))
        if not hl.available:
            print(f"--halflife: no half-life database ({hl.error}). Give it with --halflife-db or the variable "
                  f"EXFOR_HALFLIFE_DB (Section 10.2 of the manual).", file=sys.stderr)
        X.annotate_halflives(datasets, hl)
        for d_ in datasets:
            register_t12(d_)
    else:
        X.annotate_halflives(datasets, None)
    return rows, datasets


def save_retrieved(rows, datasets, args, target_code, folder=None, prefix=None):
    """Store the data retrieved for plotting in <data-dir>/<target name>/, as exfor_retrieve.py does."""
    folder = Path(folder) if folder else Path(args.data_dir) / target_dirname(target_code)
    folder.mkdir(parents=True, exist_ok=True)
    prefix = prefix or args.data_prefix or f"EXFOR_{target_code.split('-', 1)[1]}"
    datasets = sorted(datasets, key=lambda r: (r["projectile"], r["quantity"], r["product"], r["entry"], r["subentry"]))
    names = []
    for name, fields, recs in (("data", X.POINT_FIELDS, rows), ("datasets", X.DATASET_FIELDS, datasets)):
        with open(folder / f"{prefix}_{name}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            for r in recs:
                w.writerow(X._clean(r, fields))
        names.append(f"{prefix}_{name}.csv")
    print(f"Retrieved data saved to {folder}: {', '.join(names)}", file=sys.stderr)


def apply_filters(rows, args, log):
    """Select the rows to plot; returns the rows and a dict of counts for the messages."""
    n0 = len(rows)
    sel = X.Selection(args.projectiles)
    psel = X.ProductSelection(args.product, exact=args.product_exact)
    qty = None if args.quantity.upper() == "ALL" else {q.strip().upper() for q in args.quantity.split(",")}
    drop_status = {s.strip().upper() for s in args.exclude_status.split(",") if s.strip()}
    procs = {p.strip().upper() for p in args.process.split(",") if p.strip()}
    br_in, br_out = set(), set()
    for tok in [t.strip().upper() for t in args.branch.split(",") if t.strip()]:
        (br_out if tok[0] in "-!" and len(tok) > 1 else br_in).add(tok.lstrip("-!") if tok[0] in "-!" and len(tok) > 1 else tok)
    inc_e = {e.strip() for e in args.entries.split(",") if e.strip()} if args.entries else None
    exc_e = {e.strip() for e in args.exclude_entries.split(",") if e.strip()}
    out = []
    for r in rows:
        if not sel.accepts(r.get("projectile_code", "")):
            continue
        if not psel.is_all:
            psel.set_target(r.get("target", ""))
            if not psel.accepts(X.parse_product(r.get("product", ""))):
                continue
        if qty and r.get("quantity") not in qty:
            continue
        if procs and (r.get("process") or "").upper() not in procs:
            continue
        if br_in or br_out:
            parts = {x for x in (r.get("branch") or "").upper().split("/") if x} or {"NONE"}
            if (br_in and not (br_in & parts)) or (br_out & parts):
                log["branch"] += 1
                continue
        if r.get("reaction_type") == "complex" and not args.include_complex:
            log["complex"] += 1
            continue
        if drop_status and drop_status & set(s.strip() for s in (r.get("status") or "").split(",")):
            log["status"] += 1
            continue
        if inc_e is not None and r.get("entry") not in inc_e and r.get("subentry") not in inc_e:
            continue
        if r.get("entry") in exc_e or r.get("subentry") in exc_e:
            continue
        if args.at_angle is not None:
            a = r.get("angle_deg")
            if a is None or abs(a - args.at_angle) > args.angle_tol:
                log["at_angle"] += 1
                continue
        e = r.get("E_MeV")
        if args.at_energy is not None:
            if e is None or abs(e - args.at_energy) > args.tol:
                log["at_energy"] += 1
                continue
        else:
            if args.emin is not None and e is not None and e < args.emin:
                continue
            if args.emax is not None and e is not None and e > args.emax:
                continue
        out.append(r)
    log["selected"] = len(out)
    log["input"] = n0
    return out


def product_N(r):
    a, z = r.get("product_A"), r.get("product_Z")
    return a - z if a is not None and z is not None else None


def plot_error(r):
    """Uncertainty of the value for the error bars: the total uncertainty of EXFOR (ERR-T or DATA-ERR); when the
    dataset gives only the statistical and/or the systematic uncertainty (ERR-S, ERR-SYS), these (added in
    quadrature when both are given); None if there is none."""
    d = r.get("dvalue")
    if d is not None:
        return abs(d)
    s_, y_ = r.get("err_stat"), r.get("err_sys")
    if s_ is not None and y_ is not None:
        return (s_ * s_ + y_ * y_) ** 0.5
    v = s_ if s_ is not None else y_
    return abs(v) if v is not None else None


def x_value(r, xmode):
    return {"E": r.get("E_MeV"), "angle": r.get("angle_deg"), "Eout": r.get("E_out_MeV"),
            "A": r.get("product_A"), "Z": r.get("product_Z"), "N": product_N(r)}[xmode]


def x_error(r, xmode):
    return r.get("dE_MeV") if xmode == "E" else None


# --------------------------------------------------------------------------
# labels
# --------------------------------------------------------------------------
def surname(author):
    a = (author or "").strip()
    return a.split(".")[-1].strip() or a


def target_label(code):
    m = re.fullmatch(r"(\d+)-([A-Z]{1,2})-(\d+)", code or "")
    if not m:
        return code or ""
    sym, a = m.group(2).capitalize(), int(m.group(3))
    return f"nat{sym}" if a == 0 else f"{a}{sym}"


def pretty(label):
    """Nuclide label with the mass number as a superscript (mathtext)."""
    special = {"alpha": r"$\alpha$", "gamma": r"$\gamma$", "none": "(no product)", "pbar": r"$\bar{p}$",
               "pi+": r"$\pi^+$", "pi-": r"$\pi^-$"}
    if label in special:
        return special[label]
    m = re.fullmatch(r"(\d+(?:[mg]\d?)?)([A-Z][a-z]?)(-[A-Za-z0-9+/]+)?", label or "")
    if m:
        return rf"$^{{{m.group(1)}}}$" + m.group(2) + (m.group(3) or "")
    return label


def series_label(r):
    lab = f"{surname(r.get('first_author'))} {r.get('year') or ''}".strip()
    if r.get("branch"):
        lab += f" ({r['branch']})"
    return lab


_TERM = re.compile(r"(\d{1,3})-([A-Z]{1,2})-(\d{1,3})(?:-[A-Z])?\(([^()]*)\)(?:(\d{1,3})-([A-Z]{1,2})-(\d{1,3}))?")


def nice_reaction(text):
    """Readable form of the REACTION text of a complex reaction: ((92-U-235(N,F),,SIG)/(3-LI-6(N,T)2-HE-4,,SIG)) ->
    235U(n,f) / 6Li(n,t)4He. Empty if the text has no nuclide."""
    if not text:
        return ""
    ms = list(_TERM.finditer(text))
    if not ms:
        return ""
    parts = []
    for i, m in enumerate(ms):
        tgt = f"{int(m.group(3))}{m.group(2).capitalize()}" if m.group(3) != "0" else f"nat{m.group(2).capitalize()}"
        prod = f"{int(m.group(7))}{m.group(6).capitalize()}" if m.group(5) else ""
        qty = re.match(r"\)?\s*,[^,()]*,\s*([A-Z/]+)", text[m.end():])   # branch, quantity
        parts.append(f"{tgt}({m.group(4).lower()}){prod}")
        if i + 1 < len(ms):
            gap = text[m.end():ms[i + 1].start()]
            op = "//" if "//" in gap else "/" if "/" in gap else "+" if "+" in gap else "*" if "*" in gap else "-" if "-" in gap.replace(",", "") else ","
            parts.append(op)
    return " ".join(parts)


target_dirname = X.target_dirname      # same folder names as exfor_retrieve.py (Nb-93, Ti-nat, ...)


def plot_stem(key, prefix, args=None):
    """File name (without extension) of the plot of a panel."""
    stem = (f"{prefix}_{safe(key[0])}_{safe(key[1])}" + (f"_{safe(key[2])}" if key[2] != "SIG" else "")
            + (f"_{safe(key[3]).upper()}" if key[3] else "") + (f"_{safe(key[5])}" if key[5] else ""))
    if key[6]:
        stem += f"_E{safe(key[6])}MeV"
    elif args is not None and args.at_energy is not None:
        stem += f"_E{args.at_energy:g}MeV"
    if key[7]:
        stem += f"_A{safe(key[7])}deg"
    elif args is not None and args.at_angle is not None:
        stem += f"_A{args.at_angle:g}deg"
    return stem


def safe(text):
    return re.sub(r"[^A-Za-z0-9+.-]+", "_", text).strip("_")


# --------------------------------------------------------------------------
# panels
# --------------------------------------------------------------------------
args_unit = [None]      # --unit given on the command line (set in main): then one unit is plotted everywhere


def sig3(x):
    """Incident energy rounded to 3 significant figures, as text."""
    return f"{x:.3g}"


def unit_family(u):
    """EXFOR units that differ only in PRD (products), PRT (particles) or PT written for P are the same unit: for the
    neutrons of the exclusive and the inclusive reactions, PRT/INC and PRD/INC are both neutrons per incident particle."""
    return re.sub(r"^(PRD|PRT|PT)(?=/)", "P", (u or "").upper()) if u else ""


def build_panels(rows, args):
    """{(projectile, product, quantity, process, target, unit, energy, angle): [rows]}: one plot per target,
    projectile and product.  The process is part of the key only when asked (--by-process) or for reactions
    without a product (fission, total, elastic, ...); the unit for quantities other than SIG; the incident
    energy and the angle with --by-energy and --by-angle."""
    panels = collections.defaultdict(list)
    merged = {}
    if getattr(args, "merge_products", False):          # products and quantities of the same unit go into one panel
        grp = collections.defaultdict(lambda: (set(), set()))
        for r in rows:
            g = grp[(r.get("projectile", ""), r.get("target", ""), unit_family(r.get("value_unit")))]
            g[0].add(r.get("product_label", ""))
            g[1].add(r.get("quantity", ""))
        merged = {k: ("+".join(sorted(v[0])), "+".join(sorted(v[1]))) for k, v in grp.items()}
    for r in rows:
        if merged:
            uf = unit_family(r.get("value_unit"))
            prod_m, qty_m = merged[(r.get("projectile", ""), r.get("target", ""), uf)]
            eb = ab = ""
            if args.by_energy:
                eb = sig3(r["E_MeV"]) if r.get("E_MeV") is not None else "unknown"
            if args.by_angle:
                ab = f"{r['angle_deg']:.1f}".rstrip("0").rstrip(".") if r.get("angle_deg") is not None else "unknown"
            panels[(r.get("projectile", ""), prod_m, qty_m, "", r.get("target", ""), uf, eb, ab)].append(r)
            continue
        split = args.by_process or r.get("product_label") == "none"
        proc = (r.get("process") or "").lower() if split else ""
        unit = (r.get("value_unit") or "") if (r.get("quantity") != "SIG" and not args_unit[0]) else ""
        eb = ab = ""
        if args.by_energy:
            eb = sig3(r["E_MeV"]) if r.get("E_MeV") is not None else "unknown"
        if args.by_angle:
            ab = f"{r['angle_deg']:.1f}".rstrip("0").rstrip(".") if r.get("angle_deg") is not None else "unknown"
        prod = "fragments" if args.x in ("A", "Z", "N") else r.get("product_label", "")
        panels[(r.get("projectile", ""), prod, r.get("quantity", ""), proc,
                r.get("target", ""), unit, eb, ab)].append(r)

    def num(t):
        try:
            return float(t)
        except ValueError:
            return float("inf")

    def order(k):
        r0 = panels[k][0]
        return (k[4], k[0], k[2], r0.get("product_Z") or 0, r0.get("product_A") or 0,
                r0.get("product_state") or "", k[1], k[3], k[5], num(k[6]), num(k[7]))
    return [(k, panels[k]) for k in sorted(panels, key=order)]


def mixing_note(panels, args):
    """Hint when a plot of spectra or angular distributions mixes several incident energies or angles."""
    n_e = n_a = 0
    for key, prs in panels:
        if not args.by_energy and args.at_energy is None and group_mode(args) != "energy" and len({sig3(r["E_MeV"]) for r in prs if r.get("E_MeV") is not None}) > 1:
            n_e += 1
        if not args.by_angle and args.at_angle is None and args.x != "angle" and group_mode(args) != "angle" and \
                len({round(r["angle_deg"], 1) for r in prs if r.get("angle_deg") is not None}) > 1:
            n_a += 1
    n_part = sum(1 for key, prs in panels for r in prs
                 if r.get("dvalue") is None and (r.get("err_stat") is not None or r.get("err_sys") is not None))
    n_s = 0
    if args.x == "E":                       # spectra plotted against the incident energy: vertical lines
        for key, prs in panels:
            by_e = collections.defaultdict(set)
            for r in prs:
                if r.get("E_MeV") is not None and r.get("E_out_MeV") is not None:
                    by_e[sig3(r["E_MeV"])].add(sig3(r["E_out_MeV"]))
            if by_e and max(len(v) for v in by_e.values()) >= 5:
                n_s += 1
    msg = []
    if n_part:
        msg.append(f"{n_part} points have no total uncertainty but a statistical and/or a systematic one (ERR-S, "
                   f"ERR-SYS): the error bars show it, the two added in quadrature when both are given")
    if n_s:
        msg.append(f"{n_s} plot(s) have an outgoing energy for each point (spectra at a few incident energies), which "
                   f"gives vertical lines against the incident energy: add --x Eout --by-energy to plot them as spectra")
    if n_e and args.x != "E":
        msg.append(f"{n_e} plot(s) mix several incident energies: add --by-energy (one plot each) or --at-energy E --tol T")
    if n_a:
        msg.append(f"{n_a} plot(s) mix several angles: add --by-angle (one plot each) or --at-angle A --angle-tol T")
    return msg



# --------------------------------------------------------------------------
# labels of the axes: quantity name and unit, and the name of the emitted particle
# --------------------------------------------------------------------------
unit_pretty = X.unit_pretty
_MISFIT_SEEN = set()


def y_label(qty, unit, xvars=(), rows=()):
    """Name and unit of the plotted quantity (Section 14.13 of the manual): the names and the rule for a spectrum
    coded as a cross section are those of the ASCII files, see exfor_retrieve.quantity_name. The rule looks at the
    data (points that have an outgoing energy), not at the variable on the x axis: the values of a neutron spectrum
    are per MeV also when they are plotted against the incident energy."""
    rows = list(rows)
    has_eout = "Eout" in set(xvars) or any(r.get("E_out_MeV") is not None for r in rows)
    names = X.QTY_NAMES.get(qty)
    if names is None:
        return f"{qty} ({X.unit_pretty(unit)})" if X.unit_pretty(unit) else qty
    if not X.unit_fits_quantity(qty, unit) and (qty, unit) not in _MISFIT_SEEN:
        _MISFIT_SEEN.add((qty, unit))
        print(f"  note: the unit {unit} that EXFOR gives for the quantity {qty} does not fit it, so the label shows "
              f"the EXFOR code and unit as they are", file=sys.stderr)
    name, u = X.quantity_name(qty, unit, has_eout, rows, ascii=False)
    return f"{name} ({u})" if u else name


def emitted_name(rows):
    c = X.emitted_code(rows)
    return X.EMITTED[c][0] if c else None


def x_label(xmode, rows):
    if xmode == "Eout":
        n = emitted_name(rows)
        return f"{n} energy (MeV)" if n else "Outgoing energy (MeV)"
    return {"E": "Incident energy (MeV)", "angle": "Angle (deg)", "A": "Mass number A of the product",
            "Z": "Atomic number Z of the product", "N": "Neutron number N of the product"}[xmode]


def axis_label(name, rows):
    return x_label("Eout", rows) if name == "Eout" else AXIS_NAMES[name]


def panel_title(key, rows, target, args=None, hl_args=None):
    proj, prod, qty, kproc = key[:4]
    procs = sorted({(r.get("process") or "").lower() for r in rows})
    proc = kproc or (procs[0] if len(procs) == 1 and procs[0] else "x")
    projl = pretty(proj)
    prodl = ", ".join(pretty(x) for x in prod.split("+")) if "+" in prod else pretty(prod)
    if proj == "none":                       # no incident particle: decays and spontaneous processes
        dec = {"b-": r"$\beta^-$", "b+": r"$\beta^+$", "f": "SF"}.get(proc, proc)
        inner = dec
    else:
        inner = f"{projl},{proc}"
    tgt = pretty(target_label(target))
    p_t12 = ""
    hl_args = hl_args if hl_args is not None else args
    if hl_args is not None and halflife_on(hl_args):
        tz, ta = X._target_za(target)
        tt = t12_text(hl_args, tz, ta, "") if ta else ""
        if tt and not tt.lower().startswith("stable"):          # a radioactive target: its half-life too
            tgt += t12_par(tt)
        if prod not in ("none", "fragments") and rows:
            p_t12 = product_t12_par(hl_args, rows[0])
    title = f"{tgt}({inner}){prodl}{p_t12}" if prod not in ("none", "fragments") else f"{tgt}({inner})"
    extra = []
    if len(key) > 7:
        if key[6]:
            extra.append(f"E = {key[6]} MeV" if key[6] != "unknown" else "E unknown")
        if key[7]:
            extra.append(rf"$\theta$ = {key[7]}$^\circ$" if key[7] != "unknown" else "angle unknown")
    if args is not None:
        if args.at_energy is not None and not (len(key) > 6 and key[6]):
            extra.append(f"E = {args.at_energy:g} MeV")
        if args.at_angle is not None and not (len(key) > 7 and key[7]):
            extra.append(rf"$\theta$ = {args.at_angle:g}$^\circ$")
    return title + (f"  [{qty}]" if qty and qty != "SIG" else "") + (("  " + ", ".join(extra)) if extra else "")


def assign_styles(rows):
    """Same colour and marker for the same entry in every panel."""
    import matplotlib.pyplot as plt
    palette = PALETTE
    entries = sorted({r["entry"] for r in rows}, key=lambda e: (
        min((r.get("year") or "9999") for r in rows if r["entry"] == e), e))
    return {e: (palette[i % len(palette)], MARKERS[(i // 3) % len(MARKERS)]) for i, e in enumerate(entries)}


# cross sections that EXFOR gives multiplied by a power of the incident energy: unit -> (energy unit in MeV, power)
WEIGHTED_UNITS = {"B*EV": (1e-6, 1.0, 1e3), "B*KEV": (1e-3, 1.0, 1e3), "B*MEV": (1.0, 1.0, 1e3),
                  "MB*MEV": (1.0, 1.0, 1.0), "B*RT-EV": (1e-6, 0.5, 1e3)}


def convert_weighted(rows, log):
    """Convert sigma*E and sigma*sqrt(E) data (units B*EV, B*KEV, B*MEV, MB*MEV, B*RT-EV) to mb."""
    for r in rows:
        spec = WEIGHTED_UNITS.get((r.get("value_unit") or "").upper())
        e = r.get("E_MeV")
        if not spec or r.get("quantity") != "SIG" or e is None or e <= 0 or r.get("value") is None:
            continue
        eunit, power, to_mb = spec
        f = to_mb / (e / eunit) ** power               # divide by E (or sqrt(E)) in the unit of the factor
        log["weighted_" + r["value_unit"].upper()] += 1
        r["value"] = r["value"] * f
        for k_ in ("dvalue", "err_stat", "err_sys"):
            if r.get(k_) is not None:
                r[k_] = r[k_] * f
        r["value_unit"] = "mb"


def choose_units(rows, args, log):
    """Keep one unit per quantity: --unit, mb for SIG, else the most frequent one."""
    by_q = collections.defaultdict(collections.Counter)
    for r in rows:
        by_q[r.get("quantity")][r.get("value_unit")] += 1
    unit_of = {}
    for q, cnt in by_q.items():
        if args.unit:
            unit_of[q] = args.unit
        elif q == "SIG" and "mb" in cnt:
            unit_of[q] = "mb"
        else:
            unit_of[q] = cnt.most_common(1)[0][0]
    kept = []
    for r in rows:
        q = r.get("quantity")
        if args.unit or q == "SIG":
            if r.get("value_unit") == unit_of.get(q):
                kept.append(r)
            else:
                log["unit"] += 1
        else:
            kept.append(r)                      # other quantities: one panel per unit (see build_panels)
    return kept, unit_of


def quantile(sorted_vals, q):
    """Linear-interpolation quantile of an already sorted list."""
    n = len(sorted_vals)
    if n == 1:
        return sorted_vals[0]
    pos = (n - 1) * q
    lo = int(math.floor(pos))
    hi = min(lo + 1, n - 1)
    return sorted_vals[lo] * (1 - (pos - lo)) + sorted_vals[hi] * (pos - lo)


def group_mode(args):
    """'angle' or 'energy' when every angle (or incident energy) is drawn as a distribution of its own in one plot,
    which is so with the label options and with --stack; else None. The labels are drawn only with --angle-labels or
    --energy-labels."""
    if args.angle_labels:
        return "angle"
    if args.energy_labels:
        return "energy"
    if args.stack > 1:
        return "energy" if args.x == "angle" else "angle"
    return None


def group_value(r, mode):
    """Angle (0.1 degree) or incident energy (3 significant figures) of a point, or None."""
    if mode == "angle":
        return round(r["angle_deg"], 1) if r.get("angle_deg") is not None else None
    if mode == "energy":
        return float(sig3(r["E_MeV"])) if r.get("E_MeV") is not None else None
    return None


_STACK_WARNED = [False]


def group_factors(rows, args):
    """{group value: multiplying factor}; the factor is stack**i with i the position of the value in the plot."""
    mode = group_mode(args)
    if mode is None:
        return {}
    vals = sorted({group_value(r, mode) for r in rows if group_value(r, mode) is not None})
    f = args.stack if args.stack > 1 else 1.0
    if f > 1 and (len(vals) - 1) * math.log10(f) > 250:        # the factors would overflow: do not stack
        if not _STACK_WARNED[0]:
            _STACK_WARNED[0] = True
            print(f"  note: {len(vals)} distributions are too many to stack with --stack {f:g} (the factors would "
                  f"be beyond 10^250): they are drawn without scaling", file=sys.stderr)
        return {v: 1.0 for v in vals}
    return {v: f ** i for i, v in enumerate(vals)}


def panel_points(rows, args):
    """x, y and y error of the points of a panel that can be drawn."""
    xs, ys, es = [], [], []
    mode = group_mode(args)
    fac = group_factors(rows, args)
    for p in rows:
        x, y = x_value(p, args.x), p.get("value")
        if x is None or y is None:
            continue
        f = fac.get(group_value(p, mode), 1.0) if mode else 1.0
        xs.append(x)
        ys.append(y * f)
        es.append((plot_error(p) or 0.0) * f)
    return xs, ys, es


def plain_axes(args):
    """Axes settings when --auto-axes is not used."""
    return {"logx": args.logx, "logy": args.logy, "xlim": args.xlim, "ylim": args.ylim, "note": "", "auto": False}


def decide_x(xs, args):
    """(log?, limits) for the x axis."""
    n = len(xs)
    if n == 0:
        return args.logx, args.xlim
    sx = sorted(xs)
    if args.x == "angle":
        lo, hi = sx[0], sx[-1]
        lim = (0.0, 180.0) if lo >= -1 and hi <= 181 else (lo - 0.04 * (hi - lo), hi + 0.04 * (hi - lo))
        return False, lim
    pos = [x for x in sx if x > 0]
    if args.logx:
        log = True
    elif args.linx:
        log = False
    else:
        log = len(pos) >= 5 and len(pos) >= 0.95 * n and quantile(pos, 0.95) / quantile(pos, 0.05) >= 50
    if log and pos:
        lo = 10 ** math.floor(math.log10(pos[0]))
        hi = 10 ** math.ceil(math.log10(pos[-1]))
        return True, (lo, hi if hi > lo else lo * 10)
    q95 = quantile(sx, 0.95)
    xmax = sx[-1]
    far = [x for x in sx if q95 > 0 and x > 3 * q95]
    if far and len(far) <= 0.05 * n:                     # a few points far beyond the bulk: leave them out
        xmax = max(x for x in sx if x <= 3 * q95)
    xmin = sx[0]
    span = max(xmax - xmin, 0.05 * abs(xmax), 1e-12)
    lo = 0.0 if (xmin >= 0 and xmin <= 0.3 * xmax) else xmin - 0.04 * span
    return False, (lo, xmax + 0.04 * span)


def decide_y(ys, es, args):
    """(log?, limits) for the y axis."""
    n = len(ys)
    if n == 0:
        return args.logy, args.ylim
    sy = sorted(ys)
    pos = [y for y in sy if y > 0]
    if args.logy:
        log = True
    elif args.liny:
        log = False
    else:
        log = False
        if len(pos) >= 5 and len(pos) >= 0.9 * n:
            decades = math.log10(quantile(pos, 0.95) / quantile(pos, 0.05))
            med = quantile(pos, 0.5)
            log = decades >= 3 or (med > 0 and sy[-1] / med >= 100)
    if log and pos:
        lo = 10 ** math.floor(math.log10(quantile(pos, 0.01)))
        hi = 10 ** math.ceil(math.log10(pos[-1]))
        return True, (lo, hi if hi > lo else lo * 10)
    q98 = quantile(sy, 0.98)
    far = [y for y in sy if q98 > 0 and y > 4 * q98]
    clip = bool(far) and len(far) <= 0.03 * n
    tops = [y + min(e, abs(y)) for y, e in zip(ys, es) if not (clip and y > 4 * q98)]
    top = max(tops) if tops else sy[-1]
    bottom = 0.0 if (sy[0] >= 0 and not args.no_zero) else sy[0] - 0.05 * max(top - sy[0], 1e-12)
    top = bottom + (top - bottom) * 1.08 if top > bottom else bottom + 1.0
    return False, (bottom, top)


def finalize_axes(d, xs, ys):
    """Count the points outside the limits and write the note shown in the panel."""
    xl, yl = d["xlim"], d["ylim"]
    out = 0
    for x, y in zip(xs, ys):
        bad = False
        if xl and not (xl[0] <= x <= xl[1]):
            bad = True
        if yl and not (yl[0] <= y <= yl[1]):
            bad = True
        if d["logx"] and x <= 0 or d["logy"] and y <= 0:
            bad = True
        out += bad
    d["note"] = f"{out} point{'s' if out != 1 else ''} outside the range" if out else ""
    return d


def auto_axes(points, args, share=None):
    """Axes settings for a list of panels (points = [(xs, ys, es), ...]); share = union decision source."""
    decs = []
    for xs, ys, es in points:
        lx, xl = decide_x(xs, args)
        ly, yl = decide_y(ys, es, args)
        decs.append({"logx": lx, "logy": ly, "xlim": args.xlim or xl, "ylim": args.ylim or yl, "auto": True})
    if (args.sharex or args.sharey) and len(points) > 1:
        ux = [x for p in points for x in p[0]]
        uy = [y for p in points for y in p[1]]
        ue = [e for p in points for e in p[2]]
        lx, xl = decide_x(ux, args)
        ly, yl = decide_y(uy, ue, args)
        for d in decs:
            if args.sharex:
                d["logx"], d["xlim"] = lx, args.xlim or xl
            if args.sharey:
                d["logy"], d["ylim"] = ly, args.ylim or yl
    for d, (xs, ys, es) in zip(decs, points):
        finalize_axes(d, xs, ys)
    return decs


def axes_text(d):
    f = lambda lim: "auto" if not lim else f"{lim[0]:.3g}-{lim[1]:.3g}"
    return f"x {'log' if d['logx'] else 'lin'} {f(d['xlim'])}   y {'log' if d['logy'] else 'lin'} {f(d['ylim'])}"


single_hint = [False]    # the overlap hint is printed once per run



def _spread(ys, h, lo, hi):
    """Vertical positions (points) of labels of height h that are as near as possible to ys without overlapping."""
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    pos = [ys[i] for i in order]
    for k in range(1, len(pos)):                      # push upwards what overlaps the label below
        pos[k] = max(pos[k], pos[k - 1] + h)
    if pos and pos[-1] > hi:                          # too high: shift down
        pos[-1] = hi
        for k in range(len(pos) - 2, -1, -1):
            pos[k] = min(pos[k], pos[k + 1] - h)
    out = [0.0] * len(ys)
    for k, i in enumerate(order):
        out[i] = pos[k]
    return out


def place_end_labels(ax, ends, mode, args, axes):
    """Label every distribution next to its last point, to the right of the data, without overlaps, and extend the
    x range to the right to make room for the labels (a leader line joins a label that had to move to its point)."""
    fig, dpi = ax.figure, ax.figure.dpi
    try:
        rend = fig.canvas.get_renderer()
    except Exception:                                  # a backend without a renderer: estimate the sizes
        rend = None
    order = sorted(ends)
    texts = []
    for i, grp in enumerate(order):
        txt = f"{grp:g}$^\\circ$" if mode == "angle" else f"{grp:g} MeV"
        if args.stack > 1 and i > 0:
            txt += f" (x{args.stack:g}$^{{{i}}}$)"
        texts.append(txt)
    bb = ax.get_window_extent(rend) if rend is not None else ax.bbox
    W, H = bb.width * 72.0 / dpi, bb.height * 72.0 / dpi          # size of the axes in points
    fs = 8.0
    n_all = len(order)
    max_fit = max(2, int(0.92 * H / (6.0 * 1.5)))                 # labels of 6 points still fit one above the other
    if n_all > max_fit:                                           # too many: label an evenly spaced subset
        keep = sorted({round(k * (n_all - 1) / (max_fit - 1)) for k in range(max_fit)})
        order, texts = [order[i] for i in keep], [texts[i] for i in keep]
        print(f"  note: {n_all} distributions are too many to label without overlap: {len(order)} evenly spaced "
              f"ones are labelled (select fewer with --at-energy, --at-angle or --entries)", file=sys.stderr)
    if len(order) * fs * 1.5 > 0.92 * H:                          # many labels: smaller text
        fs = max(6.0, 0.92 * H / (len(order) * 1.5))

    def width(txt):
        if rend is not None:
            t = ax.text(0, 0, txt, fontsize=fs, fontweight="bold")
            w = t.get_window_extent(rend).width * 72.0 / dpi
            t.remove()
            return w + 5.0
        return 0.62 * fs * len(txt) + 5.0

    ws = [width(t) for t in texts]
    left, right = ax.get_xlim()
    logx = axes["logx"]
    T = (lambda v: math.log10(v)) if logx else (lambda v: v)
    Ti = (lambda v: 10.0 ** v) if logx else (lambda v: v)
    # the labels stand in one column to the right of all the labelled data (and of their error bars), so that no
    # label covers the points of another distribution; each label is next to the last point of its distribution when
    # that is the rightmost one, and is joined to it by a thin line when its distribution ends earlier
    x_col = max(ends[g][1] + (ends[g][4] if ends[g][4] and ends[g][1] + ends[g][4] > 0 else 0.0) for g in order)
    if not axes["xlim"]:                           # make room on the right for the labels
        tl, tr = T(left), T(right)
        room = W - 2.0 - 8.0 - max(ws)
        if room > 5.0 and T(x_col) > tl:
            need = tl + (T(x_col) - tl) * W / room
            if need > tr:
                ax.set_xlim(left, Ti(min(need, tl + (tr - tl) * 2.0)))
    left, right = ax.get_xlim()
    tl, tr = T(left), T(right)
    off = [8.0 + max(0.0, (T(x_col) - T(ends[g][1])) / (tr - tl) * W) if ends[g][1] > 0 or not logx else 8.0
           for g in order]                          # distance from the point to its label, in points
    ypts = [ax.transData.transform((ends[g][1], ends[g][2]))[1] * 72.0 / dpi for g in order]
    h = fs * 1.5
    y0, y1 = bb.y0 * 72.0 / dpi, bb.y1 * 72.0 / dpi
    adj = _spread(ypts, h, y0 + h / 2.0, y1 - h / 2.0)
    for grp, txt, o, yp, ya in zip(order, texts, off, ypts, adj):
        color = ends[grp][3]
        shifted = abs(ya - yp) > 2.0 or o > 14.0
        ax.annotate(txt, (ends[grp][1], ends[grp][2]), xytext=(o, ya - yp), textcoords="offset points",
                    ha="left", va="center", fontsize=fs, fontweight="bold", color="black", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=color, lw=0.8, alpha=0.9),
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.6, shrinkA=0, shrinkB=2) if shifted else None,
                    annotation_clip=False)

# --------------------------------------------------------------------------
# evaluated data (ENDF files) drawn over the EXFOR data
# --------------------------------------------------------------------------
ENDF_STYLES = [("#222222", "-"), ("#0072b2", "--"), ("#d55e00", "-."), ("#009e73", ":"), ("#cc79a7", "-"),
               ("#7f7f7f", "--")]
_endf_notes = set()


def endf_note(msg):
    """Print a note about the ENDF lines once."""
    if msg not in _endf_notes:
        _endf_notes.add(msg)
        print(f"  note: {msg}", file=sys.stderr)


def endf_expand(items):
    """Expand the --endf items (files, wildcards, folders) into ([files], [folders])."""
    files, folders = [], []
    for it in items or []:
        hits = sorted(glob.glob(os.path.expanduser(it))) or [it]
        for h in hits:
            if os.path.isdir(h):
                folders.append(h)
            elif os.path.isfile(h):
                files.append(h)
            else:
                sys.exit(f"--endf: '{h}' is not a file or a folder.")
    return files, folders


def peek_za(path):
    """ZA of the first material of an ENDF file, from its first two cards (no full read); None if it is not ENDF."""
    try:
        with open(path, "r", encoding="latin-1") as fh:
            fh.readline()
            second = fh.readline()
        if len(second) < 75 or second[70:75].strip() != "1451":
            return None
        return int(ER.efloat(second[0:11]))
    except (OSError, ValueError):
        return None


class EndfLibrary:
    """The ENDF files given with --endf: the files are read at once, those of a folder when a plot needs them."""

    def __init__(self, items, labels):
        files, folders = endf_expand(items)
        self.cache = {}                  # path -> Tape
        self.explicit = [(f, labels[i] if labels and i < len(labels) else None) for i, f in enumerate(files)]
        if labels and len(labels) != len(files):
            print(f"  note: --endf-label has {len(labels)} label(s) for {len(files)} file(s); "
                  f"the labels go to the files in order, the files without a label use the name the file states",
                  file=sys.stderr)
        self.folder_index = {}           # (Z, A) -> [path]
        for fo in folders:
            n_ok = 0
            for path in sorted(glob.glob(os.path.join(fo, "*"))):
                za = peek_za(path) if os.path.isfile(path) else None
                if za:
                    self.folder_index.setdefault((za // 1000, za % 1000), []).append(path)
                    n_ok += 1
            print(f"  ENDF folder {fo}: {n_ok} file(s) recognised", file=sys.stderr)
        for path, _lab in self.explicit:
            self.tape(path)              # an unreadable file shows up at once
        self.styles = {}

    def tape(self, path):
        if path not in self.cache:
            try:
                t = ER.read_endf(path)
            except (OSError, ValueError, ER.EndfError) as exc:
                sys.exit(f"--endf: cannot read '{path}' as an ENDF-6 file: {exc}")
            if not t.materials:
                sys.exit(f"--endf: no ENDF material found in '{path}' (an ENDF-6 file has File 1, MT 451)")
            self.cache[path] = t
            for m in t.materials:
                print(f"  ENDF {Path(path).name}: {m.label}, Z={m.z} A={m.a}{' (isomer)' if m.liso else ''}; "
                      f"{m.resonance_note()}", file=sys.stderr)
        return self.cache[path]

    def materials(self, z, a):
        """[(Material, label, path)] for the target Z, A: the files given first, then those of the folders."""
        out = []
        for path, lab in self.explicit:
            m = self.tape(path).find(z, a)
            if m is not None:
                out.append((m, lab or m.label, path))
        for path in self.folder_index.get((z, a), []):
            m = self.tape(path).find(z, a)
            if m is not None:
                out.append((m, m.label, path))
        return out

    def style(self, path):
        """The same colour and line style for the same file in every plot."""
        if path not in self.styles:
            self.styles[path] = ENDF_STYLES[len(self.styles) % len(ENDF_STYLES)]
        return self.styles[path]


def endf_mt_for_panel(key, rows):
    """(MT, reaction type) of the evaluated cross section that belongs to a panel, or (None, why not)."""
    if key[2] != "SIG":
        return None, "only cross sections (quantity SIG) have an ENDF line"
    if key[0] != "n":
        return None, "the ENDF files are neutron-induced: no line in plots of projectile " + str(key[0])
    if key[6] or key[7]:
        return None, "no ENDF line in plots of one incident energy or angle"
    procs = {(r.get("process") or "").upper() for r in rows}
    mts = {ER.PROCESS_TO_MT[p]: p for p in procs if p in ER.PROCESS_TO_MT}
    if not mts:
        return None, "reaction type " + "/".join(sorted(x for x in procs if x) or ["?"]) + " has no ENDF cross section"
    if len(mts) > 1:
        return None, "this plot mixes reaction types " + "/".join(sorted(mts.values())) + ": use --by-process or --process"
    mt = next(iter(mts))
    if {(r.get("product_state") or "") for r in rows} - {"", "G"} and mt not in (1, 2, 3, 18):
        return None, "isomeric products have no ENDF line (File 3 gives the total of the reaction)"
    return mt, mts[mt]


def clip_curve(e, s, lo, hi):
    """Part of a curve between lo and hi (None = no limit), with a point at each limit."""
    m = e > 0
    e, s = e[m], s[m]
    if len(e) < 2:
        return e, s
    if lo is not None and e[0] < lo < e[-1]:
        i = int(np.searchsorted(e, lo))
        e, s = np.concatenate([[lo], e[i:]]), np.concatenate([[float(np.interp(lo, e, s))], s[i:]])
    if hi is not None and e[0] < hi < e[-1]:
        i = int(np.searchsorted(e, hi, side="right"))
        e, s = np.concatenate([e[:i], [hi]]), np.concatenate([s[:i], [float(np.interp(hi, e, s))]])
    keep = np.ones(len(e), dtype=bool)
    if lo is not None:
        keep &= e >= lo
    if hi is not None:
        keep &= e <= hi
    return e[keep], s[keep]


def draw_endf(ax, key, rows, unit, args, axes):
    """Draw the ENDF lines of a panel (before the axes are set); returns the number of lines."""
    lib = getattr(args, "endf_lib", None)
    if lib is None:
        return 0
    mt, what = endf_mt_for_panel(key, rows)
    name = f"{target_label(key[4])} {key[0]} {key[1] if key[1] != 'none' else ''}".strip()
    if mt is None:
        endf_note(f"{name}: {what}")
        return 0
    z, a = X._target_za(key[4])
    if not a:
        endf_note(f"{name}: a natural target has no ENDF line (an ENDF file is one nuclide)")
        return 0
    mats = lib.materials(z, a)
    if not mats:
        endf_note(f"no ENDF material for {target_label(key[4])} in the files given with --endf")
        return 0
    unit_mb = X.B_PREFIX.get((unit or "mb").upper())            # value in mb = value in the unit x unit_mb
    if unit_mb is None:
        endf_note(f"{name}: the unit '{unit}' of the plot is not a cross-section unit, so there is no ENDF line")
        return 0
    f = 1000.0 / unit_mb                                         # barn -> plotted unit
    xs_ = [x_value(r, "E") for r in rows if x_value(r, "E") is not None and x_value(r, "E") > 0]
    lo, hi = (axes["xlim"] if axes.get("xlim") else args.xlim) or (None, None)
    lo = args.emin if lo is None else lo
    hi = args.emax if hi is None else hi
    if xs_ and not args.endf_full:                               # the range of the data, a little wider
        dlo, dhi = min(xs_), max(xs_)
        if axes.get("logx") or dhi > 20 * dlo:
            dlo, dhi = dlo / 1.3, dhi * 1.3
        else:
            dlo, dhi = max(dlo - 0.05 * (dhi - dlo), 0.0), dhi + 0.05 * (dhi - dlo)
        lo = dlo if lo is None else lo
        hi = dhi if hi is None else hi
    n_lines = 0
    labels_ = [lab for _m, lab, _p in mats]
    for mat, label, path in mats:
        if labels_.count(label) > 1:                              # two files state the same library: tell them apart
            label = f"{label} [{Path(path).name}]"
        res = mat.sigma(mt, sub=args.endf_sub)
        if res is None:
            endf_note(f"{label}: the file has no MT{mt} ({what}) for {target_label(key[4])}")
            continue
        e_mev, sig = res[0] * 1e-6, res[1] * f
        lo_i, suffix = lo, ""
        if mt in ER.RESONANCE_MTS:
            c_ev, why = mat.complete_from()
            below = bool(np.any((e_mev > 0) & (e_mev < c_ev * 1e-6) & (e_mev >= (lo_i or 0.0))))
            if c_ev and not args.endf_full and below:
                lo_i = max(lo_i or 0.0, c_ev * 1e-6)
                endf_note(f"{label}, {target_label(key[4])} ({what}): the line starts at {c_ev * 1e-6:.6g} MeV, above the "
                          f"{why}. For the resonances use a pointwise (PENDF) file; --endf-full also draws File 3 below "
                          f"that energy (the background only)")
            elif c_ev and below:
                suffix = f" (File 3 only below {c_ev * 1e-6:.3g} MeV)"
        ex, sy = clip_curve(e_mev, sig, lo_i, hi)
        if len(ex) < 2:
            endf_note(f"{label}: the ENDF line of {target_label(key[4])} ({what}) is outside the energy range of the plot")
            continue
        if axes["logy"]:
            sy = np.where(sy > 0, sy, np.nan)
        col, ls = lib.style(path)
        ax.plot(ex, sy, color=col, ls=ls, lw=args.endf_lw, label=label + suffix, zorder=6)
        n_lines += 1
    return n_lines


def draw_panel(ax, key, rows, styles, unit, args, target, axes, single=False):
    mode = group_mode(args)
    draw_labels = bool(args.angle_labels or args.energy_labels)
    fac = group_factors(rows, args)
    series = collections.OrderedDict()
    for r in rows:
        g = group_value(r, mode) if mode else None
        iso_k = ""
        if args.x in PRODUCT_AXES and (r.get("product_state") or "") not in ("", "G"):
            iso_k = "|" + r["product_state"]                 # isomers of a nuclide are drawn as a series of their own
        series.setdefault((r["entry"], r["subentry"], r.get("branch", "") + iso_k, g), []).append(r)
    # complex reactions (ratios and so on): the datasets of one entry that are different reactions get their own colour
    # and marker, and the legend says the reaction; datasets of the same reaction share one legend entry
    variants = collections.OrderedDict()
    for k_, v_ in series.items():
        if v_[0].get("reaction_type") == "complex":
            rs_ = nice_reaction(v_[0].get("reaction_string"))
            if rs_:
                variants.setdefault(k_[0], [])
                if rs_ not in variants[k_[0]]:
                    variants[k_[0]].append(rs_)
    rs_legend = set()
    labels_used = collections.Counter(series_label(v[0]) for v in series.values())
    entry_labels = collections.Counter((series_label(v[0]), k[0]) for k, v in series.items())
    n = 0
    legend_done, peaks = set(), {}
    # draw the series with many points first and the sparse ones on top, so that small datasets stay visible
    by_size = sorted(series, key=lambda k: -len(series[k]))
    zmap = {k: 2.0 + 0.002 * i for i, k in enumerate(by_size)}
    for (entry, sub, branch, grp), pts in sorted(series.items(), key=lambda kv: (kv[1][0].get("year") or "", kv[0][:3],
                                                                              kv[0][3] if kv[0][3] is not None else -1)):
        pts = [p for p in pts if x_value(p, args.x) is not None and p.get("value") is not None]
        if axes["logy"]:
            pts = [p for p in pts if p["value"] > 0]
        if axes["logx"]:
            pts = [p for p in pts if x_value(p, args.x) > 0]
        if not pts:
            continue
        pts.sort(key=lambda p: x_value(p, args.x))
        xs = [x_value(p, args.x) for p in pts]
        f = fac.get(grp, 1.0) if mode else 1.0
        ys = [p["value"] * f for p in pts]
        yerr = [(plot_error(p) or 0.0) * f for p in pts]
        xerr = None if args.no_xerr or args.no_errorbars or args.x != "E" else [abs(p["dE_MeV"]) if p.get("dE_MeV") is not None else 0.0
                                                          for p in pts]
        color, marker = styles[entry]
        curve = "CURVE" in (pts[0].get("status") or "")
        label = series_label(pts[0])
        rs_ = nice_reaction(pts[0].get("reaction_string")) if pts[0].get("reaction_type") == "complex" else ""
        if rs_ and entry in variants:
            kv_ = variants[entry].index(rs_)
            if len(variants[entry]) > 1:
                color = PALETTE[(PALETTE.index(color) + 3 * kv_) % len(PALETTE)] if color in PALETTE else color
                marker = MARKERS[(MARKERS.index(marker) + kv_) % len(MARKERS)] if marker in MARKERS else marker
            label += f" [{entry}]: {rs_}"
            if (entry, rs_) in rs_legend:
                label = "_nolegend_"
            rs_legend.add((entry, rs_))
        elif labels_used[label] > 1:
            label += f" [{entry}]"
            if entry_labels[(series_label(pts[0]), entry)] > 1:       # several subentries of one entry
                label += f" {sub[-3:]}"
        if args.x in PRODUCT_AXES and (pts[0].get("product_state") or "") not in ("", "G"):
            label += f" isomer {pts[0]['product_state']}"
        if "+" in key[1]:                            # a plot of merged products: say the product of the series
            label += f" [{pts[0].get('product_label')}]"
        if mode:                                   # one legend entry per dataset, not per angle or energy
            if entry in legend_done:
                label = "_nolegend_"
            else:
                legend_done.add(entry)
        hollow = curve or args.hollow
        ax.errorbar(xs, ys, yerr=yerr if (any(yerr) and not (args.no_yerr or args.no_errorbars)) else None,
                    xerr=xerr if xerr and any(xerr) else None,
                    fmt=marker, ms=args.ms, lw=0.7, capsize=1.5 if args.ms >= 3 else 0.8, color=color, label=label,
                    mfc="none" if hollow else color, mew=0.9 if hollow else 1.0, alpha=args.alpha,
                    zorder=zmap[(entry, sub, branch, grp)])
        if mode and draw_labels and grp is not None:    # keep the series with most points for the label of this value
            il = len(xs) - 1                       # its last point (the points are sorted by x)
            if grp not in peaks or len(pts) > peaks[grp][0]:
                peaks[grp] = (len(pts), xs[il], ys[il], color, (xerr[il] if xerr else 0.0))
        n += 1
    if mode and draw_labels and not peaks:
        print(f"  note: no {mode} labels in '{panel_title(key, rows, target, args)}': its points have no "
              f"{'angle' if mode == 'angle' else 'incident energy'} value", file=sys.stderr)
    elif mode and draw_labels and len(peaks) >= 3 and args.stack <= 1 and not single_hint[0]:
        single_hint[0] = True
        print(f"  note: {len(peaks)} labelled distributions without --stack may overlap; on a logarithmic y axis "
              f"--stack 10 separates them", file=sys.stderr)
    if args.x == "E":
        n += draw_endf(ax, key, rows, key[5] or unit, args, axes)
    ax.set_title(panel_title(key, rows, target, args), fontsize=9)
    ax.set_xlabel(args.xlabel or x_label(args.x, rows), fontsize=8)
    ax.set_ylabel(args.ylabel or y_label(key[2], key[5] or unit, [args.x], rows), fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.3)
    if axes["logx"]:
        ax.set_xscale("log")
    if axes["logy"]:
        ax.set_yscale("log")
    elif not axes["ylim"] and not args.no_zero:
        ax.set_ylim(bottom=0)
    if not axes["logx"] and not axes["xlim"] and args.x in ("E", "Eout"):
        left, right = ax.get_xlim()
        if left < 0:
            ax.set_xlim(0, right)               # no negative energies because of the error bars
    if axes["xlim"]:
        ax.set_xlim(*axes["xlim"])
    if axes["ylim"]:
        ax.set_ylim(*axes["ylim"])
    if mode and draw_labels and peaks:
        place_end_labels(ax, peaks, mode, args, axes)
    elif mode and args.stack > 1 and not draw_labels:
        # scaled distributions without labels: say in the plot how they were scaled
        what = "angle" if mode == "angle" else "incident energy"
        ax.text(0.01, 0.01, f"distributions multiplied by {args.stack:g}$^i$, i = 0, 1, 2 ... in order of increasing "
                f"{what}", transform=ax.transAxes, ha="left", va="bottom", fontsize=6.5, color="0.25", zorder=7,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.7", lw=0.5, alpha=0.8))
        if not single_hint[0]:
            single_hint[0] = True
            print(f"  note: --stack multiplies the distributions by {args.stack:g}, {args.stack:g}^2 ... and without "
                  f"--{'angle' if mode == 'angle' else 'energy'}-labels the factors are not written on labels; the plot "
                  f"carries a note instead", file=sys.stderr)
    if axes.get("note"):
        ax.text(0.99, 0.01, axes["note"], transform=ax.transAxes, ha="right", va="bottom", fontsize=6, color="0.4")
    for v in args.vline or []:
        ax.axvline(v, color="k", ls="--", lw=0.8)
    if (args.legend == "panel" or (single and args.legend == "figure")) and n:
        if n <= args.max_legend:
            ax.legend(fontsize=6.5 if not single else 7, loc="best", framealpha=0.8)
        elif single:
            # no room inside the plot: labels in columns on the right, next to the axes
            ncol = math.ceil(n / 24)
            ax.legend(fontsize=6, loc="upper left", bbox_to_anchor=(1.01, 1.0), ncol=ncol, frameon=False,
                      borderaxespad=0, columnspacing=1.0, handletextpad=0.3)
        else:
            print(f"  note: legend omitted in panel '{panel_title(key, rows, target, args)}' ({n} series, more than "
                  f"--max-legend {args.max_legend}); select entries with --entries or --exclude-entries.",
                  file=sys.stderr)
    return n


AXIS_NAMES = {"E": "Incident energy (MeV)", "Eout": "Outgoing energy (MeV)", "angle": "Angle (deg)",
              "A": "Mass number A of the product", "Z": "Atomic number Z of the product",
              "N": "Neutron number N of the product"}
PRODUCT_AXES = ("A", "Z", "N")
THIRD_LABEL = {"E": "E = {} MeV", "Eout": "E_out = {} MeV", "angle": "angle = {} deg"}


def axis_value(r, name):
    return {"E": r.get("E_MeV"), "Eout": r.get("E_out_MeV"), "angle": r.get("angle_deg"),
            "A": r.get("product_A"), "Z": r.get("product_Z"), "N": product_N(r)}[name]


def parse_axes(text):
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 2 or any(p not in AXIS_NAMES for p in parts) or parts[0] == parts[1]:
        raise argparse.ArgumentTypeError("two different variables among E, Eout and angle, e.g. Eout,angle")
    return parts


def axis_is_log(values, name, force_log, force_lin):
    """Logarithmic scale for an energy axis whose bulk spans a factor of 50 or more (or when forced)."""
    if name == "angle" or name in PRODUCT_AXES or force_lin:
        return False
    if force_log:
        return True
    pos = sorted(v for v in values if v > 0)
    return len(pos) >= 5 and len(pos) >= 0.95 * len(values) and quantile(pos, 0.95) / quantile(pos, 0.05) >= 50


def axis_bins(values, log, nbins, name):
    """Cell edges and centres of one axis. A variable with at most nbins distinct values (angles, a few
    incident energies) gets one cell per value; otherwise nbins equal cells (equal in log for a log axis)."""
    import numpy as np
    v = np.array(values, float)
    if name in PRODUCT_AXES:                  # integer variable: one cell per integer, empty cells stay empty
        lo, hi = int(round(v.min())), int(round(v.max()))
        return np.arange(lo - 0.5, hi + 1.5), np.arange(lo, hi + 1, dtype=float)
    uniq = np.unique([float(sig3(x)) for x in v])
    if len(uniq) <= nbins:
        if len(uniq) == 1:
            half = 0.5 * abs(uniq[0]) if uniq[0] else 0.5
            edges = np.array([uniq[0] - half, uniq[0] + half]) if not log else np.array([uniq[0] / 1.5, uniq[0] * 1.5])
        elif log:
            m = np.sqrt(uniq[1:] * uniq[:-1])
            edges = np.concatenate([[uniq[0] ** 2 / m[0]], m, [uniq[-1] ** 2 / m[-1]]])
        else:
            m = (uniq[1:] + uniq[:-1]) / 2.0
            edges = np.concatenate([[2 * uniq[0] - m[0]], m, [2 * uniq[-1] - m[-1]]])
        if name == "angle":
            edges[0] = max(edges[0], min(uniq[0], 0.0))
        centers = uniq
    else:
        lo, hi = float(v.min()), float(v.max())
        if log:
            edges = np.logspace(math.log10(lo), math.log10(hi), nbins + 1)
            centers = np.sqrt(edges[1:] * edges[:-1])
        else:
            edges = np.linspace(lo, hi, nbins + 1)
            centers = (edges[1:] + edges[:-1]) / 2.0
    return edges, centers


def make_grid_plots(rows, args, root, prefix_of, formats, plt, kind, list_only=False):
    """2D maps (kind 'map') or 3D plots (kind '3d') of the data on two of the variables E (incident energy),
    Eout (outgoing energy) and angle; the colour or the height is the value. One plot per dataset and per value
    of the third variable."""
    import numpy as np
    from matplotlib.colors import LogNorm, Normalize
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    ax_names = args.axes
    third = [v for v in ("E", "Eout", "angle") if v not in ax_names][0]
    groups = collections.OrderedDict()
    skipped = 0
    for r in rows:
        vx, vy = axis_value(r, ax_names[0]), axis_value(r, ax_names[1])
        if vx is None or vy is None or r.get("value") is None:
            skipped += 1
            continue
        tv = axis_value(r, third)
        tb = sig3(tv) if tv is not None else ""
        unit = r.get("value_unit") or ""
        if any(a in PRODUCT_AXES for a in ax_names):      # the products are the axis: one map for each entry and branch
            st_ = r.get("product_state") or ""
            prod_, sub_ = "fragments", f"{r.get('branch') or '-'}|{r.get('process') or ''}|" + ("" if st_ in ("", "G") else st_)
        else:
            prod_, sub_ = r.get("product_label", ""), r["subentry"]
        groups.setdefault((r.get("target", ""), r.get("projectile", ""), prod_,
                           r.get("quantity", ""), unit, r["entry"], sub_, tb), []).append(r)
    if skipped:
        print(f"  note: {skipped} points lack {ax_names[0]}, {ax_names[1]} or a value and cannot go into the "
              f"{'map' if kind == 'map' else '3D plot'}", file=sys.stderr)
    todo = []
    for key, pts in groups.items():
        nx = len({sig3(axis_value(p, ax_names[0])) for p in pts})
        ny = len({sig3(axis_value(p, ax_names[1])) for p in pts})
        if nx < 2 or ny < 2 or (nx * ny < 6):
            print(f"  note: no {kind} plot for {target_dirname(key[0])} {key[1]}->{key[2]} {key[3]} {key[5]} "
                  f"{key[6][-3:]} {THIRD_LABEL[third].format(key[7]) if key[7] else ''}: needs at least 2 distinct "
                  f"{ax_names[0]} and 2 distinct {ax_names[1]} values", file=sys.stderr)
            continue
        todo.append((key, pts))
    if list_only:                                           # --list: say what would be drawn, draw nothing
        tag = "map" if kind == "map" else f"3d-{args.style}"
        print(f"\n{len(todo)} {'maps' if kind == 'map' else '3D plots'} from {len({k[5] for k, _ in todo})} EXFOR "
              f"entries would be written" + (f" (above the limit --max-plots {args.max_plots}: restrict the selection "
                                             f"or raise it)" if len(todo) > args.max_plots else "") + ":")
        print(f"{'entry':8} {'branch':8} {THIRD_LABEL[third].split(' =')[0]:>8} {'points':>7} "
              f"{ax_names[0] + ' x ' + ax_names[1] + ' values':>20}   file")
        for key, pts in todo:
            tcode, proj, prod, qty, unit, entry, sub, tb = key
            prod_axes = any(a in PRODUCT_AXES for a in ax_names)
            branch_txt = (pts[0].get("branch") or "") if prod_axes else ""
            iso_txt = sub.split("|")[2] if (prod_axes and sub.count("|") >= 2) else ""
            nx = len({sig3(axis_value(p_, ax_names[0])) for p_ in pts})
            ny = len({sig3(axis_value(p_, ax_names[1])) for p_ in pts})
            stem = (f"{prefix_of(tcode)}_{safe(proj)}_{safe(prod)}_{safe(qty)}" + (f"_{safe(unit)}" if unit else "")
                    + f"_{tag}_{ax_names[0]}-{ax_names[1]}" + (f"_{third}{safe(tb)}" if tb else "")
                    + (f"_{safe(branch_txt)}" if branch_txt else "") + (f"_isomer-{iso_txt}" if iso_txt else "")
                    + f"_{entry}" + ("" if prod_axes else sub[-3:]))
            print(f"{entry:8} {(branch_txt + (' ' + iso_txt if iso_txt else '')) or '-':8} {tb or '-':>8} {len(pts):7d} {f'{nx} x {ny}':>20}   "
                  f"{root / target_dirname(tcode) / (stem + '.' + (formats[0] if formats else 'png'))}")
        return []
    if len(todo) > args.max_plots:
        sys.exit(f"{len(todo)} plots would be written (limit --max-plots {args.max_plots}). Restrict the selection "
                 f"(--at-energy, --at-angle, --entries, --product, --branch, --unit) or raise --max-plots; "
                 f"--list shows all of them.")
    written = []
    for key, pts in todo:
        tcode, proj, prod, qty, unit, entry, sub, tb = key
        vx = [axis_value(p, ax_names[0]) for p in pts]
        vy = [axis_value(p, ax_names[1]) for p in pts]
        logs = [axis_is_log(vx, ax_names[0], args.logx, args.linx), axis_is_log(vy, ax_names[1], args.logy, args.liny)]
        ex, cx = axis_bins(vx, logs[0], args.ebins, ax_names[0])
        ey, cy = axis_bins(vy, logs[1], args.ebins, ax_names[1])
        ssum = np.zeros((len(cy), len(cx)))
        cnt = np.zeros((len(cy), len(cx)))
        for p, x, y in zip(pts, vx, vy):
            ix = min(max(int(np.searchsorted(ex, x, side="right")) - 1, 0), len(cx) - 1)
            iy = min(max(int(np.searchsorted(ey, y, side="right")) - 1, 0), len(cy) - 1)
            ssum[iy, ix] += p["value"]
            cnt[iy, ix] += 1
        z = np.where(cnt > 0, ssum / np.maximum(cnt, 1), np.nan)
        zpos = z[np.isfinite(z) & (z > 0)]
        if zpos.size == 0:
            continue
        use_log = args.logz or (not args.linz and zpos.max() / zpos.min() >= 100)
        if use_log:
            z = np.where(z > 0, z, np.nan)
        vmin, vmax = args.zlim if args.zlim else ((float(zpos.min()), float(zpos.max())) if use_log else
                                                  (min(0.0, float(np.nanmin(z))), float(np.nanmax(z))))
        norm = LogNorm(vmin=vmin, vmax=vmax) if use_log else Normalize(vmin=vmin, vmax=vmax)
        zlabel = args.ylabel or y_label(qty, unit, ax_names, pts)
        pk = (proj, prod, qty, "", tcode, unit, "", "")
        prod_axes = any(a in PRODUCT_AXES for a in ax_names)
        subs = sorted({str(p["subentry"])[-3:] for p in pts})
        sub_txt = subs[0] if len(subs) == 1 else "several subentries"
        branch_txt = (pts[0].get("branch") or "") if prod_axes else ""
        iso_txt = sub.split("|")[2] if (prod_axes and sub.count("|") >= 2) else ""
        title = panel_title(pk, pts, tcode, hl_args=args) + (("  " + THIRD_LABEL[third].format(tb)) if tb else "")
        title += (f"  {branch_txt}" if branch_txt else "") + (f"  isomers {iso_txt}" if iso_txt else "")
        title += f"\n{series_label(pts[0])} [{entry} {sub_txt}]"
        if kind == "map":
            fig, ax = plt.subplots(figsize=(7.4, 5.0))
            mesh = ax.pcolormesh(ex, ey, np.ma.masked_invalid(z), norm=norm, cmap=args.cmap, shading="flat")
            cb = fig.colorbar(mesh, ax=ax, pad=0.02)
            cb.set_label(zlabel, fontsize=8)
            cb.ax.tick_params(labelsize=7)
            if logs[0]:
                ax.set_xscale("log")
            if logs[1]:
                ax.set_yscale("log")
            ax.set_xlabel(axis_label(ax_names[0], pts), fontsize=8)
            ax.set_ylabel(axis_label(ax_names[1], pts), fontsize=8)
            ax.tick_params(labelsize=7)
            ax.set_title(title, fontsize=8)
            tag = "map"
        else:
            from matplotlib.cm import ScalarMappable
            fig = plt.figure(figsize=(8.2, 6.2))
            ax = fig.add_subplot(projection="3d")
            tr = [(np.log10 if lg else (lambda a: a)) for lg in logs]
            tz = (lambda a: np.log10(a)) if use_log else (lambda a: a)
            X, Y = np.meshgrid(tr[0](cx), tr[1](cy))
            ok = np.isfinite(z)
            cmap = plt.get_cmap(args.cmap)
            znorm = Normalize(vmin=tz(vmin), vmax=tz(vmax))
            if args.style == "scatter":
                xs = tr[0](np.array([v for v, p in zip(vx, pts) if p["value"] > 0 or not use_log]))
                ys = tr[1](np.array([v for v, p in zip(vy, pts) if p["value"] > 0 or not use_log]))
                zs = tz(np.array([p["value"] for p in pts if p["value"] > 0 or not use_log]))
                ax.scatter(xs, ys, zs, c=zs, cmap=cmap, norm=znorm, s=8, depthshade=True)
            elif args.style == "bars":
                dx = np.diff(tr[0](ex)) * 0.9
                dy = np.diff(tr[1](ey)) * 0.9
                x0 = (tr[0](ex)[:-1])[None, :].repeat(len(cy), 0)[ok]
                y0 = (tr[1](ey)[:-1])[:, None].repeat(len(cx), 1)[ok]
                ddx = dx[None, :].repeat(len(cy), 0)[ok]
                ddy = dy[:, None].repeat(len(cx), 1)[ok]
                zt = tz(z[ok])
                base = znorm.vmin if use_log else 0.0
                ax.bar3d(x0, y0, np.full_like(zt, base), ddx, ddy, zt - base, color=cmap(znorm(zt)), shade=True)
            else:
                zt = np.where(ok, tz(np.where(ok, z, 1.0)), np.nan)
                try:                                              # regular grid; empty cells stay empty
                    ax.plot_surface(X, Y, zt, cmap=cmap, norm=znorm, linewidth=0.2, edgecolor="0.3",
                                    antialiased=True, rstride=1, cstride=1)
                except Exception:
                    ax.scatter(X[ok], Y[ok], tz(z[ok]), c=tz(z[ok]), cmap=cmap, norm=znorm, s=10)
            fmt = FuncFormatter(lambda v, _: f"$10^{{{v:g}}}$")
            for axis, lg in zip((ax.xaxis, ax.yaxis), logs):
                if lg:
                    axis.set_major_formatter(fmt)
                    axis.set_major_locator(MaxNLocator(integer=True))
            if use_log:
                ax.zaxis.set_major_formatter(fmt)
                ax.zaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_xlabel(axis_label(ax_names[0], pts), fontsize=8, labelpad=4)
            ax.set_ylabel(axis_label(ax_names[1], pts), fontsize=8, labelpad=4)
            ax.set_zlabel(zlabel, fontsize=8, labelpad=4)
            ax.tick_params(labelsize=6)
            ax.view_init(elev=args.elev, azim=args.azim)
            cb = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.6, pad=0.1)
            cb.set_label(zlabel, fontsize=7)
            cb.ax.tick_params(labelsize=6)
            ax.set_title(title, fontsize=8)
            tag = f"3d-{args.style}"
        tdir = root / target_dirname(tcode)
        tdir.mkdir(parents=True, exist_ok=True)
        stem = (f"{prefix_of(tcode)}_{safe(proj)}_{safe(prod)}_{safe(qty)}" + (f"_{safe(unit)}" if unit else "")
                + f"_{tag}_{ax_names[0]}-{ax_names[1]}" + (f"_{third}{safe(tb)}" if tb else "")
                + (f"_{safe(branch_txt)}" if branch_txt else "") + (f"_isomer-{iso_txt}" if iso_txt else "")
                + f"_{entry}" + ("" if prod_axes else sub[-3:]))
        for fmt_ in formats:
            fn = f"{stem}.{fmt_}"
            fig.savefig(tdir / fn, dpi=args.dpi, bbox_inches="tight")
            written.append(f"{target_dirname(tcode)}/{fn}")
        if args.show:
            plt.show()
        plt.close(fig)
    return written


def parse_pair(text):
    try:
        a, b = text.split(",")
        return float(a), float(b)
    except ValueError:
        raise argparse.ArgumentTypeError("expected two numbers separated by a comma, e.g. 0,50")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Plot EXFOR data selected with exfor_retrieve.py (excitation functions with error bars).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python exfor_plot.py --target Nb-93 --projectiles d --product 92mNb,89Zr,90Nb\n"
               "  python exfor_plot.py --data EXFOR_NB-93_data.csv --product \"Zr-*\" --logy\n"
               "  python exfor_plot.py --target Cu-nat --projectiles d --product Zn-65,Zn-63 --vline 40 --format png,pdf")
    src = ap.add_argument_group("data source (one of the two)")
    src.add_argument("--target", help="retrieve and plot in one step, e.g. Nb-93, Ti-nat (needs the EXFOR master files)")
    src.add_argument("--data", nargs="+",
                     help="CSV file(s) written by exfor_retrieve.py, or a folder such as data/Nb-93 (wildcards allowed). "
                          "A path that does not exist yet is retrieved first (the target is taken from its name)")
    sel = ap.add_argument_group("selection (same syntax as exfor_retrieve.py)")
    sel.add_argument("--projectiles", default=None,
                     help="'all' or a subset. Default: d,p,he3,a with --target (as in exfor_retrieve.py); "
                          "all with --data (everything in the file)")
    sel.add_argument("--product", "--products", dest="product", default="all", help="final product(s), default all; also heavy (every nuclide with Z>=3) and residual (heavy products except the target itself)")
    sel.add_argument("--product-exact", action="store_true")
    sel.add_argument("--facility", default=None,
                     help="with --target: only the entries measured at a facility: ntof (n_TOF at CERN), gelina or a regular "
                          "expression searched in the FACILITY and INSTITUTE fields. Several targets: retrieve with "
                          "exfor_retrieve.py --facility ntof and plot each folder with --data.")
    sel.add_argument("--quantity", default="SIG", help="EXFOR quantity code(s), default SIG (cross sections)")
    sel.add_argument("--emin", type=float, default=None, help="minimum incident energy (MeV)")
    sel.add_argument("--emax", type=float, default=None, help="maximum incident energy (MeV)")
    sel.add_argument("--entries", default="", help="keep only these EXFOR entries, e.g. D4344,D4156, or subentries, e.g. C3057016")
    sel.add_argument("--process", default="", help="keep only these reaction types, e.g. F (fission), 2N, TOT, X")
    sel.add_argument("--branch", default="",
                     help="keep only these EXFOR branch codes, for example DL (delayed), PR (prompt), CUM, IND; "
                          "a code matches the parts of the branch, so DL also selects DL/GRP; a leading - excludes; "
                          "none selects data without a branch")
    sel.add_argument("--by-process", action="store_true",
                     help="one panel per reaction type (done automatically for reactions without a product)")
    sel.add_argument("--exclude-entries", default="", help="drop these EXFOR entries or subentries")
    sel.add_argument("--exclude-status", default="", help="drop datasets with these status codes, e.g. SPSDD (superseded). Not applied by default. Do not drop DEP as a rule")
    sel.add_argument("--include-complex", action="store_true", help="also plot complex reactions (ratios, sums)")
    sel.add_argument("--merge-products", action="store_true",
                     help="draw the selected products of a target and projectile in one plot, not one plot for each "
                          "product; the quantities that have the same unit are merged too, and the legend gives the "
                          "product of each series. For example the neutron production and the reaction to a residual "
                          "nucleus, whose yields are in the same unit")
    sel.add_argument("--unit", default=None, help="unit to plot (default mb for SIG, else the most frequent)")
    sel.add_argument("--no-convert-units", action="store_true",
                     help="do not convert cross sections given as sigma*E or sigma*sqrt(E) (B*EV, B*KEV, B*MEV, "
                          "MB*MEV, B*RT-EV) to mb; such points are then dropped")
    sel.add_argument("--x", choices=["E", "angle", "Eout", "A", "Z", "N"], default="E",
                     help="x variable: incident energy (default), angle, outgoing energy, or the mass number A, "
                          "atomic number Z or neutron number N of the product (fission yields)")
    sel.add_argument("--at-energy", type=float, default=None, help="keep points whose incident energy is near this (MeV)")
    sel.add_argument("--tol", type=float, default=0.5, help="tolerance for --at-energy in MeV (default 0.5)")
    sel.add_argument("--at-angle", type=float, default=None,
                     help="keep points measured at this angle (degrees), for angular and double-differential data")
    sel.add_argument("--angle-tol", type=float, default=5.0, help="tolerance for --at-angle in degrees (default 5)")
    sel.add_argument("--by-energy", action="store_true",
                     help="one plot per incident energy (energies rounded to 3 significant figures)")
    sel.add_argument("--by-angle", action="store_true", help="one plot per angle (rounded to 0.1 degree)")
    sel.add_argument("--angle-labels", action="store_true",
                     help="draw all angles in one plot, each distribution labelled with its angle in a column at "
                          "the right of the data (for spectra, --x Eout)")
    sel.add_argument("--energy-labels", action="store_true",
                     help="draw all incident energies in one plot, each distribution labelled with its energy in a "
                          "column at the right of the data (for angular distributions, --x angle)")
    sel.add_argument("--stack", type=float, default=1.0,
                     help="draw all angles (--x Eout) or all incident energies (--x angle) in one plot and multiply "
                          "the distributions by F, F^2, F^3 ... in order of increasing angle or energy (for example "
                          "10) so that they do not overlap on a logarithmic y axis. The labels are drawn only with "
                          "--angle-labels or --energy-labels, which write the factors; without them a note in the "
                          "plot gives the rule")
    sel.add_argument("--map2d", action="store_true",
                     help="2D maps instead of curves: the value as colour over two variables (--axes, default "
                          "outgoing energy against angle), one map per dataset and value of the third variable")
    sel.add_argument("--plot3d", action="store_true",
                     help="3D plots instead of curves: the value as height and colour over two variables "
                          "(--axes), one plot per dataset and value of the third variable")
    sel.add_argument("--axes", type=parse_axes, default=["Eout", "angle"],
                     help="the two variables of --map2d and --plot3d, among E (incident energy), Eout (outgoing "
                          "energy) and angle, for example Eout,angle (default) or E,Eout")
    sel.add_argument("--style", choices=["surface", "bars", "scatter"], default="surface",
                     help="with --plot3d: surface (default), bars (3D histogram) or scatter (the points)")
    sel.add_argument("--elev", type=float, default=25.0, help="with --plot3d: elevation of the view (default 25)")
    sel.add_argument("--azim", type=float, default=-60.0, help="with --plot3d: azimuth of the view (default -60)")
    sel.add_argument("--ebins", type=int, default=40,
                     help="with --map2d and --plot3d: a variable with more distinct values than this is put in this "
                          "many bins (default 40); with fewer values each value has its own cell")
    sel.add_argument("--logz", action="store_true", help="with --map2d/--plot3d: logarithmic colour or height scale")
    sel.add_argument("--linz", action="store_true", help="with --map2d/--plot3d: linear scale (default: logarithmic "
                                                       "when the values span two decades or more)")
    sel.add_argument("--zlim", type=parse_pair, default=None, help="with --map2d/--plot3d: value range, e.g. 1e-3,10")
    sel.add_argument("--cmap", default="viridis", help="with --map2d/--plot3d: matplotlib colour map (default viridis)")
    sel.add_argument("--ascii", action="store_true",
                     help="also write each plotted dataset as its own ASCII file in columns, with the units in the "
                          "first row (2D distributions: one file with three columns), in <data-dir>/<target>/ascii/")
    sel.add_argument("--ascii-format", choices=["dataset", "entry", "quantity"], default="dataset",
                     help="with --ascii: 'dataset' (default) one file per dataset; 'entry' one file per EXFOR entry, "
                          "quantity and unit; 'quantity' one file per projectile, process, quantity and unit "
                          "(far fewer files, with columns that tell the datasets apart)")
    sel.add_argument("--ascii-no-blanks", action="store_true",
                     help="with --ascii: no blank line between the blocks of a 2D file (default: a blank line)")
    sel.add_argument("--halflife", action="store_true",
                     help="print the NUBASE2020 half-life in parentheses next to the isotope name (the product, and "
                          "the target when it is radioactive) in the titles of the plots, and in the files written "
                          "by the same command. Off by default; --halflife-db also switches it on")
    sel.add_argument("--halflife-db", default=None,
                     help="SQLite database of NUBASE2020 half-lives (see exfor_retrieve.py --help); giving it also "
                          "switches --halflife on")
    sel.add_argument("--ascii-dir", default=None, help="folder for the ASCII files (default <data-dir>/<target>/ascii)")
    sel.add_argument("--ascii-no-errors", action="store_true",
                     help="with --ascii: leave out the uncertainty columns (the files have them by default, also the "
                          "2D files, when the dataset gives them)")
    sel.add_argument("--ascii-errors", action="store_true", help=argparse.SUPPRESS)       # kept: now the default
    sel.add_argument("--max-ascii", type=int, default=5000, help="maximum number of ASCII files (default 5000)")
    sel.add_argument("--references", action="store_true",
                     help="also write the list of references of the plotted datasets, one file set per target, "
                          "next to the plots (<target>_references.txt, .bib, .csv; see --ref-format)")
    sel.add_argument("--ref-format", default="txt,bib", help="formats of the reference list: txt, bib, csv "
                                                            "(comma list, default txt,bib)")
    sel.add_argument("--ref-authors", type=int, default=3,
                     help="authors written in a reference: all if there are at most this many, otherwise the first "
                          "one and 'et al.' (default 3; 0 = always all)")
    sel.add_argument("--max-plots", type=int, default=200,
                     help="stop instead of writing more than this many plots (default 200)")
    sel.add_argument("--data-dir", default="data",
                     help="retrieve mode: the retrieved data are saved in <data-dir>/<target name>/ (default ./data)")
    sel.add_argument("--data-prefix", default=None,
                     help="retrieve mode: prefix of the saved data files (default EXFOR_<target>, as in exfor_retrieve.py)")
    sel.add_argument("--no-save-data", action="store_true", help="retrieve mode: do not save the retrieved data")
    sel.add_argument("--master", default=None,
                     help="EXFOR master files (retrieve mode); default as in exfor_retrieve.py (MASTER_DEFAULT, "
                          "else ./exfor_master)")
    sel.add_argument("--update", action="store_true", help="git pull the master files first (retrieve mode)")
    sel.add_argument("--jobs", type=int, default=min(8, os.cpu_count() or 1))
    ev = ap.add_argument_group("evaluated data (ENDF files)")
    ev.add_argument("--endf", nargs="+", default=None, metavar="FILE",
                    help="draw the cross sections of evaluated files in ENDF-6 format over the EXFOR data (neutron-induced "
                         "SIG plots): files, wildcards or folders; several give several lines. See the header of "
                         "exfor_plot.py or the README")
    ev.add_argument("--endf-label", nargs="+", default=None, metavar="TEXT",
                    help="legend text of each --endf file, in the order of the files (default: the library and version "
                         "that the file states, e.g. ENDF/B-VIII.0)")
    ev.add_argument("--endf-full", action="store_true",
                    help="draw File 3 over the whole energy range of the file, also where the cross section is stored as "
                         "resonance parameters (then File 3 is only the background); default: the energy range of the data, "
                         "starting above the resonance ranges of files with resonance parameters")
    ev.add_argument("--endf-lw", type=float, default=1.4, help="line width of the ENDF lines (default 1.4)")
    ev.add_argument("--endf-sub", type=int, default=12,
                    help="points inserted in each interval that is not linear-linear, so that straight lines follow the "
                         "evaluation on any axes (default 12; 0 = none)")
    lay = ap.add_argument_group("layout and output")
    lay.add_argument("--auto-axes", action="store_true",
                     help="choose linear or logarithmic axes and the limits for each panel from the data")
    lay.add_argument("--linx", action="store_true", help="force a linear x axis (with --auto-axes)")
    lay.add_argument("--liny", action="store_true", help="force a linear y axis (with --auto-axes)")
    lay.add_argument("--logx", action="store_true", help="logarithmic x axis")
    lay.add_argument("--logy", action="store_true", help="logarithmic y axis (default: linear, starting at zero)")
    lay.add_argument("--no-zero", action="store_true", help="do not force the linear y axis to start at 0")
    lay.add_argument("--xlim", type=parse_pair, help="x limits, e.g. 0,50")
    lay.add_argument("--ylim", type=parse_pair, help="y limits, e.g. 0,300")
    lay.add_argument("--vline", type=float, nargs="*", help="vertical dashed line(s) at these x values, e.g. 40")
    lay.add_argument("--sharex", action="store_true", help="with --combine: same x axis in all panels")
    lay.add_argument("--sharey", action="store_true", help="with --combine: same y axis in all panels")
    lay.add_argument("--combine", action="store_true",
                     help="put several panels in one figure instead of one file per plot")
    lay.add_argument("--cols", type=int, default=3, help="with --combine: panels per row (default 3)")
    lay.add_argument("--max-panels", type=int, default=9, help="with --combine: panels per figure (default 9)")
    lay.add_argument("--separate", action="store_true", help="one file per plot (this is now the default)")
    lay.add_argument("--legend", choices=["panel", "figure", "none"], default="panel",
                     help="legend in each panel (default), one per figure, or none")
    lay.add_argument("--max-legend", type=int, default=12,
                     help="legend inside the plot up to this many series; with more, the labels are written "
                          "to the right of the plot in columns (default 12)")
    lay.add_argument("--no-xerr", action="store_true", help="do not draw energy error bars")
    lay.add_argument("--xlabel", default=None, help="text of the x axis label (default: made from the data)")
    lay.add_argument("--ylabel", default=None, help="text of the y axis label (default: quantity and unit from the data)")
    lay.add_argument("--no-yerr", action="store_true", help="do not draw the vertical error bars (the values' uncertainties)")
    lay.add_argument("--no-errorbars", action="store_true", help="do not draw any error bars")
    lay.add_argument("--ms", type=float, default=4.0, help="marker size (default 4; use 1-2 for many points)")
    lay.add_argument("--alpha", type=float, default=0.9,
                     help="transparency of markers and error bars, 0 to 1 (default 0.9; 0.3-0.5 shows overlapping points)")
    lay.add_argument("--hollow", action="store_true", help="open markers (only the edge), so that points behind show")
    lay.add_argument("--title", default=None, help="figure title (replaces the automatic title)")
    lay.add_argument("--format", default="png", help="png (default), pdf, svg or a comma list, e.g. png,pdf")
    lay.add_argument("--dpi", type=int, default=150)
    lay.add_argument("--out", default="plots",
                     help="parent folder: the plots of each target go to <out>/<target>/ (default: ./plots)")
    lay.add_argument("--prefix", default=None, help="file name prefix (default: the target name, e.g. Nb-93)")
    lay.add_argument("--list", action="store_true", help="list the plots (with file names) and exit")
    lay.add_argument("--show", action="store_true", help="also open the figure window")
    ap.add_argument("--version", action="version", version=f"exfor_plot {__version__} (build {__build__})")
    args = ap.parse_args(argv)
    args.master = args.master or X.default_master()
    args.endf_lib = None
    if args.endf:
        if ER is None:
            ap.error("--endf needs endf_reader.py in the same folder as exfor_plot.py")
        args.endf_lib = EndfLibrary(args.endf, args.endf_label)
    elif args.endf_label:
        ap.error("--endf-label needs --endf")

    if bool(args.target) == bool(args.data):
        ap.error("give either --target (retrieve and plot) or --data (CSV files from exfor_retrieve.py)")
    projectiles_given = args.projectiles is not None
    if args.projectiles is None:
        args.projectiles = "d,p,he3,a" if args.target else "all"
    if group_mode(args) == "angle":
        args.by_angle = False                       # all angles go into one plot, each with its label
    elif group_mode(args) == "energy":
        args.by_energy = False
    try:
        X.Selection(args.projectiles)
        X.ProductSelection(args.product, exact=args.product_exact)
        target_code = X.parse_target(args.target) if args.target else None
    except ValueError as exc:
        ap.error(str(exc))

    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    try:
        ref_formats = X.parse_ref_formats(args.ref_format)
    except ValueError as exc:
        ap.error(str(exc))
    meta = {}
    if args.target:
        rows, datasets = retrieve_rows(args)
        meta = {d["entry"]: d for d in datasets}
        if not args.no_save_data:
            save_retrieved(rows, datasets, args, target_code)
    else:
        existing, missing = classify_data_args(args.data)
        rows = read_csv_files(existing) if existing else []
        if existing:                                # titles, references and the ASCII index use the datasets file
            meta = read_dataset_meta(existing)
        for path in missing:                       # data not retrieved yet: retrieve them now
            tcode = target_from_path(path)
            if tcode is None:
                sys.exit(no_data_message(path, os.path.isdir(path)))
            proj = args.projectiles if projectiles_given else "d,p,he3,a"
            print(f"No data found at '{path}': retrieving {target_dirname(tcode)} from the EXFOR master files "
                  f"(projectiles {proj}, product {args.product}, quantity {args.quantity})"
                  + ("" if projectiles_given else "; --projectiles was not given, so the default d,p,he3,a is used"
                                                  " (add --projectiles all for everything)") + ".", file=sys.stderr)
            new_rows, new_datasets = retrieve_rows(args, tcode, proj)
            for d_ in new_datasets:
                meta.setdefault(d_["entry"], d_)
            if not args.no_save_data:
                folder, prefix = save_location(path)
                save_retrieved(new_rows, new_datasets, args, tcode, folder, prefix)
            rows += new_rows
    log = collections.Counter()
    rows = apply_filters(rows, args, log)
    if not rows:
        print("No data left after the selection. Check --projectiles, --product, --quantity and the energy limits."
              + (" If the saved data were retrieved with a narrower selection, retrieve them again with "
                 "exfor_retrieve.py (or delete the folder: it is retrieved again with this selection)."
                 if args.data else ""), file=sys.stderr)
        return 1
    if args.process:                       # tell the user when a requested reaction type has no data
        found = {(r.get("process") or "").upper() for r in rows}
        for p in [x.strip().upper() for x in args.process.split(",") if x.strip()]:
            if p not in found:
                hint = ""
                if args.product.strip().lower() not in ("all", "any", "*"):
                    hint = (f" Product selection is '{args.product}': most reactions (for example capture, (n,g)) "
                            f"lead to a product, which '--product none' leaves out. Add the product, for example "
                            f"--product none,U-239, or use --product all.")
                print(f"  note: no data for reaction type {p} with this selection.{hint}", file=sys.stderr)
    if not args.no_convert_units:
        convert_weighted(rows, log)
        for k in sorted(k for k in log if k.startswith("weighted_")):
            what = k[len("weighted_"):]
            how = "sigma x sqrt(E)" if what == "B*RT-EV" else "sigma x E"
            print(f"  note: {log[k]} points given as {how} (unit {what}) were converted to cross sections in mb "
                  f"(--no-convert-units plots only the points already in mb)", file=sys.stderr)
    rows, unit_of = choose_units(rows, args, log)
    # points without the plotted coordinate
    usable = [r for r in rows if x_value(r, args.x) is not None and r.get("value") is not None]
    log["no_x"] = len(rows) - len(usable)
    rows = usable
    if not rows:
        print(f"No point has the coordinate '{args.x}' (for angular distributions or spectra use --x angle or "
              f"--x Eout, with --at-energy).", file=sys.stderr)
        return 1
    args_unit[0] = args.unit
    panels = build_panels(rows, args)
    if args.ascii and not args.list:
        write_plot_ascii(rows, args)
    styles = assign_styles(rows)
    formats = [f.strip().lower().lstrip(".") for f in args.format.split(",") if f.strip()]
    root = Path(args.out)

    def prefix_of(tcode):
        return args.prefix or target_dirname(tcode)

    def label_of(key):
        return (f"{target_dirname(key[4])} {key[0]} -> {key[1]} {key[2]}"
                + (f" ({key[3]})" if key[3] else "") + (f" [{key[5]}]" if key[5] else "")
                + (f" E={key[6]}" if key[6] else "") + (f" A={key[7]}" if key[7] else ""))

    if args.map2d or args.plot3d:                    # the number of maps is given below; panels are not drawn
        print(f"{len(rows)} points from {len({r['entry'] for r in rows})} EXFOR entries, "
              f"{len({k[4] for k, _ in panels})} target(s).", file=sys.stderr)
    else:
        print(f"{len(rows)} points in {len(panels)} plots from {len({r['entry'] for r in rows})} EXFOR entries, "
              f"{len({k[4] for k, _ in panels})} target(s).", file=sys.stderr)
    for lab, why in (("complex", "complex reactions left out (use --include-complex)"),
                     ("status", "points dropped by --exclude-status"),
                     ("branch", "points dropped by --branch"),
                     ("at_energy", "points dropped by --at-energy"),
                     ("at_angle", "points dropped by --at-angle"),
                     ("unit", "points dropped because their unit differs from the plotted one"),
                     ("no_x", f"points without the coordinate '{args.x}'")):
        if log[lab]:
            print(f"  note: {log[lab]} {why}", file=sys.stderr)
    dense = [k for k, prs in panels if len(prs) > 1500]
    if dense and args.ms >= 4 and args.alpha >= 0.9 and not args.hollow and not args.map2d and not args.plot3d:
        print(f"  note: {len(dense)} plot(s) have more than 1500 points; if the markers hide each other, make them "
              f"smaller and transparent, for example --ms 2 --alpha 0.5 (also --hollow, --no-xerr, --no-yerr).",
              file=sys.stderr)
    for msg in ([] if (args.map2d or args.plot3d) else mixing_note(panels, args)):
        print(f"  note: {msg}", file=sys.stderr)
    if len(panels) > args.max_plots and not args.list and not (args.map2d or args.plot3d):
        sys.exit(f"{len(panels)} plots would be written (limit --max-plots {args.max_plots}). Restrict the selection "
                 f"(--product, --projectiles, --at-energy, --at-angle, --entries) or raise --max-plots; "
                 f"--list shows all of them.")
    if args.list and (args.map2d or args.plot3d):
        if args.map2d:
            make_grid_plots(rows, args, root, prefix_of, formats, None, "map", list_only=True)
        if args.plot3d:
            make_grid_plots(rows, args, root, prefix_of, formats, None, "3d", list_only=True)
        return 0
    if args.list:
        print(f"{'plot':40} {'series':>6} {'points':>7} {'x range':>20}" + ("   axes" if args.auto_axes else "")
              + "   file")
        dec_list = auto_axes([panel_points(prs, args) for _, prs in panels], args) if args.auto_axes else None
        for pi, (key, prs) in enumerate(panels):
            xs = [x_value(p, args.x) for p in prs]
            ns = len({(p['entry'], p['subentry'], p.get('branch', '')) for p in prs})
            fn = str(root / target_dirname(key[4]) / f"{plot_stem(key, prefix_of(key[4]), args)}.{formats[0] if formats else 'png'}")
            print(f"{label_of(key):40} {ns:6d} {len(prs):7d} {min(xs):9.4g} - {max(xs):9.4g}"
                  + (f"   {axes_text(dec_list[pi])}" + (f"   [{dec_list[pi]['note']}]" if dec_list[pi]["note"] else "")
                     if dec_list else "") + f"   {fn}")
        return 0

    if args.map2d or args.plot3d:
        written = []
        if args.map2d:
            written += make_grid_plots(rows, args, root, prefix_of, formats, plt, "map")
        if args.plot3d:
            written += make_grid_plots(rows, args, root, prefix_of, formats, plt, "3d")
        if args.references and written:
            written += write_plot_references(rows, meta, args, root, prefix_of, ref_formats)
        print(f"\n{len(written)} map/3D file(s) written to {root.resolve()}:\n  "
              + "\n  ".join(f"{root}/{w}" for w in written), file=sys.stderr)
        return 0 if written else 1
    by_target = collections.OrderedDict()
    for key, prs in panels:
        by_target.setdefault(key[4], []).append((key, prs))
    cols = max(1, args.cols)
    written = []
    for tcode, tpanels in by_target.items():
        tdir = root / target_dirname(tcode)
        tdir.mkdir(parents=True, exist_ok=True)
        prefix = prefix_of(tcode)
        if args.combine:
            groups = [tpanels[i:i + args.max_panels] for i in range(0, len(tpanels), args.max_panels)]
        else:
            groups = [[p] for p in tpanels]
        pdf = None
        if args.combine and "pdf" in formats:
            from matplotlib.backends.backend_pdf import PdfPages
            pdf = PdfPages(tdir / f"{prefix}.pdf")
            written.append(f"{tdir.name}/{prefix}.pdf")
        for ci, chunk in enumerate(groups, 1):
            n = len(chunk)
            single = not args.combine
            c = min(cols, n) if args.combine else 1
            r_ = math.ceil(n / c)
            fig, axes = plt.subplots(r_, c, figsize=(4.8 * c, 3.7 * r_) if args.combine else (6.4, 4.8), squeeze=False,
                                     sharex=args.sharex and args.combine, sharey=args.sharey and args.combine)
            for ax in axes.ravel()[n:]:
                ax.axis("off")
            if args.auto_axes:
                decs = auto_axes([panel_points(prs, args) for _, prs in chunk], args)
                for (key, _), d in zip(chunk, decs):
                    print(f"  auto axes {label_of(key)}: {axes_text(d)}" + (f"   [{d['note']}]" if d["note"] else ""),
                          file=sys.stderr)
            else:
                decs = [plain_axes(args)] * n
            for ax, (key, prs), d in zip(axes.ravel(), chunk, decs):
                draw_panel(ax, key, prs, styles, unit_of.get(key[2], ""), args, key[4], d, single=single)
            if args.combine:
                if args.legend == "figure":
                    seen = {}
                    for _, prs in chunk:
                        for p in prs:
                            seen.setdefault(p["entry"], f"{series_label(p)} [{p['entry']}]")
                    from matplotlib.lines import Line2D
                    handles = [Line2D([], [], marker=styles[e][1], color=styles[e][0], ls="", ms=6, label=l)
                               for e, l in sorted(seen.items(), key=lambda kv: kv[1])]
                    if len(handles) <= 30:
                        fig.legend(handles=handles, loc="lower center", ncol=min(len(handles), 5), fontsize=7)
                    else:
                        print(f"  note: figure legend omitted ({len(handles)} entries); select entries with --entries.",
                              file=sys.stderr)
                fig.suptitle(args.title or f"EXFOR data on {pretty(target_label(tcode))}", fontsize=11)
                fig.tight_layout(rect=[0, 0.06 if args.legend == "figure" else 0, 1, 0.97])
                stem = prefix + (f"_p{ci}" if len(groups) > 1 else "")
            else:
                if args.title:
                    axes.ravel()[0].set_title(args.title, fontsize=9)
                # fixed margins: tight_layout would squeeze the axes to make room for a legend outside the
                # plot; bbox_inches="tight" at saving adds the space on the right for the legend columns
                fig.subplots_adjust(left=0.11, right=0.97, top=0.93, bottom=0.12)
                stem = plot_stem(chunk[0][0], prefix, args)
            for fmt in formats:
                if fmt == "pdf" and pdf is not None:
                    pdf.savefig(fig)
                    continue
                fn = f"{stem}.{fmt}"
                fig.savefig(tdir / fn, dpi=args.dpi, bbox_inches="tight")
                written.append(f"{tdir.name}/{fn}")
            if args.show:
                plt.show()
            plt.close(fig)
        if pdf is not None:
            pdf.close()
    if args.references and written:
        written += write_plot_references(rows, meta, args, root, prefix_of, ref_formats)
    print(f"\n{len(written)} file(s) written to {root.resolve()}:\n  " + "\n  ".join(f"{root}/{w}" for w in written),
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
