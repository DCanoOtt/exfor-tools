#!/usr/bin/env bash
# plot_Al27_alpha_neutron_spectra.sh
# Neutron emission spectra at several angles from alpha particles on 27Al, from EXFOR.
#
# Run it from any folder (the programs exfor_retrieve.py and exfor_plot.py must have build 2026-10-07 or later,
# versions 2.2 and 1.2; their folder is the variable PROGRAMS below):
#     bash plot_Al27_alpha_neutron_spectra.sh
# Use another Python with:  PYTHON=python3 bash plot_Al27_alpha_neutron_spectra.sh
# Other folders for one run:  PROGRAMS=/path/to/programs DATA=/path/to/data OUT=plots bash plot_Al27_alpha_neutron_spectra.sh
#
# What EXFOR has (snapshot of 2026-09-28). Two groups of data, coded in different ways:
#
# A. Low energies, the 27Al(alpha,n)30P reaction: thick-target neutron spectra of Jacobs and Liskien (entry D0757,
#    G.J.H. Jacobs and H. Liskien, Ann. Nucl. Energy 10 (1983) 541). EXFOR codes them as the reaction to 30P, with the
#    quantity MLT (neutron multiplicity), not with the neutron as product; a search with --product n does not find them.
#
#   quantity    unit          alpha energy (MeV)        angles (deg)           entry
#   MLT/DA/DE   P/IN/MEVSR    4, 4.5, 5, 5.5            0, 30, 60, 100, 140    D0757  Jacobs 1983
#   MLT/DE      PRT/IN/MEV    4, 4.5, 5, 5.5            integrated             D0757  Jacobs 1983
#   MLT         PRT/INC       3.08 to 5.5               integrated             C3065 Brandenburg 2023, D0757 Jacobs 1983
#   KE          MEV           4, 4.5, 5, 5.5            mean neutron energy    D0757  Jacobs 1983
#
# B. High energies, neutron emission (alpha,xn) with the neutron as product; none below 30 MeV:
#
#   quantity   unit          alpha energy (MeV)                             angles (deg)   entry
#   PY/DA/DE   P/IN/MEVSR    30, 40, 50   thick Al target                   0, 30, 45      A0490  Dhar 2003
#   DA/DE      mb/sr/MeV     140                                            20 to 120      C0841  Kalend 1983
#   PY/DA/DE   P/IN/MEVSR    400, 720     thick target                      0 to 90        E2079  Satoh 2007 (it
#                                                                           supersedes E1810 Kurosawa 1999, which
#                                                                           --exclude-status SPSDD leaves out)
#   DA/DE      mb/sr/MeV     540                                            0 to 110       E1750  Sato 2001
#   PY/DA/DE   P/IN/MEVSR    620          thick target                      10 to 160      C1051  Heilbronn 1999
#   DA/DE      mb/sr/MeV     920                                            5 to 80        E2050  Heilbronn 2007
#   PY/DA/DE   P/IN/MEVSR    1600, 3200, 6000                               10 to 135      C3057  Ratliff 2023
#
# P/IN/MEVSR are neutron yields per incident alpha particle, per MeV and per steradian (thick targets); mb/sr/MeV are
# double-differential cross sections. Different units are never drawn in the same plot.
#
# Ratliff 2023 (C3057) has dual-thick-target measurements: an upstream aluminium target of 20, 40 or 60 g/cm2 and a
# downstream one of 60 g/cm2. Each configuration is a dataset of its own and it is plotted separately (the yield
# depends on the thickness). At 3200 MeV EXFOR has two datasets for each thickness (subentries 016-018 and 055-057);
# the entry does not say what distinguishes them. The subentries 104 to 109 of the entry are aluminium plus
# polyethylene targets, a sum of two reactions: they are complex reactions and are left out.

set -e

# PATHS: edit these lines, or set the variables when you run the script
PYTHON=${PYTHON:-python}
# PROGRAMS: the folder with exfor_retrieve.py and exfor_plot.py; by default the folder of this script or its parent
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if [ -z "${PROGRAMS:-}" ]; then
  if [ -f "$HERE/exfor_retrieve.py" ]; then PROGRAMS=$HERE
  elif [ -f "$HERE/../exfor_retrieve.py" ]; then PROGRAMS=$(cd "$HERE/.." && pwd)
  else echo "exfor_retrieve.py not found: set PROGRAMS=/path/to/exfor-tools when you run the script" >&2; exit 1; fi
fi
DATA=${DATA:-data}                               # the retrieved data are in "$DATA/Al-27" (relative to the folder where you run)
OUT=${OUT:-plots_Al27_alpha_n}                   # folder of the plots (relative to the folder where you run the script)
FORMATS=png,pdf                                  # output formats
# The EXFOR master files are those of exfor_retrieve.py (its constant MASTER_DEFAULT); to use another folder add
# --master /path/to/exfor_master to the retrieve command of step 1.

retrieve() { "$PYTHON" "$PROGRAMS/exfor_retrieve.py" "$@"; }
plot()     { "$PYTHON" "$PROGRAMS/exfor_plot.py" "$@"; }

# 1. Retrieve the data once, with the list of their references ("$DATA/Al-27/EXFOR_AL-27_references.txt" and .bib).
retrieve --target Al-27 --projectiles a --product "n,P-30" --out "$DATA" \
    --quantity "DA/DE,PY/DA/DE,MLT/DA/DE,MLT/DE,MLT,KE" --references --ref-format txt,bib

# 2. A. Low energies (Jacobs and Liskien): one plot for each alpha energy; all the angles are drawn in one plot, each
#    labelled at the right of the data; --stack 10 multiplies them by 1, 10, 100 ... in order of increasing angle so
#    that they do not overlap on the logarithmic y axis (the factor is in the label).
for E in 4 4.5 5 5.5; do
    echo "--- alpha energy $E MeV (Jacobs and Liskien)"
    plot --data "$DATA/Al-27" --projectiles a --product P-30 --quantity MLT/DA/DE --x Eout \
        --at-energy $E --tol 0.1 --exclude-status SPSDD --angle-labels --stack 10 --logy --format $FORMATS \
        --out "$OUT/low/E${E}MeV"
done
#    The spectrum integrated over the angles, the four energies in one plot
plot --data "$DATA/Al-27" --projectiles a --product P-30 --quantity MLT/DE --x Eout \
    --energy-labels --stack 10 --logy --format $FORMATS --out "$OUT/low/integrated"
#    The neutron yield per incident alpha particle (Brandenburg 2023 and Jacobs 1983) and the mean neutron energy
plot --data "$DATA/Al-27" --projectiles a --product P-30 --quantity MLT --logy --format $FORMATS \
    --out "$OUT/low/yield"
plot --data "$DATA/Al-27" --projectiles a --product P-30 --quantity KE --format $FORMATS \
    --out "$OUT/low/mean_energy"

# 3. B. High energies: one plot for each incident energy and each kind of data.
COMMON=(--data "$DATA/Al-27" --projectiles a --product n --quantity DA/DE,PY/DA/DE --x Eout --exclude-status SPSDD
        --angle-labels --stack 10 --logy --logx --format $FORMATS)
for E in 30 40 50 140 400 540 620 720 920; do
    echo "--- incident energy $E MeV"
    plot "${COMMON[@]}" --at-energy $E --tol 1 --exclude-entries C3057 --out "$OUT/E${E}MeV"
done

# 4. Ratliff 2023: one plot for each target configuration (energy:subentry:thickness of the upstream target).
for ITEM in 1600:C3057013:20 1600:C3057014:40 1600:C3057015:60 \
            3200:C3057016:20 3200:C3057017:40 3200:C3057018:60 \
            3200:C3057055:20 3200:C3057056:40 3200:C3057057:60 \
            6000:C3057061:20 6000:C3057062:40 6000:C3057063:60; do
    IFS=: read E SUB UP <<< "$ITEM"
    echo "--- incident energy $E MeV, $SUB, upstream target $UP g/cm2"
    plot "${COMMON[@]}" --at-energy $E --tol 1 --entries $SUB \
        --title "\$^{27}\$Al(\$\\alpha\$,x)n  E = $E MeV, upstream Al target $UP g/cm\$^2\$  [$SUB]" \
        --out "$OUT/E${E}MeV_$SUB"
done

# 5. Optional: the same spectra as 2D maps (neutron energy against angle), one per dataset and energy:
#    plot --data "$DATA/Al-27" --projectiles a --product "n,P-30" --quantity "DA/DE,PY/DA/DE,MLT/DA/DE" --map2d --out "$OUT/maps"

# 6. Optional: the (alpha,n) cross section to 30P and the neutron production cross section:
#    plot --target Al-27 --projectiles a --product P-30 --process N --include-complex \
#        --exclude-status SPSDD --logy --xlim 2,32 --ylim 0.1,1000
#    plot --target Al-27 --projectiles a --product n --quantity SIG --include-complex --logy

echo "Plots in $OUT/ ; references in $DATA/Al-27/"
