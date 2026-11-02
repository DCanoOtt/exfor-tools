#!/usr/bin/env python3
"""
build_halflife_db.py  -  NUBASE2020 half-lives and isomers -> SQLite database
=============================================================================
Reads the NUBASE table of the Atomic Mass Data Center (AMDC, https://www-nds.iaea.org/amdc, or https://www.anl.gov/phy/reference/nubase-2020-nubase4mas20; file nubase_4.mas20 or
nubase_4.mas20.txt for NUBASE2020) and writes two files:

  1. nuclear_halflives.db   indexed SQLite database (table halflives); this is the file that exfor_retrieve.py reads for
                            --halflife (see "Setting the paths" in README.md) and that lookup_halflife.py queries
  2. nuclear_halflives.dat  the same data as a clean columnar ASCII table

Usage
-----
    python build_halflife_db.py /path/to/nubase_4.mas20.txt            # files are written next to the NUBASE file
    python build_halflife_db.py nubase_4.mas20.txt --out-dir data      # ... or into another folder
    python build_halflife_db.py                                        # looks for nubase_4.mas20(.txt) in this folder
                                                                       # (or the file named by the variable NUBASE_FILE)

Only the standard library is needed.  To update the database when the AMDC publishes a new evaluation, download the new
file and run this program again; the old database is replaced.  Then check it with
    python exfor_retrieve.py --check-halflives --halflife-db /path/to/nuclear_halflives.db
Cite the evaluation when you publish half-lives: F. G. Kondev, M. Wang, W. J. Huang, S. Naimi and G. Audi, Chin. Phys. C 45,
030001 (2021) (NUBASE2020).
"""

import argparse
import os
import re
import sqlite3
import sys

CANDIDATES = ("nubase_4.mas20.txt", "nubase_4.mas20", "nubase2020.txt")


def parse_nubase_line(line: str):
    """
    Parses fixed-width columns per NUBASE2020 specification:
      Cols   1:3   (line[0:3])    Mass Number AAA
      Cols   5:7   (line[4:7])    Atomic Number ZZZ
      Col    8     (line[7:8])    State indicator i (0=gs, 1,2=isomers, ...)
      Cols  12:16  (line[11:16])  Element Symbol
      Col   17     (line[16:17])  Isomer flag 's' (m, n, p, q, ...)
      Cols  43:54  (line[42:54])  Excitation Energy in keV
      Cols  55:65  (line[54:65])  Excitation Energy uncertainty in keV
      Cols  70:78  (line[69:78])  Half-life value T (or 'stbl', 'p-unst')
      Cols  79:80  (line[78:80])  Half-life unit
      Cols  82:88  (line[81:88])  Half-life uncertainty dT
      Cols  89:102 (line[88:102]) Spin and parity Jpi
    """
    if line.startswith("#") or len(line) < 80:
        return None

    try:
        a_str = line[0:3].strip()
        if not a_str.isdigit():
            return None
        a = int(a_str)

        z_str = line[4:7].strip()
        if not z_str.isdigit():
            return None
        z = int(z_str)

        state_idx = line[7:8].strip()
        raw_symbol = line[11:16].strip()

        elem_match = re.search(r"[A-Za-z]+", raw_symbol)
        if not elem_match:
            return None
        symbol = elem_match.group(0).capitalize()

        iso_flag = line[16:17].strip() if len(line) > 16 else ""
        exc_str = line[42:54].strip() if len(line) >= 54 else ""
        d_exc_str = line[54:65].strip() if len(line) >= 65 else ""

        hl_val = line[69:78].strip() if len(line) >= 78 else ""
        unit = line[78:80].strip() if len(line) >= 80 else ""
        unc = line[81:88].strip() if len(line) >= 88 else ""
        jpi = line[88:102].strip() if len(line) >= 102 else ""

        if not hl_val:
            return None

        # State label formatting (g.s., m1, m2, etc.)
        if state_idx == "0" or (not state_idx and not iso_flag):
            state = "g.s."
        else:
            state = f"m{state_idx}" if not iso_flag else f"{iso_flag}{state_idx}"

        if hl_val.lower() == "stbl":
            hl_display = "STABLE"
            unit = ""
            unc = ""
        else:
            hl_display = hl_val

        # Standard 5-digit ZZAAA representation (e.g. 13028 for 28Al)
        zzaaa = f"{z:02d}{a:03d}"

        return {
            "zzaaa": zzaaa,
            "z": z,
            "a": a,
            "symbol": symbol,
            "state": state,
            "state_idx": int(state_idx) if state_idx.isdigit() else 0,
            "exc_energy_kev": exc_str,
            "exc_unc_kev": d_exc_str,
            "half_life": hl_display,
            "unit": unit,
            "unc": unc,
            "jpi": jpi,
            "key_a_elem": f"{a}{symbol.lower()}",
            "key_elem_a": f"{symbol.lower()}{a}"
        }
    except Exception:
        return None


def export_ascii_dat(records, filename):
    """Exports clean, fixed-width columnar ASCII table."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# NUBASE2020 Evaluated Half-Lives & Isomeric States\n")
        f.write("# Source: Chin. Phys. C45, 030001 (2021) / AMDC / IAEA NDS\n")
        f.write("#" + "-" * 98 + "\n")
        header = (
            f"# {'ZZAAA':<6} {'Z':>3} {'A':>4} {'El':<3} {'State':<6} "
            f"{'E_exc (keV)':>14} {'dE (keV)':>10} {'T1/2':>14} {'Unit':<5} "
            f"{'dT':>10} {'Jpi':<14}\n"
        )
        f.write(header)
        f.write("#" + "-" * 98 + "\n")

        for r in records:
            line = (
                f"  {r['zzaaa']:<6} {r['z']:3d} {r['a']:4d} {r['symbol']:<3} {r['state']:<6} "
                f"{r['exc_energy_kev']:>14} {r['exc_unc_kev']:>10} {r['half_life']:>14} "
                f"{r['unit']:<5} {r['unc']:>10} {r['jpi']:<14}\n"
            )
            f.write(line)

    print(f"ASCII data file generated: '{filename}'")


def export_sqlite_db(records, filename):
    """Exports records to an indexed SQLite database."""
    if os.path.exists(filename):
        os.remove(filename)

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE halflives (
            zzaaa TEXT,
            z INTEGER,
            a INTEGER,
            symbol TEXT,
            state TEXT,
            state_idx INTEGER,
            exc_energy_kev TEXT,
            exc_unc_kev TEXT,
            half_life TEXT,
            unit TEXT,
            unc TEXT,
            jpi TEXT,
            key_a_elem TEXT,
            key_elem_a TEXT
        )
    """)

    cur.executemany("""
        INSERT INTO halflives VALUES (
            :zzaaa, :z, :a, :symbol, :state, :state_idx,
            :exc_energy_kev, :exc_unc_kev,
            :half_life, :unit, :unc, :jpi,
            :key_a_elem, :key_elem_a
        )
    """, records)

    # Multi-indexes for high-speed queries
    cur.execute("CREATE INDEX idx_key_a_elem ON halflives(key_a_elem);")
    cur.execute("CREATE INDEX idx_key_elem_a ON halflives(key_elem_a);")
    cur.execute("CREATE INDEX idx_za ON halflives(z, a);")
    cur.execute("CREATE INDEX idx_zzaaa ON halflives(zzaaa);")

    conn.commit()
    conn.close()

    print(f"SQLite database generated: '{filename}'")


def find_input(given):
    """The NUBASE file: the argument, the variable NUBASE_FILE, or a standard name in the current folder."""
    for c in ([given] if given else []) + [os.environ.get("NUBASE_FILE", "")] + list(CANDIDATES):
        if c and os.path.isfile(c):
            return c
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="NUBASE table -> nuclear_halflives.db and nuclear_halflives.dat")
    ap.add_argument("nubase", nargs="?", default=None,
                    help="the NUBASE file (nubase_4.mas20.txt); default: NUBASE_FILE or a file of that name in this folder")
    ap.add_argument("--out-dir", default=None, help="folder of the output files (default: the folder of the NUBASE file)")
    args = ap.parse_args(argv)

    path = find_input(args.nubase)
    if path is None:
        print("NUBASE file not found. Download nubase_4.mas20(.txt) from https://www-nds.iaea.org/amdc and give its path:\n"
              "  python build_halflife_db.py /path/to/nubase_4.mas20.txt", file=sys.stderr)
        return 2
    out_dir = args.out_dir or os.path.dirname(os.path.abspath(path))
    os.makedirs(out_dir, exist_ok=True)
    db_file = os.path.join(out_dir, "nuclear_halflives.db")
    dat_file = os.path.join(out_dir, "nuclear_halflives.dat")

    print(f"Reading: {path}")
    with open(path, "r", encoding="latin-1") as f:
        lines = f.readlines()

    records = []
    for line in lines:
        entry = parse_nubase_line(line)
        if entry:
            records.append(entry)

    n_gs = sum(1 for r in records if r["state"] == "g.s.")
    print(f"Parsed {len(records)} nuclear levels: {n_gs} ground states, {len(records) - n_gs} isomers and other levels.")
    if len(records) < 1000:
        print("WARNING: very few levels were read. Is this the NUBASE table (nubase_4.mas20), with its fixed columns?",
              file=sys.stderr)

    export_sqlite_db(records, db_file)
    export_ascii_dat(records, dat_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
