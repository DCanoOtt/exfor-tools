#!/usr/bin/env bash
# n_TOF (CERN) data in EXFOR other than cross sections: reaction yields (RYL), resonance widths (WID, WID/STR),
# resonance integrals (RI), strength functions (STF), gamma yields (PY, DE) and angular distributions (DA).
# Run it from any folder. The programs are found in the folder of the script or its parent; set PROGRAMS, DATA and OUT to change them.
#   bash plot_ntof_data.sh                 # all targets with such data (about 55, takes 10-15 minutes)
#   bash plot_ntof_data.sh Au-197 Am-243   # only these targets
PYTHON=python3
# PROGRAMS: the folder with exfor_retrieve.py and exfor_plot.py; by default the folder of this script or its parent
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if [ -z "${PROGRAMS:-}" ]; then
  if [ -f "$HERE/exfor_retrieve.py" ]; then PROGRAMS=$HERE
  elif [ -f "$HERE/../exfor_retrieve.py" ]; then PROGRAMS=$(cd "$HERE/.." && pwd)
  else echo "exfor_retrieve.py not found: set PROGRAMS=/path/to/exfor-tools when you run the script" >&2; exit 1; fi
fi
DATA=${DATA:-data_ntof}                                                  # relative to the folder where you run the script
OUT=${OUT:-plots_ntof}
QTY="RYL,WID,WID/STR,RI,STF,PY,DE,INT,DA"                                # quantities beyond SIG (add SIG for the cross sections)

R="$PROGRAMS/exfor_retrieve.py"
P="$PROGRAMS/exfor_plot.py"

# 1. what is there: the targets with n_TOF entries for these quantities (no files written)
"$PYTHON" "$R" --facility ntof --find --quantity "$QTY" --summary-only --max-rows 200

# 2. retrieve (CSV and one ASCII file per dataset, with errors) and the references
if [ "$#" -eq 0 ]; then
    "$PYTHON" "$R" --facility ntof --quantity "$QTY" --out "$DATA" --ascii --references
else
    for T in "$@"; do
        "$PYTHON" "$R" --facility ntof --target "$T" --quantity "$QTY" --out "$DATA" --ascii --references
    done
fi

# 3. plots, one folder per target. Reaction yields and resonance parameters span many decades: log energy axis.
for D in "$DATA"/*/; do
    "$PYTHON" "$P" --data "$D" --projectiles n --quantity RYL --logx --auto-axes --out "$OUT" --format png
    "$PYTHON" "$P" --data "$D" --projectiles n --quantity WID,WID/STR --logx --logy --out "$OUT" --format png
    "$PYTHON" "$P" --data "$D" --projectiles n --quantity RI,STF --out "$OUT" --format png
done
