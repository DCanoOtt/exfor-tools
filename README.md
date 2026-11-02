# EXFOR tools

Python programs to retrieve and plot nuclear reaction data from the EXFOR library of the
IAEA Nuclear Data Section, and to compare them with evaluated data files (ENDF).

Current versions: `exfor_retrieve.py` 2.3 and `exfor_plot.py` 1.4 (build 2026-10-27; `--version` prints them) and `endf_reader.py` 1.0.

| Program | What it does |
| --- | --- |
| `exfor_retrieve.py` | Retrieves the EXFOR data for reactions induced on one target isotope by the projectiles of your choice (neutrons, protons, deuterons, tritons, 3He, alphas, photons, electrons, pions, kaons, antiprotons, heavy ions, or all of them), optionally restricted to a final product (for example `Nb-92m`). Writes CSV (and optionally JSON) tables. |
| `exfor_plot.py` | Plots the selected data as excitation functions with error bars, one plot (one file) per target, projectile and product. It can read the files written by `exfor_retrieve.py` or run the retrieval itself. With `--endf` it draws evaluated cross sections (ENDF-6 files) over the data. |
| `build_halflife_db.py`, `lookup_halflife.py` | Convert the NUBASE table into the SQLite half-life database (`nuclear_halflives.db`) that `--halflife` reads, and look up a half-life in it from the command line. |
| `endf_reader.py` | Reads evaluated nuclear data files in ENDF-6 format (File 3 cross sections with all interpolation laws, the header and the resonance ranges). Used by `exfor_plot.py --endf`; it can also be used on its own (`python endf_reader.py FILE`). Needs `exfor_plot.py` and `endf_reader.py` in the same folder. |

The programs read the complete EXFOR library from the IAEA-NDS repository
[exfor_master](https://github.com/IAEA-NDS/exfor_master) (cloned once, about 1.4 GB), so queries are
local and repeatable.

More features, all described in the manual:

- **References** of the datasets you use: `--references` writes a text list and BibTeX.
- **One ASCII file per dataset** (`--ascii`), in columns with the units in the first row, or far fewer
  files for fission yields (`--ascii-format entry` or `quantity`).
- **Half-lives** of the isotopes from the NUBASE2020 evaluation next to the target and the products
  (`--halflife`, needs the SQLite database of half-lives, see the manual), and in the titles of the plots.
- **Fission yields** against A, Z and the incident energy, as curves, 2D maps and 3D plots.
- **Spectra, angular distributions, 2D maps and 3D plots**, and axis labels made from the EXFOR coding.
- **Facility filter** (`--facility ntof`): only the entries measured at n_TOF (CERN), with yields, resonance widths, resonance integrals and strength functions as well as cross sections; for all targets at once.
- **Evaluated data over the EXFOR data** (`--endf`): the cross sections of ENDF-6 files (ENDF/B, JEFF, JENDL, CENDL, TENDL ...) as lines over the EXFOR points, for neutron-induced reactions (see below).
- Search over all targets (`--find`), and the date and version of the EXFOR data (`--master-info`).

## Requirements

- Python 3.8 or later (tested with 3.12)
- git (recommended; without it the EXFOR files are downloaded as a zip archive)
- matplotlib and numpy, for `exfor_plot.py` (`pip install -r requirements.txt`)
- optional, for `--halflife`: a SQLite database of NUBASE2020 half-lives, made with `build_halflife_db.py` from the NUBASE table (included; see "Updating the data")

## Quick start

```bash
# retrieve deuteron cross sections on 93Nb, only the products 92mNb and 89Zr
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m,Zr-89
# -> data/Nb-93/EXFOR_NB-93_data.csv and EXFOR_NB-93_datasets.csv

# plot them
python exfor_plot.py --data data/Nb-93
# -> plots/Nb-93/Nb-93_d_92mNb.png, Nb-93_d_89Zr.png

# or retrieve and plot in one step (the data are also saved in data/Nb-93/)
python exfor_plot.py --target Nb-93 --projectiles d --product 92mNb,89Zr --auto-axes
```

To check what EXFOR has before retrieving anything, and to write the references of the datasets you use:

```bash
python exfor_retrieve.py --target Nb-93 --available                  # projectiles, quantities, products with data
python exfor_retrieve.py --target Nb-93 --projectiles d --available entries   # the EXFOR entries
python exfor_retrieve.py --find --projectiles d --product Nb-92m     # which targets have such data
python exfor_plot.py --data data/Nb-93 --product 92mNb --references  # references (txt and BibTeX) next to the plots
```

The first run downloads the EXFOR master files into a folder `exfor_master` (30 seconds to a few
minutes; or clone them yourself, see "Setting the paths" below). A search takes about 20 seconds to a minute.

Useful options: `--projectiles all`, `--projectiles=all,-n`, `--product "Zr-*"`, `--summary-only`
(see what exists before writing files), `--auto-axes`, `--logx`, `--logy`, `--exclude-entries`,
`--combine`. Run `python exfor_retrieve.py -h` and `python exfor_plot.py -h`, or read the manual.

## Evaluated data over the EXFOR data (`--endf`)

```bash
python exfor_plot.py --target U-238 --projectiles n --product none --process F --logx --logy \
       --endf n_092-U-238.endf --endf-label "ENDF/B-VIII.0"
python exfor_plot.py --data data/Fe-56 --projectiles n --process TOT,EL \
       --endf endf-b8/n_026_Fe_056.endf jeff33/Fe056.jeff --endf-label ENDF/B-VIII.0 JEFF-3.3
python exfor_plot.py --data data/U-238 --projectiles n --process G --product 239U --endf pendf/u238_300K.pendf
```

`--endf` takes files, wildcards and folders (from a folder only the files of the target of a plot are read).
Each file gives one line, labelled with the library and version that the file states; `--endf-label` overrides
the names. The reaction type of the plot picks the cross section: TOT, EL, NON, INL, 2N, 3N, F, G, P, D, T, HE3, A
and others (MT 1, 2, 3, 4, 16, 17, 18, 102 - 107 ...), converted to the unit of the plot. Only neutron-induced
cross sections (`SIG`) get a line; a note says why a plot gets none.

**Resonances.** In an evaluated file the resolved resonance range is stored as resonance parameters, which the
program does not reconstruct; File 3 holds only a background there. By default the line therefore starts above the
resonance range (a note says where). For the resonances use a pointwise (PENDF) file, which is drawn over its whole
range; `--endf-full` draws File 3 below the resonance range too (the background only, marked in the legend).
Other options: `--endf-lw` (line width), `--endf-sub` (points per non-linear interval).

Tests (the ENDF files are synthetic; the check against an independent parser needs `pip install endf-parserpy`):
`python tests/test_endf.py`; the half-life programs: `python tests/test_halflife.py` (synthetic NUBASE-format lines).

## Setting the paths

Nothing needs to be edited if you run the programs from the folder where you want `exfor_master`, `data` and
`plots` to appear. To keep the EXFOR database in one fixed place, tell the programs where it is. Use **one** of these,
in the order in which the programs look at them:

| What | Command line | Environment variable | Constant in the script |
| --- | --- | --- | --- |
| **EXFOR master files** | `--master /path/to/exfor_master` | `EXFOR_MASTER` | `MASTER_DEFAULT` at the top of `exfor_retrieve.py` |
| **Half-life database** (optional) | `--halflife-db /path/to/nuclear_halflives.db` | `EXFOR_HALFLIFE_DB` | `HALFLIFE_DB_DEFAULT` in `exfor_retrieve.py` |
| **Folder of the programs** (examples only) | `--programs-dir /path/to/exfor-tools` | `EXFOR_PROGRAMS_DIR` | `PROGRAMS_DIR` in the example script |

**What the paths must point at:**

- `MASTER_DEFAULT`, `EXFOR_MASTER` and `--master` point to the folder **that contains the sub-folder `exforall`**, that
  is, the clone of <https://github.com/IAEA-NDS/exfor_master>. If your clone is `/home/you/nuclear-data/exfor_master`, then
  `/home/you/nuclear-data/exfor_master/exforall/` must exist, and that is the path to give (not `.../exforall`, and not
  the folder above). `python exfor_retrieve.py --master-info` prints the folder, date and version that are used.
- `HALFLIFE_DB_DEFAULT`, `EXFOR_HALFLIFE_DB` and `--halflife-db` point to the **file** `nuclear_halflives.db` (SQLite), not
  to its folder. Without it the half-lives are simply not printed.
- `PROGRAMS_DIR` (examples) points to the folder with `exfor_retrieve.py` and `exfor_plot.py`. Leave it empty when the
  example is kept in the `examples` folder of this package or next to the programs: it is then found by itself.

Examples (Linux and macOS; on Windows use `set EXFOR_MASTER=C:\data\exfor_master` or `setx`):

```bash
export EXFOR_MASTER=/home/you/nuclear-data/exfor_master        # add to ~/.bashrc or ~/.zshrc to make it permanent
export EXFOR_HALFLIFE_DB=/home/you/nuclear-data/nuclear_halflives.db
```

or edit the two lines at the top of `exfor_retrieve.py`:

```python
MASTER_DEFAULT = "/home/you/nuclear-data/exfor_master"
HALFLIFE_DB_DEFAULT = "/home/you/nuclear-data/nuclear_halflives.db"
```

The `.sh` examples find the programs in their own folder or its parent; set `PROGRAMS`, `DATA` and `OUT` when you run
them to change this. The data and the plots are written relative to the folder where you run a command, never inside
the package.

### Downloading the EXFOR database yourself

```bash
git clone --depth 1 https://github.com/IAEA-NDS/exfor_master.git exfor_master    # about 1 GB; --depth 1: no history
# without git: download https://codeload.github.com/IAEA-NDS/exfor_master/zip/refs/heads/main, unzip, rename the folder
python exfor_retrieve.py --master-info                          # which version you have, and whether GitHub has a newer one
python exfor_retrieve.py --target Nb-93 --projectiles d --update  # git pull before the search
```

Do not add `exfor_master` to a git repository of your own (the database is 1.4 GB); the `.gitignore` of this package
excludes it.

## Updating the data

### The EXFOR database

The IAEA-NDS publishes new EXFOR master files from time to time in <https://github.com/IAEA-NDS/exfor_master>. Your copy does
not change by itself.

```bash
python exfor_retrieve.py --master-info                  # your date and commit, and whether GitHub has a newer snapshot
python exfor_retrieve.py --target Nb-93 --projectiles d --update   # git pull the master files, then search (any retrieval)
# or by hand, in the folder of the master files:
git -C /path/to/exfor_master pull
```

If you downloaded the zip file instead of cloning, download it again
(<https://codeload.github.com/IAEA-NDS/exfor_master/zip/refs/heads/main>) and unzip it over the folder, or delete the folder: the next
run downloads it again.

**The data you retrieved earlier do not change.** `data/<target>/` holds what EXFOR contained when you retrieved it, and
`exfor_plot.py --data data/<target>` plots those files. To refresh them, update the master files and retrieve again (delete the
folder, or run `exfor_retrieve.py` for the same target; a path that does not exist is retrieved again by `exfor_plot.py --data`). Write the
EXFOR version with your results: `--master-info` prints it.

### The NUBASE and AME tables (half-lives and masses)

NUBASE (nuclear properties: half-lives, isomers) and AME (atomic masses) are evaluated together by the Atomic Mass Data Center
(AMDC): <https://www-nds.iaea.org/amdc>. The latest evaluation on that page is **AME2020 / NUBASE2020** (F. G. Kondev et al., Chin. Phys. C 45
(2021) 030001 for NUBASE; M. Wang et al., Chin. Phys. C 45 (2021) 030003 for AME). Its files are `nubase_4.mas20` (NUBASE: half-lives
and isomers) and `mass_1.mas20` (AME: atomic masses); the page gives the exact names and links.

**These programs read only NUBASE**, and only for `--halflife` (the half-lives next to the isotopes in titles and tables), through
the SQLite file `nuclear_halflives.db` (table `halflives`: `z, a, state, state_idx, exc_energy_kev, half_life, unit`). The AME masses
are not used.

To update, when the AMDC publishes a new evaluation:

1. Download the new NUBASE file (`nubase_4.mas20`) from the AMDC page <https://www-nds.iaea.org/amdc> or from the Argonne National Laboratory page
   <https://www.anl.gov/phy/reference/nubase-2020-nubase4mas20> (and AME if you need it for other work). Both give the same file; if your browser
   adds `.txt` to the name, that is fine.
2. Build the SQLite file (only the Python standard library is needed):
   ```bash
   python build_halflife_db.py /path/to/nubase_4.mas20.txt            # writes nuclear_halflives.db and .dat next to that file
   python build_halflife_db.py nubase_4.mas20.txt --out-dir data       # or into another folder
   ```
   The program prints the number of levels read (it warns if there are very few, which means the file
   is not the fixed-column NUBASE table). The old database is replaced. `python lookup_halflife.py 99mTc` (or `Al-28`, `242mAm`,
   `13028`; `--db FILE` or `EXFOR_HALFLIFE_DB` choose the database) prints the half-lives of a nuclide and its isomers, to check it.
3. Put the new file at the path that `HALFLIFE_DB_DEFAULT`, `EXFOR_HALFLIFE_DB` or `--halflife-db` points to (see "Setting the paths").
4. Check it: `python exfor_retrieve.py --check-halflives` compares the half-lives assigned to the EXFOR states with those that the
   EXFOR entries quote themselves, and `python exfor_retrieve.py --target Nb-93 --projectiles d --summary-only --halflife` prints the
   half-lives next to the isotopes.
5. Change the evaluation named in the "Notes" below (the citation) and in the manual, if the evaluation is not NUBASE2020 any more.

## Output layout

```text
data/<target name>/   data and dataset tables (CSV, optionally JSON)
plots/<target name>/  one plot per target, projectile and product
```

Natural targets are named `Ti-nat`, `Cu-nat`, and so on.

## Examples

- `examples/plot_Al27_alpha_neutron_spectra.sh`: retrieves and plots the neutron spectra at several angles from alpha
  particles on 27Al (4 to 5.5 MeV, Jacobs and Liskien 1983, and 30 MeV to 6 GeV), with the list of references (`bash examples/plot_Al27_alpha_neutron_spectra.sh`; Section 16.8 of the manual).

- `examples/plot_neutron_emission.py`: all the neutron spectra and yields of an (x,n) reaction on any isotope, in three kinds
  of plots: exclusive (the reaction to the residual nucleus), inclusive (the neutron as product) and the two combined,
  with a table of the coverage of the datasets (`python plot_neutron_emission.py Al-27`; Section 16.9 of the manual).

- `examples/plot_ntof_data.sh`: n_TOF data other than cross sections (reaction yields, resonance widths, resonance integrals, strength functions) for all targets or a list of them (`bash plot_ntof_data.sh Au-197 Am-243`; Section 16.10 of the manual).
- `examples/plot_ntof_reactions.py`: the n_TOF data in EXFOR for a table of reactions (Li, Be, B, Cr, Fe, Ni, W, Zr, Mo, C, N, S, Cl, Pb, Bi, 7Be), with a table of the reactions that EXFOR does not have (`python plot_ntof_reactions.py --also RYL`; Section 16.11 of the manual).

The programs are found automatically in the folder of the package; the paths of the programs, the data and the plots can be
changed at the top of each script or on the command line (see "Setting the paths").

## Documentation

The full user manual is in [docs/user_manual.md](docs/user_manual.md).

## Notes

- The programs retrieve what is in EXFOR; they do not judge data quality, and the plots show the
  data as they are (EXFOR contains outliers and duplicated or superseded datasets).
- The programs were tested on a limited set of targets (93Nb, 55Mn, natTi, natCu, 63Cu, 56Fe, 208Pb,
  235U, 238U and a few others) and on Linux. Other systems and unusual EXFOR entries may need fixes.
- When you publish results, cite the original publications of the data and EXFOR itself
  (N. Otuka et al., Nucl. Data Sheets 120 (2014) 272, doi:10.1016/j.nds.2014.07.065).
- If you publish half-lives printed by the programs, cite the NUBASE2020 evaluation:
  F. G. Kondev, M. Wang, W. J. Huang, S. Naimi and G. Audi, The NUBASE2020 evaluation of nuclear
  physics properties, Chin. Phys. C 45, 030001 (2021).

## License

The programs are released under the MIT licence, see [LICENSE](LICENSE). The EXFOR data they retrieve are distributed by the IAEA Nuclear Data Section under CC BY 4.0; evaluated files that you plot keep the licences of their libraries.
