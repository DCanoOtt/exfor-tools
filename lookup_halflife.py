#!/usr/bin/env python3
"""
Offline nuclear half-life lookup utility: queries the SQLite database nuclear_halflives.db made by build_halflife_db.py
from the NUBASE2020 table.

Usage:
    python lookup_halflife.py 99mTc
    python lookup_halflife.py Al-28 --db /path/to/nuclear_halflives.db

The database is the one given by --db, else the variable EXFOR_HALFLIFE_DB, else nuclear_halflives.db in the current folder or
next to this script (the same file that exfor_retrieve.py reads, see "Setting the paths" in README.md).

Supported inputs:
  - 28Al, Al-28, Al28
  - 99mTc, Tc-99m, Tc99m
  - 242Am, 242mAm, Am-242m1
  - 13028 (ZZAAA notation)
"""

import os
import re
import sqlite3
import sys

DB_FILE = ""      # set here, or use --db or EXFOR_HALFLIFE_DB; empty: nuclear_halflives.db in this folder or next to the script


def find_db(given=None):
    here = os.path.dirname(os.path.abspath(__file__))
    for c in ([given] if given else []) + [DB_FILE, os.environ.get("EXFOR_HALFLIFE_DB", ""),
                                           "nuclear_halflives.db", os.path.join(here, "nuclear_halflives.db")]:
        if c and os.path.isfile(c):
            return c
    return None

def parse_input(query_str: str):
    """
    Parses various input notations into (query_mode, value).
    Returns:
      ('zzaaa', '13028')
      ('keys', ['28al'])            candidate keys A+element; the database is asked for all of them
    A leading isomer letter is ambiguous with an element symbol (99mTc: isomer m of Tc; 99Mo: molybdenum), so both
    readings are offered and the one that exists in the database is found.
    """
    clean = query_str.strip().lower().replace("-", "")

    # 1. ZZAAA format (e.g. 13028 -> Z=13, A=28)
    if clean.isdigit() and len(clean) == 5:
        return ("zzaaa", clean)

    # 2. A + (isomer letter) + Elem (e.g. 28al, 99mtc, 242mam, 99mo)
    m1 = re.match(r"^(\d+)([a-z]{1,4})(?:\d*)$", clean)
    if m1:
        a, letters = m1.groups()
        keys = []
        if len(letters) <= 2:
            keys.append(f"{a}{letters}")
        if len(letters) >= 2 and letters[0] in "mnpqrxyz" and len(letters) - 1 <= 2:
            keys.append(f"{a}{letters[1:]}")
        if keys:
            return ("keys", keys)

    # 3. Elem + A (+ isomer letter and number) (e.g. al28, tc99m, am242, am242m1)
    m2 = re.match(r"^([a-z]{1,2})(\d+)(?:[a-z]\d*)?$", clean)
    if m2:
        elem, a = m2.groups()
        return ("keys", [f"{a}{elem}"])

    return ("keys", [clean])


def query_halflife(user_input: str, db=None):
    db_file = find_db(db)
    if db_file is None:
        print("Error: database nuclear_halflives.db not found. Build it with build_halflife_db.py from the NUBASE table, "
              "and give its path with --db or EXFOR_HALFLIFE_DB.")
        return

    mode, val = parse_input(user_input)

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    if mode == "zzaaa":
        cur.execute("""
            SELECT zzaaa, z, a, symbol, state, exc_energy_kev, exc_unc_kev,
                   half_life, unit, unc, jpi
            FROM halflives
            WHERE zzaaa = ?
            ORDER BY state_idx ASC
        """, (val,))
    else:
        cur.execute("""
            SELECT zzaaa, z, a, symbol, state, exc_energy_kev, exc_unc_kev,
                   half_life, unit, unc, jpi
            FROM halflives
            WHERE key_a_elem IN ({q}) OR key_elem_a IN ({q})
            ORDER BY z, state_idx ASC
        """.format(q=",".join("?" * len(val))), tuple(val) + tuple(val))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"No records found for input: '{user_input}'")
        return

    zzaaa, z, a, symbol = rows[0][0], rows[0][1], rows[0][2], rows[0][3]

    print(f"\nNuclide: {symbol}-{a} (Z={z}, A={a} | ZZAAA: {zzaaa}) — NUBASE2020 Evaluated")
    print(f"{'State':<7} | {'E_exc (keV)':<16} | {'Jπ':<12} | {'T1/2':<26}")
    print("-" * 68)

    for r in rows:
        state = r[4]
        e_exc = r[5].strip() if r[5] else ""
        d_exc = r[6].strip() if r[6] else ""
        hl = r[7].strip()
        unit = r[8].strip()
        unc = r[9].strip()
        jpi = r[10].strip() if r[10] else "-"

        # Format excitation energy
        if state == "g.s." or not e_exc:
            level_str = "0.0 (g.s.)"
        else:
            level_str = f"{e_exc}"
            if d_exc:
                level_str += f" ± {d_exc}"

        # Format half-life string
        if hl == "STABLE":
            hl_str = "STABLE"
        else:
            unc_str = f" ± {unc}" if unc else ""
            unit_str = f" {unit}" if unit else ""
            hl_str = f"{hl}{unc_str}{unit_str}".strip()

        print(f"{state:<7} | {level_str:<16} | {jpi:<12} | {hl_str:<26}")

    print("-" * 68 + "\n")


if __name__ == "__main__":
    argv = sys.argv[1:]
    db_arg = None
    if "--db" in argv:
        k = argv.index("--db")
        db_arg = argv[k + 1] if k + 1 < len(argv) else None
        del argv[k:k + 2]
    if argv:
        target = argv[0]
    else:
        target = input("Enter nuclide (e.g., 28Al, Al-28, 99mTc, 242Am, 13028): ")
    query_halflife(target, db_arg)
    