# EXFOR retrieval and plotting scripts: user manual (exfor\_retrieve.py 2.3, exfor\_plot.py 1.4, endf\_reader.py 1.0)

**Author:** Daniel Cano Ott · **Last updated:** 2 November 2026 (paths, `--endf` Section 14.14, half-life database tools)

This manual belongs to the repository [exfor-tools](https://github.com/DCanoOtt/exfor-tools); the README there is the short version. Some worked examples were run on the EXFOR master files of 2026-09-28; numbers you obtain with a newer snapshot can differ slightly.

## Contents

- [1. Purpose](#1-purpose)
- [2. How it works](#2-how-it-works)
- [3. Requirements and installation](#3-requirements-and-installation)
  - [3.1 Downloading the EXFOR master files](#31-downloading-the-exfor-master-files)
  - [3.2 Updating and checking the EXFOR master files: step by step](#32-updating-and-checking-the-exfor-master-files-step-by-step)
- [4. Quick start](#4-quick-start)
- [5. What is available in EXFOR, and the list of references](#5-what-is-available-in-exfor-and-the-list-of-references)
  - [5.1 What EXFOR has for a target](#51-what-exfor-has-for-a-target)
  - [5.2 Which targets have data? (search over all targets)](#52-which-targets-have-data-search-over-all-targets)
  - [5.3 The list of references of the datasets](#53-the-list-of-references-of-the-datasets)
  - [5.4 A routine from the question to the references](#54-a-routine-from-the-question-to-the-references)
  - [5.5 Changes in the data and datasets files](#55-changes-in-the-data-and-datasets-files)
  - [5.6 Quick reference: checking the data and getting the references](#56-quick-reference-checking-the-data-and-getting-the-references)
- [6. Command-line reference](#6-command-line-reference)
- [7. Selecting projectiles and products](#7-selecting-projectiles-and-products)
  - [7.1 The --projectiles string](#71-the---projectiles-string)
  - [7.2 Particles in EXFOR](#72-particles-in-exfor)
  - [7.3 Heavy ions](#73-heavy-ions)
  - [7.4 Groups](#74-groups)
  - [7.5 How much data to expect](#75-how-much-data-to-expect)
  - [7.6 Selecting the final product (--product)](#76-selecting-the-final-product---product)
- [8. Output files](#8-output-files)
  - [8.1 Files](#81-files)
  - [8.2 Columns of the data file](#82-columns-of-the-data-file)
  - [8.3 Columns of the datasets file](#83-columns-of-the-datasets-file)
  - [8.4 Energies](#84-energies)
  - [8.5 JSON output (--json)](#85-json-output---json)
  - [8.6 One ASCII file per dataset (`--ascii`)](#86-one-ascii-file-per-dataset---ascii)
- [9. Worked examples](#9-worked-examples)
  - [9.1 Choose projectiles, quantity and energy](#91-choose-projectiles-quantity-and-energy)
  - [9.2 Natural targets and several targets in a loop](#92-natural-targets-and-several-targets-in-a-loop)
  - [9.3 Which datasets exist for one product?](#93-which-datasets-exist-for-one-product)
  - [9.4 Plot an excitation function from all datasets](#94-plot-an-excitation-function-from-all-datasets)
  - [9.5 Energy per nucleon for heavy ions](#95-energy-per-nucleon-for-heavy-ions)
  - [9.6 Update the local copy](#96-update-the-local-copy)
  - [9.7 Select the final product](#97-select-the-final-product)
  - [9.8 Save each dataset as an ASCII file: examples](#98-save-each-dataset-as-an-ascii-file-examples)
  - [9.9 Half-lives next to the isotopes: examples](#99-half-lives-next-to-the-isotopes-examples)
- [10. Interpreting the results: good practice](#10-interpreting-the-results-good-practice)
  - [10.1 Status codes: which data to exclude](#101-status-codes-which-data-to-exclude)
  - [10.2 Half-lives of the isotopes (NUBASE2020)](#102-half-lives-of-the-isotopes-nubase2020)
- [11. Troubleshooting](#11-troubleshooting)
- [12. Reproducibility and citation](#12-reproducibility-and-citation)
- [13. Limitations](#13-limitations)
- [14. Plotting the selected data (exfor\_plot.py)](#14-plotting-the-selected-data-exfor_plotpy)
  - [14.1 Requirements and use](#141-requirements-and-use)
  - [14.2 What is plotted](#142-what-is-plotted)
  - [14.3 Options](#143-options)
  - [14.4 Examples](#144-examples)
  - [14.5 Notes](#145-notes)
  - [14.6 Typical workflow](#146-typical-workflow)
  - [14.7 Automatic axes (--auto-axes)](#147-automatic-axes---auto-axes)
  - [14.8 Example: fission, total and capture of 238U](#148-example-fission-total-and-capture-of-238u)
  - [14.9 Many points: when the markers hide each other](#149-many-points-when-the-markers-hide-each-other)
  - [14.10 Fission yields in 2D and 3D](#1410-fission-yields-in-2d-and-3d)
  - [14.11 How fission yields are stored in EXFOR](#1411-how-fission-yields-are-stored-in-exfor)
  - [14.12 Half-lives in the titles of the plots](#1412-half-lives-in-the-titles-of-the-plots)
  - [14.13 Axis labels: quantity, unit and emitted particle](#1413-axis-labels-quantity-unit-and-emitted-particle)
  - [14.14 Evaluated data over the EXFOR data (`--endf`)](#1414-evaluated-data-over-the-exfor-data---endf)
- [15. Example: beta-delayed neutron spectra and neutron yields](#15-example-beta-delayed-neutron-spectra-and-neutron-yields)
  - [15.1 Beta-delayed neutron spectra of individual precursors](#151-beta-delayed-neutron-spectra-of-individual-precursors)
  - [15.2 Delayed neutrons from fission](#152-delayed-neutrons-from-fission)
  - [15.3 Neutron yields](#153-neutron-yields)
  - [15.4 Practical notes](#154-practical-notes)
- [16. Example: neutron spectra from charged-particle reactions](#16-example-neutron-spectra-from-charged-particle-reactions)
  - [16.1 How these data are coded](#161-how-these-data-are-coded)
  - [16.2 Retrieve](#162-retrieve)
  - [16.3 Choose the incident energy and the angle](#163-choose-the-incident-energy-and-the-angle)
  - [16.4 Practical notes](#164-practical-notes)
  - [16.5 Several angles in one plot, and 2D maps](#165-several-angles-in-one-plot-and-2d-maps)
  - [16.6 3D plots and other pairs of variables](#166-3d-plots-and-other-pairs-of-variables)
  - [16.7 A spectrum coded as a cross section: 27Al(d,n)28Si](#167-a-spectrum-coded-as-a-cross-section-27aldn28si)
  - [16.8 Neutron spectra at several angles from alpha particles on 27Al: a script](#168-neutron-spectra-at-several-angles-from-alpha-particles-on-27al-a-script)
  - [16.9 All the neutron spectra and yields of an (x,n) reaction: exclusive, inclusive and combined](#169-all-the-neutron-spectra-and-yields-of-an-xn-reaction-exclusive-inclusive-and-combined)
  - [16.10 Data measured at n\_TOF (CERN): yields, resonance parameters and strength functions](#1610-data-measured-at-n_tof-cern-yields-resonance-parameters-and-strength-functions)
  - [16.11 The n\_TOF data of a table of reactions](#1611-the-n_tof-data-of-a-table-of-reactions)
- [17. More examples for different cases](#17-more-examples-for-different-cases)
  - [17.1 Activation and production cross sections](#171-activation-and-production-cross-sections)
  - [17.2 Neutron multiplicity](#172-neutron-multiplicity)
  - [17.3 Working with the data](#173-working-with-the-data)
  - [17.4 A routine that works for any case](#174-a-routine-that-works-for-any-case)
- [18. Further examples: isotope production, dosimetry, tables and figures](#18-further-examples-isotope-production-dosimetry-tables-and-figures)
  - [18.1 Isotope production for nuclear medicine](#181-isotope-production-for-nuclear-medicine)
  - [18.2 Neutron dosimetry, capture and total cross sections](#182-neutron-dosimetry-capture-and-total-cross-sections)
  - [18.3 Cumulative and independent yields](#183-cumulative-and-independent-yields)
  - [18.4 Tables from the data](#184-tables-from-the-data)
  - [18.5 Figures](#185-figures)
- [19. Changes from version 1](#19-changes-from-version-1)
  - [Changes in version 2.2 and 1.2](#changes-in-version-22-and-12)
  - [Changes in version 2.1](#changes-in-version-21)

## 1. Purpose

`exfor_retrieve.py` retrieves EXFOR data sets for nuclear reactions induced on one target isotope by the projectiles you choose: neutrons, protons, deuterons, tritons, 3He, alpha particles, photons, electrons, pions, kaons, antiprotons, heavy ions, or all of them. The result is saved as CSV (and optionally JSON) tables that open in Excel or Origin and load directly into Python/pandas.

It is meant for compiling the experimental status of activation or production cross sections for a material, comparing datasets from different laboratories, and preparing input for evaluations and plots. The projectiles are chosen with `--projectiles` (Section 7) and the final product (the residual nucleus) with `--product` (Section 7.6).

A companion program, `exfor_plot.py`, draws the selected data as excitation functions with error bars, either from the files written by `exfor_retrieve.py` or by running the retrieval itself (Section 14).

What the script does not do:

- It does not judge data quality, remove duplicates or correct errors (Section 10).
- It does not plot itself; the companion program exfor\_plot.py does (Section 14), and a short example is in Section 9.
- It does not contact the IAEA web interface, which blocks automated access.
- It selects data by target. Data in which your isotope is the projectile (for example heavy-ion beams in inverse kinematics) are not returned (Section 13).

## 2. How it works

The script scans a local copy of the IAEA EXFOR library, so queries are fast, repeatable and do not load the IAEA web servers.

The IAEA Nuclear Data Section publishes the complete library on GitHub as the repository [exfor\_master](https://github.com/IAEA-NDS/exfor_master), with one text file per EXFOR entry (`exforall/<first three characters>/<entry>.x4`). It is updated daily from the finalised transmissions of the nuclear reaction data centres.

The script:

1. obtains a local copy of this repository (a one-off download of about 1.4 GB);
2. scans all entries for the requested target;
3. parses the bibliographic information and the data tables of the subentries whose projectile you selected, including COMMON blocks and subentries with several reactions;
4. writes a catalogue of datasets and a table with one row per data point.

The data table is written entry by entry while the script runs, so memory use stays low even for very large outputs.

Because the data come from the repository and not from the web interface, very recent submissions, preliminary entries and dictionary updates may appear later than on the website.

**Local or online?** The programs run locally. Every search, catalogue, `--find`, retrieval and plot reads the copy of the repository on your computer; the data are not retrieved from the web each time, and nothing is sent anywhere. The network is used in only three cases:

- The first download of the master files (`git clone`, or a ZIP file if git is missing), about 1.4 GB, once.
- `--update`, which runs `git pull` to bring the copy up to date.
- `--master-info`, which asks GitHub whether a newer snapshot exists. Without a connection it says that GitHub could not be reached and skips only that comparison.

After the first download everything works offline: I ran a retrieval, a plot and `--master-info` with the network blocked, and only the GitHub comparison was skipped. A search takes about 20 seconds to a minute, because it reads the local files. `exfor_plot.py` has no network code of its own; it needs the master files only when it has to retrieve data (Section 14.5), and it uses the saved CSV files otherwise.

## 3. Requirements and installation

Nothing needs installing: copy `exfor_retrieve.py` to any folder and run it.

- **Python** 3.8 or later (tested with 3.12). Only the standard library is used.
- **git** (recommended). If git is not installed, the script downloads a zip archive of the repository instead.
- **Disk space and network:** about 2 GB for the local copy of the repository. An internet connection is needed only the first time and when updating. Output files can be large when many projectiles are selected (Section 7.5).
- **Optional:** pandas and matplotlib, for the examples in Section 9. matplotlib is required by the plotting program `exfor_plot.py` (Section 14), which also needs `exfor_retrieve.py` in the same folder, with the same build date (`--version`); `exfor_plot.py` checks this when it starts (Section 11).

On the first run the script clones the repository into the folder of the master files (30 seconds to a few minutes). Later runs reuse that folder. The folder is the one that `--master` gives; without it, the constant `MASTER_DEFAULT` at the top of `exfor_retrieve.py` or the environment variable `EXFOR_MASTER` if they point to an existing folder, and otherwise a folder called `exfor_master` in the folder where you run the command (see "Which folder do the programs use?" below).

**Which folder do the programs use?** The one that `--master` gives. Without it, the constant `MASTER_DEFAULT` at the top of `exfor_retrieve.py` (empty in the repository; write the path of your folder there if you want a permanent default), then the environment variable `EXFOR_MASTER`, when they point to an existing folder. When neither does, a folder called `exfor_master` in the folder where you run the command, not next to the script. The folder must contain a subfolder `exforall` (the entry files). Both `exfor_retrieve.py` and `exfor_plot.py` use the same default. The consequences:

- If you run a program from another folder, it looks for `exfor_master` there and, if it is not there, downloads a new copy of about 1.4 GB into that folder.
- To use another copy than the default one, give its path: `python exfor_retrieve.py --master /path/to/exfor_master --target Nb-93 ...`. The same option exists in `exfor_plot.py`.
- `python exfor_retrieve.py --master-info` prints the full path of the folder it found on its first line, so you can always check which copy is used (Section 3.2).
- The output folders follow the same rule: `data/` and `plots/` are created in the folder where you run the command, unless you change them with `--out` and `--data-dir` (Sections 6 and 14.3).

For example, with the scripts in `~/tools` and the master files in `~/exfor_master`, running from your project folder:

```bash
cd ~/myproject
python ~/tools/exfor_retrieve.py --master ~/exfor_master --target Nb-93 --projectiles d --quantity SIG
```

The data are written to `~/myproject/data/Nb-93/`, and the master files are the ones in `~/exfor_master`. Without `--master` the programs use the default folder of the installation (`MASTER_DEFAULT`), and if that does not exist a new `exfor_master` would be downloaded into `~/myproject`.

### 3.1 Downloading the EXFOR master files

**Where they come from.** The IAEA Nuclear Data Section publishes the library as the GitHub repository [IAEA-NDS/exfor\_master](https://github.com/IAEA-NDS/exfor_master). An automated workflow runs every day at 13:00 UTC and, when new finalised transmissions from the nuclear reaction data centres are available, updates the entries; when there is nothing new it makes no data commit. Dictionary transmissions are not processed. Each update is tagged `Backup-YYYY-MM-DD` and published as a GitHub release.

**Download.** The programs download the files themselves at the first retrieval. To do it by hand, put the repository in a folder called `exfor_master` (or any folder, and give it with `--master`):

```bash
# the current snapshot only (about 1.4 GB), as the programs do
git clone --depth 1 https://github.com/IAEA-NDS/exfor_master.git

# the complete repository with its whole history (larger)
git clone https://github.com/IAEA-NDS/exfor_master.git
```

Without git, use the green Code button on the repository page and choose Download ZIP, unzip it and give the unzipped folder to `--master` (it must contain the subfolder `exforall`). A copy obtained this way cannot be updated with git and cannot be compared with GitHub. Older snapshots are available from the [releases page](https://github.com/IAEA-NDS/exfor_master/releases), by the date in the tag.

**Shallow or complete clone?** Both give you the same current data.

|  | `git clone --depth 1` | `git clone` (complete) |
| --- | --- | --- |
| Entries | All of them, in their latest version | All of them, in their latest version |
| History (earlier versions) | None: one commit | All commits since the repository was created |
| Size (measured) | 1.4 GB: 1.2 GB of entry files and 274 MB of git data | Larger (the history holds every earlier version and 601 tagged snapshots); size not measured |
| Updating with `git pull` | Works | Works |

The programs need only the current files, so the shallow clone (`--depth 1`, what the program makes) is enough. A complete clone is useful only to see the history of an entry. You can add the history later in the same folder with `git fetch --unshallow`.

**An older snapshot.** Every published snapshot has a tag `Backup-YYYY-MM-DD`. To work with the data of a given date, for example to reproduce an old result, clone that tag into its own folder and point the programs to it:

```bash
git clone --depth 1 --branch Backup-2026-08-27 https://github.com/IAEA-NDS/exfor_master.git exfor_master_2026-08-27
python exfor_retrieve.py --master exfor_master_2026-08-27 --target Nb-93 --projectiles d --quantity SIG
```

This is standard git syntax; I did not download a tagged snapshot to test it. The tags available can be listed with `git ls-remote --tags https://github.com/IAEA-NDS/exfor_master.git "Backup-*"`. The retrieval prints the date of the data, so you can confirm which snapshot you used. Releases are also listed on the GitHub releases page.

### 3.2 Updating and checking the EXFOR master files: step by step

The programs search a local copy of the repository `exfor_master`; they do not update it by themselves. Downloading the files and the choice of clone are in Section 3.1; this is the routine for checking the copy and keeping it up to date.

**1. See what you have.**

```bash
python exfor_retrieve.py --master-info
```

```text
EXFOR master files: /your/folder/exfor_master
  entries                : 27108
  entry files in exforall: 27108 (every listed entry is present)
  latest data update     : 2026-09-28 (latest date in entry_updatedate.dat)
  local git commit       : d2af85eca4  2026-09-28 20:18:12 +0000
  GitHub latest commit   : the same: your copy is up to date
  latest backup releases : Backup-2026-09-28, Backup-2026-09-08, Backup-2026-08-27
```

Read three lines: `latest data update` (the date of your data), `GitHub latest commit` (the same, or a newer snapshot exists) and `entry files in exforall` (every listed entry is present, or a warning that the copy is incomplete). If it says `git information: not available`, your copy is not a git clone and cannot be updated with git (step 4). The first line of the answer is the full path of the folder that was used; if it is not the copy you expected, you ran the command from another folder (Section 3) or need \`--master\`.

| Line | Meaning |
| --- | --- |
| `entries`, `entry files in exforall` | The number of entries listed in `entry_updatedate.dat` and the number of entry files found. If listed entries have no file, the program prints a warning: the copy is incomplete and should be updated or downloaded again. |
| `latest data update` | The most recent date at which an entry was changed, taken from the file `entry_updatedate.dat` of the repository. This is the date of the data. |
| `local git commit` | The commit of your copy and its date. It can be later than the data update, because the workflow also commits the update-date file itself. |
| `GitHub latest commit` | Compared with your copy. If they differ, the program says that a newer snapshot exists and how to update. If GitHub cannot be reached it says so and skips the comparison. |
| `latest backup releases` | The three most recent `Backup-` releases on GitHub, that is, the dates of the latest published snapshots. |

The same can be read with plain git: `git -C exfor_master log -1 --format="%H %cd"` (your commit and its date), `git ls-remote origin refs/heads/main` (the latest commit on GitHub: compare the two hashes) and `git ls-remote --tags origin "Backup-*"` (the dates of the snapshots). Every retrieval also prints the date of the data it used, for example `Scanned 27108 EXFOR entries (master files of 2026-09-28)`. Quote that date, and the commit, when you publish results (Section 12).

In the snapshot used for the tests the latest releases were on 28 September, 8 September and 27 August 2026, and the local copy was identical to the GitHub copy. The data of a release can be earlier than the entries on the IAEA web interface, which may show very recent submissions first (Section 2).

**2. Update.**

```bash
python exfor_retrieve.py --update --master-info
```

This runs `git pull` in the folder and shows the date of the data afterwards. The same effect as `git -C exfor_master pull origin main`. You can also add `--update` to any retrieval. Update before starting a new analysis and when `--master-info` reports a newer snapshot. The repository changes only when new finalised transmissions arrive (in the snapshot used for the tests the latest releases were on 28 September, 8 September and 27 August 2026), so there is no need to update every day.

**3. Note the date.** Every retrieval prints `master files of 2026-09-28`. Write that date, and if you want the commit (`git -C exfor_master log -1 --format=%H`), in your report, so that the result can be reproduced (Section 12).

**4. If the update is skipped.** The message `--update skipped` means that the folder is not a git clone, or that git is not installed. Install git, rename or delete the folder and run the program again so that it clones the files, or clone them yourself: `git clone --depth 1 https://github.com/IAEA-NDS/exfor_master.git`. The details follow.

**If you see `--update skipped`.** The message `--update skipped: the folder ... is not a git clone` (older versions: `--update needs a git clone; skipping`) means that the `exfor_master` folder was not obtained with git, so it cannot be updated with `git pull`. Typical causes:

- The files were downloaded as a ZIP file, by hand or by the program itself when git was not installed at the first run (the program then says that the copy cannot be updated).
- The folder was copied without its hidden `.git` subfolder.
- git is not installed or is not found. The message says so (`git was not found`).

The data are not damaged: the copy simply cannot be updated. `python exfor_retrieve.py --master-info` shows the date of its data. To enable updates:

```bash
# macOS: if git is missing, this offers to install the command line tools
git --version

# then rename or delete the old folder and let the program clone it, or clone it yourself
mv exfor_master exfor_master_old
git clone --depth 1 https://github.com/IAEA-NDS/exfor_master.git
```

On Windows install git from git-scm.com, on Linux with your package manager. Without git you can still update by downloading a fresh ZIP file (Section 3.1) and unzipping it over the folder. Check which folder is used with `--master-info`: the default is the folder `MASTER_DEFAULT` if it exists, and otherwise `exfor_master` relative to the folder where you run the command, so running from another folder may use another copy; give the folder with `--master`.

**Is the shallow copy complete?** Yes for the current data. In the test, the copy had 27,108 entry files, exactly the 27,108 entries that the repository lists, with none missing and none empty, and it was the latest commit of GitHub. `--master-info` repeats the check of the entry count every time you run it. What "complete" does not mean:

- It is the state of the repository on the day you cloned or updated. New entries need an update (step 2).
- The repository is built from finalised transmissions, so it can lag behind the IAEA web interface for very recent submissions (Section 2). EXFOR dictionary transmissions are not processed. To check an entry in doubt, look it up by its number on the IAEA interface and compare it with `exforall/<first three characters>/<entry>.x4`.

## 4. Quick start

**First, check what EXFOR has.** Before retrieving anything, ask for the catalogue of your target. It shows the projectiles, quantities and products with data, how many entries, datasets and points there are, the energy range and the years (Section 5):

```bash
python exfor_retrieve.py --target Nb-93 --available
```

If you do not know the target, `python exfor_retrieve.py --find --projectiles d --product Nb-92m` lists the targets that have such data. For the publications behind the data you use, add `--references` to the retrieval or to the plotting command (Section 5.3). To see the date of the EXFOR data you are using and whether GitHub has a newer snapshot, run `python exfor_retrieve.py --master-info`; `--update` brings your copy up to date (Section 3.2). To save every dataset as a plain text file in columns, with the units in the first row, add --ascii to the retrieval or to the plotting command (Sections 8.6 and 9.8). To print the half-life of each isotope next to it, with stable isotopes marked stable, add --halflife (Section 10.2).

One command retrieves the data; a typical search takes 20 seconds to a minute because every entry of the library is scanned.

Everything for niobium-93 induced by deuterons, protons, 3He and alphas (the default selection):

```bash
python exfor_retrieve.py --target Nb-93
```

Deuteron cross sections only (the files go to the folder `data/Nb-93/`):

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG
```

The output of the second command (repository snapshot of October 2026; the numbers grow as EXFOR does):

```text
Scanned 27108 EXFOR entries: 790 contain 41-NB-93 as target (projectiles requested: d).

Target 41-NB-93: 60 datasets, 441 data points
projectile   code      datasets  entries    points products
d            D               60       11       441       37

Points by quantity (top): SIG: 441
Points by product (top): 93mMo: 120, 92mNb: 89, 89Zr: 35, 90mY: 30, 94mNb: 23, 90Nb: 17, 91mNb: 15, 89gZr: 12

Files written to /your/folder/data/Nb-93:
  EXFOR_NB-93_data.csv
  EXFOR_NB-93_datasets.csv
```

To see which projectiles have data for a target without writing any file:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles all --summary-only
```

On Windows use `py exfor_retrieve.py ...` if `python` is not found.

To plot the data you just retrieved (Section 14), keep `exfor_plot.py` next to `exfor_retrieve.py` and run:

```bash
python exfor_plot.py --data data/Nb-93 --product 92mNb,89Zr,90Nb
```

The plots are written to a folder named after the target (here `plots/Nb-93/`), one file per projectile and product.

## 5. What is available in EXFOR, and the list of references

This chapter answers two questions that come before and after the retrieval: what does EXFOR have for my target, projectile and product, and which publications are behind the data that I use? The numbers come from the EXFOR snapshot used for the tests (October 2026) and will change as EXFOR grows. All commands were run on that snapshot.

### 5.1 What EXFOR has for a target

The option `--available` of `exfor_retrieve.py` reads the entries of the target and prints what is there, without writing the data. Projectiles default to all, so that nothing is hidden. For 93Nb:

```bash
python exfor_retrieve.py --target Nb-93 --available
```

The output starts with the totals and a table by projectile:

```text
What EXFOR has for Nb-93 (projectiles all, product all, quantity ALL): 543 entries, 2339 datasets, 140285 data points.

By projectile:
projectile  entries  datasets  points
----------  -------  --------  ------
n           325      851        86100
p           86       509         9643
d           23       91          1917
t           2        3            240
3He         8        69          1001
alpha       41       258         3252
gamma       24       69           976
...
```

Then comes the catalogue, with one row for each combination of projectile, quantity and product: the number of entries, datasets and points, the incident-energy range and the years of the publications. Projectiles are listed in the usual order (n, p, d, t, 3He, alpha, gamma, then heavy ions), and within a projectile the cross sections (SIG) come first. Restricting it to one projectile and cross sections:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --available
```

```text
projectile  quantity  product    entries  datasets  points  E_min  E_max  years
d           SIG       93mMo            5         5     120   0.02   48.3  2000-2018
d           SIG       92mNb            4         4      89   0.02   48.3  2007-2018
d           SIG       ELEM/MASS        2         7      54    226   7300  1986-2019
d           SIG       89Zr             2         2      33   0.02   48.3  2007-2016
d           SIG       90mY             3         3      30   0.02   48.3  2007-2016
...
```

The product `ELEM/MASS` is a table in which the product is given row by row (Section 7.6). The table is also written as `data/Nb-93/EXFOR_NB-93_catalogue.csv`, with all rows (the screen shows `--max-rows` rows, 100 by default). Use `--summary-only` to print without writing the file.

**Which entries?** `--available entries` gives one row for each EXFOR entry, with author, year, reference, what it contains and the energy range. The entries with 92mNb from deuterons on 93Nb:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --product Nb-92m --available entries
```

```text
entry  author            year  reference                                projectiles  quantities  products  points  E_min  E_max
A0294  I.O.Konstantinov  1986  Sov. At. Energy 60 (1986) 390            d            TTY         1         25      7.4    22.2
D4156  F.Tarkanyi        2007  Nucl. Instrum. Methods B 255 (2007) 297  d            SIG         1         43      0.02   38.24
D0713  M.Avrigeanu       2013  Phys. Rev. C 88 (2013) 014612            d            SIG         1         25      3.43   19.35
D4344  F.Ditroi          2016  Nucl. Instrum. Methods B 373 (2016) 17   d            SIG         1         9       30.9   48.3
E2589  M.Aikawa          2018  Nucl. Instrum. Methods B 436 (2018) 217  d            SIG         1         12      10.2   22.7
A0194  P.P.Dmitriev      1983  Report INDC(CCP)-210 (1983)              d            TTY         1         1       22     22
```

This shows at a glance that the cross sections come from four entries and that two more entries (A0294 and A0194) give thick-target yields (TTY), which are other quantities. The entry numbers can be used with `--entries` in `exfor_plot.py`.

**Check before you retrieve, check after you plot.** A practical order is: `--available` (is there anything?), then `--summary-only` with your selection (how much?), then the retrieval, then `exfor_plot.py --list` (what will be drawn?). The IAEA web interface of EXFOR can be used to cross-check an entry by its number; the programs read the same library but cannot access that website.

### 5.2 Which targets have data? (search over all targets)

When you know the projectile and the product but not the target, `--find` scans the whole library and lists the targets that have such data. It reads only the reaction fields of the entries, so it is fast (about 10 seconds):

```bash
python exfor_retrieve.py --find --projectiles d --product Nb-92m --quantity SIG
```

```text
target  entries  datasets  points~  year_min  year_max
------  -------  --------  -------  --------  --------
Zr-nat  4        4              82      1991      2021
Nb-93   4        4              89      2007      2018
Mo-nat  3        3             112      1999      2012
Mo-94   1        1              16      1977      1977
```

So 92mNb is made from deuterons on natural zirconium, 93Nb, natural molybdenum and 94Mo. The number of points is approximate (taken from the headers of the data tables) and energy limits are not applied. The table is written to `data/EXFOR_find_<selection>.csv`.

`--target` limits the search to an element: `"Nb-*"` means every isotope of niobium, and a single isotope or `Ti-nat` is also accepted. Projectiles default to all in this mode.

```bash
python exfor_retrieve.py --find --target "Cu-*" --projectiles p --quantity SIG
```

This lists the copper targets with proton cross sections: natural copper (133 entries), 63Cu (54), 65Cu (69), and a few neutron-rich isotopes with one or two entries each. Products with a table-coded product (fission fragments) are not matched when `--product` is given, because the product is not in the reaction field.

### 5.3 The list of references of the datasets

For a publication or a report you need the references of the datasets you used. `--references` writes them, in `exfor_retrieve.py` for the datasets retrieved and in `exfor_plot.py` for the datasets that are plotted. The files have the same names in both programs and the prefix of the data or of the plots:

| File | Content |
| --- | --- |
| `<prefix>_references.txt` | Numbered citations, with title, DOI, EXFOR entry and the data used (default) |
| `<prefix>_references.bib` | The same in BibTeX, ready for LaTeX (default) |
| `<prefix>_references.csv` | A table with authors, year, citation, reference code, DOI, title, institute, projectiles, products, quantities, energy range and number of points |

The formats are chosen with `--ref-format txt,bib,csv`, and the number of authors with `--ref-authors` (all authors if there are at most 3, otherwise the first author and "et al."; 0 writes all authors).

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m --references
python exfor_plot.py --data data/Nb-93 --projectiles d --product 92mNb --references
```

The first command writes `data/Nb-93/EXFOR_NB-93_references.txt` and `.bib` next to the data. The second writes `plots/Nb-93/Nb-93_references.txt` and `.bib` next to the plots, with only the datasets that are drawn (after the filters such as `--entries`, `--exclude-status` or `--emax`). The text file for the four entries above begins:

```text
References of the EXFOR datasets used in the plots of Nb-93 (projectiles d, product 92mNb, quantity SIG)
4 EXFOR entries. Generated from the bibliographic fields of EXFOR; check each reference against the original publication before citing it.

[1] F. Tarkanyi et al., Nucl. Instrum. Methods B 255 (2007) 297.
    Title: Production of longer lived radionuclides in deuteron induced reactions on niobium
    EXFOR entry D4156
    Data used: d -> 92mNb [SIG]; 0.02-38.24 MeV; 43 points

[2] M. Avrigeanu et al., Phys. Rev. C 88 (2013) 014612.
    Title: Low-energy deuteron-induced reactions on 93Nb
    EXFOR entry D0713
    Data used: d -> 92mNb [SIG]; 3.43-19.35 MeV; 25 points

[3] F. Ditroi et al., Nucl. Instrum. Methods B 373 (2016) 17.
    Title: Activation cross sections of deuteron induced reactions on niobium in the 30-50 MeV energy range
    EXFOR entry D4344   DOI: 10.1016/j.nimb.2016.02.037
    Data used: d -> 92mNb [SIG]; 30.9-48.3 MeV; 9 points
```

The BibTeX entry of the first reference starts `@article{Tarkanyi2007_D4156, author = {...}, title = {{...}}, year = {2007}, journal = {Nucl. Instrum. Methods B}, volume = {255}, pages = {297}, note = {EXFOR entry D4156; data used: ...}}`. The key is the first author, the year and the EXFOR entry.

**How the references are made, and what to check.**

- They are built from the bibliographic fields of the EXFOR entry (authors, title, reference code, DOI), not from the publisher. Check each reference against the original publication before citing it.
- Author names in EXFOR have no accents (Tarkanyi, Ditroi). EXFOR gives the journal as a code; about 50 common journals are written in full (for example `PR/C` as Phys. Rev. C, `NIM/B` as Nucl. Instrum. Methods B, `ARI` as Appl. Radiat. Isot.) and the others are printed as the code. Reports, conferences, theses and private communications are written as `Report ...`, `Conference ...` and so on.
- The title and the DOI come from the datasets file (`*_datasets.csv`). With `exfor_plot.py --data` the file next to the data file is used; if it is missing, or comes from an older version (without the author list), the program says so and the reference has only the first author with "et al.", the year and the reference code.
- An entry that was measured by one group but appears several times (for example with several subentries) gives one reference.
- Datasets that EXFOR marks as superseded (SPSDD) are still listed if you plot them; use `--exclude-status SPSDD` to leave them out of both the plots and the references (an example follows this list; which status codes to exclude is in Section 10.1).

**Example: the data and the references with and without the superseded data.** The 99mTc produced by protons on 100Mo, run twice into separate folders so that both results are kept. The first command keeps everything; the second leaves out the superseded data. Each command retrieves the data, plots them, writes one ASCII file for each dataset and writes the list of references:

```bash
# 1. with the superseded data
python exfor_plot.py --target Mo-100 --projectiles p --product Tc-99m \
    --ascii --references --data-dir data_all --out plots_all

# 2. without the superseded data
python exfor_plot.py --target Mo-100 --projectiles p --product Tc-99m --exclude-status SPSDD \
    --ascii --references --data-dir data_final --out plots_final
```

The messages of the two commands show the difference:

```text
1.  Scanned 27108 EXFOR entries (master files of 2026-09-28): 233 contain 42-MO-100 as target.
      ASCII files: 15 files (dataset format) for Mo-100 written to data_all/Mo-100/ascii (with index.csv)
    382 points in 1 plots from 12 EXFOR entries, 1 target(s).
      references: 12 EXFOR entries for Mo-100

2.    ASCII files: 14 files (dataset format) for Mo-100 written to data_final/Mo-100/ascii (with index.csv)
    358 points in 1 plots from 11 EXFOR entries, 1 target(s).
      references: 11 EXFOR entries for Mo-100
```

The files of each run are in its own folders: the plot `plots_*/Mo-100/Mo-100_p_99mTc.png`, the references `plots_*/Mo-100/Mo-100_references.txt` and `.bib` (12 BibTeX entries in the first, 11 in the second), the ASCII files and `index.csv` in `data_*/Mo-100/ascii/`, and the saved data and datasets files `data_*/Mo-100/EXFOR_MO-100_data.csv` and `..._datasets.csv`. The data file of both runs has all 382 points; the filter acts on the plot, the ASCII files and the references.

**What the filter removed.** The difference of the two reference lists (`diff plots_all/Mo-100/Mo-100_references.txt plots_final/Mo-100/Mo-100_references.txt`) is one reference, the others only change their number:

```text
[4] S. Takacs et al., J. Radioanal. Nucl. Chem. 257 (2003) 195.
    Title: Evaluation of proton induced reactions on 100Mo: New cross sections for production of 99mTc and 99Mo
    EXFOR entry D4115
    Data used: p -> 99mTc [SIG]; 5.7-37.9 MeV; 24 points
```

It is the dataset of subentry D4115002, which the datasets file marks as superseded and points to its replacement:

```text
D4115 002 S.Takacs 2003 43-TC-99-M 24 pts | TABLE,APRVD,SPSDD,SPSDD | SPSDD>D4322005;SPSDD>D4322004
```

The replacement, entry D4322 (S. Takacs et al., Nucl. Instrum. Methods B 347 (2015) 26, "Reexamination of cross sections of the 100Mo(p,2n)99mTc reaction", DOI 10.1016/j.nimb.2015.01.056), is in both reference lists and both sets of ASCII files (two datasets, 34 and 23 points, 8.38 to 37.9 MeV), so very little is lost: the new data cover 8.38 to 37.9 MeV, and the old dataset had only one more point, at 5.7 MeV, below that range (seven other entries of the selection have points below 8.38 MeV). The check that you can always make is to compare the energy ranges in the datasets file, or the plots of the two runs. The first run has the file `Mo-100_p_99mTc_SIG_Takacs2003_D4115-002.dat` in `data_all/Mo-100/ascii/`, the second does not.

**Only the retrieval, without plots.** `exfor_retrieve.py --target Mo-100 --projectiles p --product Tc-99m --ascii --references` writes the data, the ASCII files and the references in one step too, but it has no status filter, so the files contain the superseded data (the result of the first command above, without the plot). To get the second result use `exfor_plot.py` as above, or take the datasets and the references from the first result and remove the superseded ones with the `status` column of the datasets file.

When to exclude superseded data, which other status codes there are, and why `DEP` should not be excluded as a rule, is in Section 10.1.

### 5.4 A routine from the question to the references

1. What is there: `python exfor_retrieve.py --target X --available`, or `--find` if the target is not known.
2. Choose: add `--projectiles`, `--product` and `--quantity` to `--available entries` and note the entries you want.
3. Retrieve and plot: `python exfor_plot.py --target X --projectiles ... --product ... --exclude-status SPSDD --references`.
4. Keep from the plot folder: the figures, and `X_references.txt` and `X_references.bib` for the bibliography.

### 5.5 Changes in the data and datasets files

The datasets file has a new column `authors` (the full author list as in EXFOR), after `first_author`. The `year` column is now also filled for entries whose reference gives the date as year and month (for example `199203`) or as YYMM, which were empty before. Both changes are additive: existing files keep working, but references made from a datasets file of an older version show only the first author with "et al.".

The data file has two more columns at the end: `dataset`, an identifier of the dataset (the subentry and the number of the reaction record, for example `D4156003.0.0`; the points of one dataset have the same value), and `extra_units`, a JSON text with the EXFOR unit of each column kept in `extra`. They are used by `--ascii` to give every variable its unit and to write a dataset whose products are given row by row as one file (Section 8.6). The datasets file also has `dataset`. Files from older versions work without them, with the limits listed in Section 8.6.

### 5.6 Quick reference: checking the data and getting the references

All the commands of this chapter in one place. Each was run on the EXFOR snapshot used for the tests.

**Check what EXFOR has**

```bash
# everything EXFOR has for a target: projectiles, quantities, products, entries, energy ranges, years
python exfor_retrieve.py --target Nb-93 --available

# narrow it down: deuterons, cross sections only
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --available

# the list of EXFOR entries (author, year, reference, energy range)
python exfor_retrieve.py --target Nb-93 --projectiles d --product Nb-92m --available entries

# you do not know the target: which targets have such data?
python exfor_retrieve.py --find --projectiles d --product Nb-92m

# the same for one element only (every isotope of copper, proton cross sections)
python exfor_retrieve.py --find --target "Cu-*" --projectiles p --quantity SIG

# print only, write no CSV file, and show more or fewer rows on the screen
python exfor_retrieve.py --target Nb-93 --available --summary-only --max-rows 20
```

| What you see | Where it is saved |
| --- | --- |
| Catalogue (`--available`) | `data/<target>/EXFOR_<target>_catalogue.csv`, all rows |
| Entry list (`--available entries`) | `data/<target>/EXFOR_<target>_entries.csv`, all rows |
| Search over targets (`--find`) | `data/EXFOR_find_<selection>.csv`, all rows |

With `--summary-only` nothing is written. In these modes the projectiles default to all, so that nothing is hidden; the screen shows 100 rows unless you change `--max-rows`. Without the product and quantity filters the catalogue of a busy target is long (for 93Nb, 733 rows: 180 for protons, 81 for alphas, 80 for neutrons, 54 for deuterons, and the rest for other projectiles and heavy ions), so narrow it with `--projectiles`, `--product` and `--quantity`.

**Check what will be drawn**

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product 92mNb --list
```

**Check which EXFOR data you are using**

```bash
# date of the latest data update, git commit, and is there a newer snapshot on GitHub?
python exfor_retrieve.py --master-info

# bring the local copy up to the latest snapshot, then show its date
python exfor_retrieve.py --update --master-info
```

Example of the answer: `latest data update: 2026-09-28`, `GitHub latest commit: the same: your copy is up to date`. Every retrieval also prints the date of the data it used. Quote that date when you publish results (Section 3.2).

**Get the references**

```bash
# references of the datasets that you retrieve, next to the data
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m --references

# references of only the datasets that are plotted, next to the plots
python exfor_plot.py --data data/Nb-93 --projectiles d --product 92mNb --references

# also a CSV table, and all the authors written out
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m \
    --references --ref-format txt,bib,csv --ref-authors 0
```

| File | Content |
| --- | --- |
| `<prefix>_references.txt` | Numbered citations with title, DOI, EXFOR entry and the data used |
| `<prefix>_references.bib` | The same in BibTeX |
| `<prefix>_references.csv` | With `--ref-format ...,csv`: a table for a spreadsheet |

The files are written to `data/Nb-93/` (retrieval script) or to `plots/Nb-93/` (plot program). In `exfor_plot.py --data`, keep the `*_datasets.csv` file next to the data file: the titles and DOIs come from it.

**Before you cite.** The references are built from the bibliographic fields of EXFOR, not from the publishers. Author names have no accents, titles are EXFOR's wording, and journals that are not among the common ones appear as EXFOR codes. Check each reference against the original paper.

**If a command is not recognised.** The message `unrecognized arguments: --available` (or `--find`, `--references`, `--max-rows`) means that you are running an older script. Replace both `exfor_retrieve.py` and `exfor_plot.py` with the current versions (they must be in the same folder) and check them with `python exfor_retrieve.py --version`: the current version prints a build date. The same applies if `--available` complains that `--target` is missing: use `--find` to search without a target.

**An error that names a missing attribute or function, or the message "needs the matching exfor\_retrieve.py".** The two scripts use each other (`exfor_plot.py` imports `exfor_retrieve.py`), so they must have the same build date. A traceback such as `AttributeError: 'AsciiWriter' object has no attribute 'no_unc'` means that `exfor_plot.py` is newer than the `exfor_retrieve.py` next to it. `exfor_plot.py` 1.2 checks this when it starts and stops with a message that names the older file it found (its version, build date and path); replace both scripts with the current pair and check that `python exfor_retrieve.py --version` and `python exfor_plot.py --version` print the same build date. A copy of `exfor_retrieve.py` in another folder that comes first in the Python path can also be the one that is found; the message gives its path.

## 6. Command-line reference

Only `--target` is required; every other option has a default.

| Option | Default | Meaning |
| --- | --- | --- |
| `--target` | (required, except with `--find` and `--master-info`) | Target isotope. Accepted forms: Nb-93, 93Nb, NB93, 41-NB-93 (EXFOR style); natural composition: Ti-nat, natTi, Ti-0. |
| `--projectiles` | d,p,he3,a (all with `--available` and `--find`) | Projectiles to retrieve: `all`, or a string with a subset (particle names, heavy ions, groups, exclusions). Full syntax in Section 7. |
| `--list-projectiles` |  | Print all accepted projectile names and exit. |
| `--product` | all | Final product(s) to keep: `all`, or a string with a subset (nuclides with or without a state, element wildcards, particles, the groups heavy and residual, `none`, exclusions). Full syntax in Section 7.6. |
| `--product-exact` | off | Match EXFOR product codes exactly as written: `41-NB-92` then selects only data with no state given. |
| `--quantity` | ALL | EXFOR quantity code(s) to keep, for example SIG or SIG,DA. The match is exact: SIG does not return SIG/RAT. ALL keeps every quantity. |
| `--emin`, `--emax` | none | Lower and upper limits of the incident energy in MeV (total projectile energy). Points without an incident energy are kept. |
| --facility | none | Only the entries measured at a facility: ntof (n\_TOF at CERN), gelina, or a regular expression searched in the FACILITY and INSTITUTE fields. Without --target (or with --target all) every target of those entries is retrieved, one folder each. Section 16.10. |
| `--available` | off | Show what EXFOR has for the target without retrieving the data: `catalogue` (the default) gives one row per projectile, quantity and product; `entries` gives one row per EXFOR entry. The table is also written as a CSV file (Section 5.1). |
| `--find` | off | Search all targets: which targets have data for the projectiles, product and quantity given? `--target` can limit it to an element, for example `"Nb-*"` (Section 5.2). |
| `--max-rows` | 100 | Maximum number of rows printed by `--available` and `--find`; the CSV files have all rows. |
| `--references` | off | Also write the list of references of the retrieved datasets: `<prefix>_references.txt`, `.bib` and `.csv` (Section 5.3). |
| `--ref-format` | txt,bib | Formats of the reference list: `txt`, `bib` (BibTeX), `csv`, as a comma list. |
| `--ref-authors` | 3 | Authors written in a reference: all if there are at most this many, otherwise the first one and "et al."; 0 writes all authors. |
| `--ascii` | off | Also write each dataset as its own ASCII file in columns, with the units in the first row, in `<out>/<target>/ascii/`; a 2D distribution is one file with the two variables, the value and its uncertainties, the variable that labels the blocks first. The uncertainties (total, statistical, systematic, and of the incident energy) are in the files when the dataset gives them. Also writes `index.csv` (Sections 8.6, 8.6.3 and 8.6.5). |
| `--ascii-format` | dataset | With `--ascii`: `dataset` (one file for each dataset), `entry` (one file for each EXFOR entry, quantity and unit) or `quantity` (one file for each projectile, process, quantity and unit). The last two make far fewer files, with columns that tell the datasets apart (Section 8.6.2). |
| `--ascii-no-blanks` | off | With `--ascii`: no blank line between the blocks of a 2D file (Section 8.6.3). |
| `--ascii-dir` | `<out>/<target>/ascii` | Folder for the ASCII files. |
| `--ascii-no-errors` | off | With `--ascii`: leave out the uncertainty columns, so that a 2D file has exactly three columns. By default the files have them, also the 2D files, when the dataset gives them (Section 8.6.5). |
| `--max-ascii` | 5000 | Maximum number of ASCII files; the writing stops there and suggests the formats with fewer files. |
| `--summary-only` | off | Parse everything and print the summary (with the list of products), but write no files. Recommended before `--projectiles all`. |
| `--master` | exfor\_master | Folder with the EXFOR master files (it must contain a subfolder `exforall`). The default is `MASTER_DEFAULT` at the top of the script, empty in the repository (or the environment variable `EXFOR_MASTER`), if it points to an existing folder; otherwise the folder `exfor_master` in the folder where you run the command, not next to the script (Section 3). It is downloaded if it does not exist. |
| `--update` | off | Update an existing git clone (git pull) before searching, and print the date of the data after the update (Section 3.2). |
| `--master-info` | off | Print the date of the latest data update of the master files, their git commit, and whether GitHub has a newer snapshot; then exit. Combine with `--update` to update first (Section 3.2). |
| `--out` | data | Parent folder: the files of each target go to `<out>/<target name>/`, for example `data/Nb-93/` (default `data`). Created if needed. |
| `--prefix` | EXFOR\_\<target> | Prefix of the output files, for example `--prefix nb93_d`. |
| `--json` | off | Also write `<prefix>_datasets.json` and `<prefix>_data.jsonl` (one JSON object per data point per line). |
| `--jobs` | min(8, cores) | Number of processes used for the scan. |
| --halflife | off | Print the NUBASE2020 half-life next to each isotope (the target and the products) in the summaries, the catalogue and the target search, and write it in the datasets file and in the ASCII index (Section 10.2). --halflife-db also switches it on. |
| --halflife-db | see Section 10.2 | SQLite database of NUBASE2020 half-lives (nuclear\_halflives.db). Default: the constant HALFLIFE\_DB\_DEFAULT in the script (empty in the repository), then the variable EXFOR\_HALFLIFE\_DB, then the file nuclear\_halflives.db next to the script. Giving it also switches --halflife on (Section 10.2). |
| --check-halflives | off | Compare the half-lives assigned to the EXFOR states with the half-lives quoted in the DECAY-DATA fields of all entries (about a minute), print the agreement by state and exit (Section 10.2). |
| `--version`, `-h` |  | Show the version (with the date of the last change) or the built-in help. |

## 7. Selecting projectiles and products

`--projectiles` takes one string: `all`, or any subset of particles. Names are not case sensitive.

### 7.1 The --projectiles string

Write a list of items separated by commas (spaces or semicolons also work):

| Item | Meaning | Example |
| --- | --- | --- |
| `all` | Every projectile found in EXFOR, including the case of no projectile (code 0). | `--projectiles all` |
| A particle name | One particle, using any spelling of Section 7.2. | `n p d t he3 a g e pi+ pi- k+ k- ap 0` |
| A heavy ion | One nuclide used as a projectile: 12C, C-12, C12 or 6-C-12. With a level or isomer suffix (18F-L) only that code is selected; without a suffix the ground code and its -M/-L codes are selected. | `12C,16O` or `Ne-20` |
| An element wildcard | Every isotope of an element used as a projectile (heavy-ion codes only): `C-*` or `Ne*`. | `Ne-*` |
| A group | light, neutral, mesons, exotic, heavy-ions (aliases hi, ions); see Section 7.4. | `light,heavy-ions` |
| An exclusion | `-` or `!` in front of an item removes it. Exclusions are applied after the inclusions. If there are only exclusions, everything else is selected. | `all,-n,-g` |

Complete examples:

| String | Result |
| --- | --- |
| `d,p,he3,a` | The default: deuterons, protons, 3He and alphas. |
| `d` | Only deuterons. |
| `d p 3He` | Deuterons, protons and 3He (quotes needed with spaces: `--projectiles "d p 3He"`). |
| `n,g` | Neutrons and photons. |
| `light` | p, d, t, 3He and alpha. |
| `all` | Everything. |
| `all,-n` | Everything except neutrons (neutron data are usually most of the points). |
| `all,-n,-g` | Everything except neutrons and photons. |
| `12C,16O,Ne-*` | Carbon-12, oxygen-16 and every neon projectile. |
| `heavy-ions,-12C` | All heavy ions except carbon-12. |
| `pi+,pi-,k+,k-,ap` | Pions, kaons and antiprotons. |

If the string starts with a minus sign, write the option with an equals sign (`--projectiles=-n` or `--projectiles=all,-n`); otherwise the command line parser takes it for another option. An unknown name stops the script with a message that points to `--list-projectiles`. A name for a projectile that has no data for your target simply gives nothing for it.

### 7.2 Particles in EXFOR

The table lists every non-heavy-ion projectile code found in the library, with the spellings the script accepts. Counts are numbers of reaction strings and of entries in the REACTION fields of the whole library, for all targets (snapshot of October 2026). They show how much data to expect and will grow with EXFOR.

| EXFOR code | Label in output | Particle | Accepted spellings (`--projectiles`) | Reactions / entries |
| --- | --- | --- | --- | --- |
| N | n | neutron | n, neutron | 85,085 / 11,532 |
| P | p | proton | p, proton, h1, 1h | 45,895 / 5,044 |
| A | alpha | alpha particle (4He) | a, alpha, he4, 4he | 13,725 / 2,243 |
| D | d | deuteron | d, deuteron, h2, 2h | 13,086 / 2,276 |
| G | gamma | photon | g, gamma, photon | 10,846 / 1,650 |
| HE3 | 3He | helion (3He) | he3, 3he, helion | 4,235 / 824 |
| 0 | none | no incident particle (spontaneous processes, e.g. spontaneous fission) | 0, none, sf, spontaneous | 3,382 / 684 |
| T | t | triton | t, triton, h3, 3h | 1,156 / 233 |
| PIP | pi+ | positive pion | pi+, pip | 216 / 31 |
| PIN | pi- | negative pion | pi-, pin | 156 / 37 |
| E | e | electron | e, electron | 113 / 25 |
| AP | pbar | antiproton | ap, pbar, antiproton | 55 / 8 |
| KN | K- | negative kaon | k-, kn | 16 / 2 |
| KP | K+ | positive kaon | k+, kp | 2 / 2 |
| Z-SYMBOL-A | 12C, 16O, ... | heavy ions (any nuclide from He-6 on) | 12C, C-12, 6-C-12, Ne-\*, heavy-ions | 20,413 / many (Section 7.3) |

A few reactions use other spellings of the same particle (GAMMA in 3 reactions; He3 and p in one each). The script treats them as the standard code and keeps the original spelling in the column `projectile_raw` of the datasets file. Positrons, muons and neutrinos do not appear as projectiles in this snapshot; the EXFOR dictionary may define other codes that no reaction uses at present. `python exfor_retrieve.py --list-projectiles` shows everything the script understands.

### 7.3 Heavy ions

Heavy ions are coded in EXFOR as Z-SYMBOL-A, for example 6-C-12. The library contains 519 different heavy-ion projectile codes, from 2-HE-6 to 92-U-238, covering 65 elements, in about 10% of all reactions. They include radioactive beams (2-HE-6, 2-HE-8, 3-LI-8, 3-LI-11, 4-BE-11, 4-BE-14), natural-composition carbon (6-C-0, label natC), and codes with a level or isomer suffix (9-F-18-L, 13-AL-26-M). Light ions up to 4He use their own codes (P, D, T, HE3, A), never Z-SYMBOL-A.

The most frequent heavy-ion projectiles:

| EXFOR code | Label | Reactions | Entries |
| --- | --- | --- | --- |
| 6-C-12 | 12C | 4,119 | 403 |
| 8-O-16 | 16O | 1,779 | 316 |
| 3-LI-6 | 6Li | 1,280 | 252 |
| 3-LI-7 | 7Li | 1,141 | 241 |
| 7-N-14 | 14N | 996 | 108 |
| 10-NE-20 | 20Ne | 878 | 78 |
| 18-AR-40 | 40Ar | 876 | 63 |
| 79-AU-197 | 197Au | 813 | 10 |
| 8-O-18 | 18O | 552 | 121 |
| 4-BE-9 | 9Be | 395 | 112 |
| 9-F-19 | 19F | 390 | 84 |
| 14-SI-28 | 28Si | 336 | 68 |
| 2-HE-6 | 6He | 273 | 111 |

Energies of heavy ions are often given per nucleon (MEV/A or GEV/A). The script converts them to total laboratory energy with the projectile mass number (Section 8.4).

### 7.4 Groups

| Group | Contents |
| --- | --- |
| light | p, d, t, 3He, alpha |
| neutral | n, gamma |
| mesons | pi+, pi-, K+, K- |
| exotic | pi+, pi-, K+, K-, antiproton, electron |
| heavy-ions (hi, ions) | Every projectile coded as Z-SYMBOL-A |
| all (any, \*) | Every projectile, including no projectile (0) |

### 7.5 How much data to expect

The number of points depends strongly on the projectile, while the search itself takes the same time whatever you select. For 93Nb, deuterons give 1,917 points over all quantities, protons 9,643, neutrons 86,100 and 12C 17,376; all projectiles together give 140,285 points in a CSV file of about 34 MB. For 238U, all projectiles give about 620,000 points, of which 560,000 are neutron data.

Use `--summary-only` to see the numbers first, then restrict with the projectile string, `--quantity` and `--emin`/`--emax` before writing very large files. A table with a million rows opens in pandas but not in Excel (limit about 1,048,000 rows).

### 7.6 Selecting the final product (--product)

`--product` keeps only the reactions that lead to the final nucleus or particle you name; the default is `all`. It works together with `--projectiles` and `--quantity`: `--projectiles d --quantity SIG --product Nb-92m` gives the 93Nb(d,x)92mNb cross sections. Several items are separated by commas, for example `--product Nb-92m,Zr-89,Zr-88`.

| Item | Meaning | Example |
| --- | --- | --- |
| A nuclide without a state | The nuclide in every state: ground, isomers, unspecified state, and combinations such as ratios and sums. Spellings: `Nb-92`, `92Nb`, `41-NB-92`. | `Zr-89` |
| A metastable or ground state | Only that state. Write `m`, `g` or `l` after the mass: `Nb-92m`, `92mNb`, `Nb-92g`, `Nb-92m1`, `Nb-92m2`, or the EXFOR code `41-NB-92-M`. | `Nb-92m` or `92mNb` |
| An element wildcard | Every isotope of the element: `Zr-*` or `Zr*`. A bare symbol such as `Zr` is not accepted. | `Zr-*` |
| Natural element | Products coded with mass 0: `natZr` or `Zr-0`. | `natZr` |
| A light particle | n, p, d, t, he3, a (alpha) and g (gamma) as products, for example neutron production. | `n` |
| `none` | Reactions for which EXFOR gives no product, such as fission or total cross sections. Reactions such as capture, (n,g), do have a product (239U for 238U), so none leaves them out: write none,U-239 (or use all). | `none` |
| `all` | Every product (the default). | `all` |
| An exclusion | `-` or `!` in front of an item removes it, after the inclusions. | `all,-n` |

**Groups of products: `heavy` and `residual`.** Two words select many products at once, for example all the residual nuclei that matter for activation cross sections:

| Word | Selects |
| --- | --- |
| `heavy` (also `heavy-ions`, `hi`, `ions`) | Every nuclide with Z of 3 or more, that is, all products except n, p, d, t, 3He, alpha and gamma. Isotopes of hydrogen and helium (for example 6He) are not included. Products given only as an element (such as Zr) are included; reactions without a product, and products given only as a mass number, are not. |
| `residual` (also `residuals`) | The same as `heavy`, without the target nucleus itself in its unspecified state, which is elastic scattering. These are the residual nuclei, the products that activation cross sections are about. An isomer of the target, for example 93mNb from 93Nb, is kept. |

```bash
# all heavy products of deuterons on 93Nb, cross sections only
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product residual

# the same, without the zirconium products
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product "residual,-Zr-*"

# the groups can be excluded too: only the light products
python exfor_retrieve.py --target Nb-93 --projectiles d --product "all,-heavy"

# what heavy keeps and residual removes: the target itself
python exfor_retrieve.py --target Nb-93 --projectiles p --product "heavy,-residual"
```

In the snapshot used for the tests, deuterons on 93Nb with `--quantity SIG` have 60 datasets and 441 points in all; with `heavy` (and with `residual`) 57 datasets and 434 points. Spelling out the light products, `--product "all,-n,-p,-d,-t,-he3,-a,-g"`, gives 58 datasets and 435 points: the extra point is a reaction that has no product at all, which `heavy` does not select. For protons on 93Nb with all quantities there are 509 datasets (9,643 points) in all, 430 (4,287 points) with `heavy` and 422 (3,699 points) with `residual`; the 8 datasets (588 points) that `residual` removes are the elastic angular distributions of 93Nb (the quantities DA and POL/DA).

The words work in `exfor_plot.py` too, on the retrieved data (the target of each point is taken from the data), and in `--find`. The plots of the activation products of deuterons on 93Nb are then one command: `python exfor_plot.py --target Nb-93 --projectiles d --product residual --quantity SIG --exclude-status SPSDD --emax 60` (12 plots in the test). Fission yields given in a data table are filtered row by row. For 235U(n,f) with the quantity FY, `heavy` keeps 1,011 of the 1,338 datasets (9,066 of 17,351 points); what it leaves out is mainly the yields given by mass number only (chain yields, 7,393 points) and light ternary products such as alpha particles.

Notes:

- Write the state letter in lower case after the mass: `93mMo` is the isomer of molybdenum-93, `93Mo` is molybdenum-93 in every state.
- A nuclide without a state letter also selects combined-state codes such as 21-SC-44-M/G (isomeric ratio) or 77-IR-192-G+M1 (sum). To select one of those alone, write its EXFOR code, for example `21-SC-44-M/G`.
- `--product-exact` matches the EXFOR code exactly as written: `41-NB-92` then selects only data with no state given.
- Fission-fragment and mass-yield tables give the product as columns of the data table (ELEMENT, MASS). They are filtered point by point: the datasets file shows ELEM/MASS in the column `product`, the data file the product of each row. Tables with only a mass number get products labelled A=95.
- Use `--summary-only` to see which products exist before choosing: it prints the 40 products with most points, with the number of entries and points.
- The product columns of the output files are described in Sections 8.2 and 8.3.

## 8. Output files

Each run writes a catalogue of datasets and a table with one row per data point, in a folder named after the target inside `--out` (default `data`), for example `data/Nb-93/` (natural targets: `data/Ti-nat/`).

### 8.1 Files

- `EXFOR_NB-93_datasets.csv`: the catalogue, one row per dataset (one reaction of one EXFOR subentry).
- `EXFOR_NB-93_data.csv`: one row per data point, in the order of the EXFOR entries.
- `EXFOR_NB-93_datasets.json` and `EXFOR_NB-93_data.jsonl`: only with `--json`; the same tables as JSON (the data points one JSON object per line); see Section 8.5.

The CSV files are UTF-8 with comma separators. If Excel puts all columns in one cell (common with Spanish or other European regional settings), open them with Data > From Text/CSV and select comma as delimiter and UTF-8 as encoding.

With `--ascii` the run also writes every dataset as its own text file, in columns with the units in the first row, into the subfolder `ascii/` of this folder (for example `data/Nb-93/ascii/`), together with `index.csv`. The format is described in Section 8.6 and examples of its use are in Section 9.8.

### 8.2 Columns of the data file

| Column | Content |
| --- | --- |
| `target` | Target in EXFOR code (Z-SYMBOL-A, A = 0 for natural composition). |
| `projectile`, `projectile_code` | Label (n, p, d, t, 3He, alpha, gamma, 12C, ...) and EXFOR code (N, P, D, T, HE3, A, G, 6-C-12, ...). |
| `projectile_Z`, `projectile_A` | Charge and mass number of the projectile when it is a nuclide (empty for photons, electrons, mesons, antiprotons and no projectile). |
| `process` | Reaction type as written in EXFOR, for example 2N, P, A or X (any process). |
| `product` | Residual nucleus in EXFOR notation, for example 41-NB-92-M. The suffix -G means ground state and -M (or -M1, -M2) an isomer. When the product is given in the table itself the script reads it from there. |
| `product_label`, `product_Z`, `product_A`, `product_state` | Readable label of the product (92mNb, 89Zr, n, alpha, gamma, natZr), its charge and mass number, and the state suffix as in EXFOR (M, G, M1, ...; empty if none). |
| `branch` | EXFOR branch code, for example CUM (cumulative, including feeding from decay of precursors), IND (independent), M+ (the metastable state is included) or PAR (partial). |
| `quantity`, `modifier` | EXFOR quantity (SIG cross section, DA angular distribution, DE energy spectrum, TTY thick-target yield, TRN transmission, ...) and modifier, if any. |
| `reaction_type` | `simple`, or `complex` when the reaction string combines several reactions (ratios, sums). Check complex ones before using them as cross sections. |
| `entry`, `subentry` | EXFOR accession number (five characters) and subentry (eight characters). The raw text is in `exforall/<first three characters>/<entry>.x4` of the master repository. |
| `first_author`, `year`, `reference`, `status` | Publication details; the EXFOR reference code, for example (J,NIM/B,373,17,2016): journal, volume, page, year. Status codes as in EXFOR (Section 10). |
| `E_MeV`, `dE_MeV` | Incident (laboratory) energy of the projectile, total kinetic energy, and its uncertainty or resolution, in MeV. Empty when the energy is not tabulated or cannot be converted (Section 8.4). |
| `E_per_u_MeV` | Incident energy per nucleon in MeV, when the projectile mass is known. |
| `E_unit`, `E_source` | Original unit of the energy and the column it came from: EN, EN-MIN/MAX (mid-point of the range) or EN-MEAN. |
| `value`, `dvalue`, `value_unit` | The measured value and its total uncertainty, converted to mb (cross sections), mb/sr or mb/MeV when the EXFOR unit allows it; otherwise the original unit is kept. Percentage uncertainties become absolute. |
| `raw_value`, `raw_unit` | The value and unit exactly as in EXFOR. |
| `err_stat`, `err_sys` | Statistical and systematic uncertainties, when given separately in the entry. |
| `angle_deg` | Angle column of the table (ANG or ANG-CM), as tabulated. |
| `E_out_MeV` | Energy of the outgoing particle for spectra (the column E, or the mid-point of the bin E-MIN to E-MAX when the energy is given as a bin). |
| `extra` | Any other columns of the table (flags, excitation energies, ...) as JSON text. |

### 8.3 Columns of the datasets file

| Column | Content |
| --- | --- |
| `target`, `projectile`, `projectile_code`, `projectile_Z`, `projectile_A`, `process`, `product`, `product_label`, `product_Z`, `product_A`, `product_state`, `branch`, `quantity`, `reaction_type` | As in the data file. For products given in the data table the column `product` shows ELEM/MASS (or ELEM, MASS) and the product of each point is in the data file. |
| `projectile_raw` | The projectile spelling as written in the EXFOR reaction (differs from `projectile_code` only for the few miscoded entries). |
| `reaction_string` | The raw EXFOR reaction field, for example (41-NB-93(D,2N)42-MO-93-M,,SIG). |
| `entry`, `subentry`, `n_points` | Accession number, subentry and number of points retained. |
| `E_min_MeV`, `E_max_MeV` | Incident-energy range covered by the dataset. |
| `first_author`, `authors`, `year`, `reference`, `doi` | Publication details: first author, the full author list as in EXFOR, year, EXFOR reference code and DOI. They are used to write the list of references (Section 5.3). |
| `facility`, `institute` | Accelerator and laboratories as coded in EXFOR. |
| `status`, `title` | EXFOR status codes and title of the entry; the pointers of codes such as SPSDD,D4046006 are in status\_ref (Section 10.1). |
| `incident_energy_note` | Text of the EXFOR field EN-SEL, if the entry has one (often empty). |

With the option `--halflife` the datasets file has six more columns at the end (they are empty without it): `exfor_T12`, `exfor_T12_s`, `product_T12`, `product_T12_s`, `product_T12_basis` and `target_T12` (Section 10.2).

### 8.4 Energies

- **Total and per-nucleon energy.** `E_MeV` is always the total laboratory energy of the projectile. When EXFOR gives the energy per nucleon (MEV/A, GEV/A) it is multiplied by the projectile mass number: 180 MeV/A for 12C becomes 2160 MeV. The per-nucleon value is kept in `E_per_u_MeV`.
- **Units.** eV, keV, MeV, GeV and the milli-, micro- and nano-eV are converted. Neutron wavelengths (Angstrom) are converted with E = 81.804 meV Å² / λ²; the same unit for any other projectile is not converted.
- **What is never done.** An energy in a unit that cannot be converted is left empty and counted in a warning at the end of the run; it is never assumed to be MeV. A per-nucleon energy for a projectile of unknown mass (for example natural carbon) leaves `E_MeV` empty and fills `E_per_u_MeV`.
- **Energy ranges and means.** If the table gives EN-MIN and EN-MAX the mid-point is used and half the range is `dE_MeV`. If only EN-MEAN is given it is used as the energy (`E_source` = EN-MEAN).
- **Resolution columns.** EN-ERR, EN-RSL and EN-RSL-HW give `dE_MeV` directly; EN-RSL-FW (full width) is halved; percentages are converted. Resolutions given as time of flight (ns/m) are not converted and `dE_MeV` stays empty.
- **Spectra and missing energies.** For spectra the outgoing energy is in `E_out_MeV`. If the incident energy is not a column of the table (for example when it is written only in the text of the entry), `E_MeV` stays empty; see `incident_energy_note` or the entry itself.

### 8.5 JSON output (--json)

`--json` writes the results as JSON in addition to the CSV files. It adds no new data and is off by default.

Files written:

- `<prefix>_datasets.json`: one JSON file with `target`, `projectiles` (the string you gave) and a `datasets` list, with one entry per dataset.
- `<prefix>_data.jsonl`: JSON Lines, one JSON object per data point, one per line.

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --json
```

Load the files in Python:

```python
import json, pandas as pd
datasets = json.load(open("EXFOR_NB-93_datasets.json"))["datasets"]
points = pd.read_json("EXFOR_NB-93_data.jsonl", lines=True)
```

When to use it:

- When the data go to a tool that prefers JSON, such as JavaScript, a database or `jq` on the command line.
- Missing values are `null` instead of empty cells, and numbers stay numbers.
- JSON Lines can be read one line at a time without loading the whole file.

For Excel, Origin or pandas the CSV files are enough and smaller: for Nb-93 with all projectiles the CSV is about 34 MB and the JSONL about 100 MB.

The `extra` field of each point is a JSON text stored inside a string, as in the CSV; use `json.loads(row["extra"])` for non-empty values. Version 1 wrote a single `.json` file with both tables (Section 19).

### 8.6 One ASCII file per dataset (`--ascii`)

The CSV files hold all points of a retrieval in one table. For plotting programs, spreadsheets or your own analysis you often want each dataset on its own, in plain columns. `--ascii` writes one text file for each dataset (each reaction record of each subentry) into a subfolder `ascii` of the data folder, with the units in the first row of every file:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m --ascii
```

This writes `data/Nb-93/ascii/` with five files (one per dataset) and `index.csv`. The same option exists in `exfor_plot.py` (`--ascii`), where it writes only the datasets that are plotted, after the filters (`--entries`, `--exclude-status`, `--emax` and so on). There the folder is `<data-dir>/<target>/ascii` (`--data-dir`, default `data`). `--ascii-dir` chooses another folder. Examples of use, with the code to read the files, are in Section 9.8.

**The file name says what the dataset is.** For example:

```text
Nb-93_d_92mNb_SIG_Tarkanyi2007_D4156-003.dat
```

It has the target, the projectile, the product, the quantity (and the branch or modifier, if there is one, such as `CUM`), the first author with the year, and the EXFOR entry with the last three characters of the subentry. A variable that is constant in the dataset (a fixed beam energy or angle) is added at the end: `Be-9_p_n_DA_DE_Clough1970_F0789-008_E30MeV_angle30deg.dat`.

**The first row has the column names with their units**, and the columns are separated by spaces:

```text
E[MeV]  err_E[MeV]  sigma[mb]  err_sigma[mb]
0.02    2.7         1.43       0.16
5.63    1.18        0.5        0.05
6.91    1.1         0.66       0.07
```

The unit of the value is the one of the data file (cross sections are in mb), written without spaces (`particles/(MeV*uC*sr)`). `err_` in front of a name is its uncertainty, missing values are written `nan`, and the quantity has its name, not its EXFOR code: `sigma`, `dsigma/dOmega`, `d2sigma/dOmega/dE`, `fission_yield` (Section 8.6.5). The files are read as they are by numpy (`np.loadtxt(f, skiprows=1)`), pandas (`pd.read_csv(f, sep=r"\s+")`). I tested them with numpy and pandas; any program that reads columns separated by spaces can read them if it skips the first row.

| The dataset varies in | Columns of the file |
| --- | --- |
| One variable (incident energy, outgoing energy, angle, the mass number of the product, or another variable of Section 8.6.1) | The variable, its energy uncertainty `dE` (only for the incident energy), the value and its uncertainty |
| Two variables: a 2D distribution | **One file with the two variables, the value and its uncertainties**: the variable that labels the blocks first (the angle, for example), then the other variable, then the value and its uncertainty: `angle[deg]  E_neutron[MeV]  yield_dd[particles/(MeV*uC*sr)]  err_yield_dd[particles/(MeV*uC*sr)]`. All the energies and values of one angle follow each other, and a blank line separates the angles. For the yield of a fission product: `Z_product[-]  A_product[-]  fission_yield[%/fission]  err_fission_yield[%/fission]` |
| Three or more variables | One column for each variable, then the value; the blocks are those of the first variable |

The file of a 2D distribution holds every point of the dataset: a double-differential yield of 9Be(p,n) at 9.18 MeV, with 10 angles and 80 outgoing energies, is one file of 738 data lines plus the first row and 9 blank lines between the 10 angle blocks. The uncertainties are in the columns after the value, as in every file, when the dataset gives them (`err_yield_dd[particles/(MeV*uC*sr)]` here); `--ascii-no-errors` leaves them out and gives exactly three columns. The blank lines are skipped by numpy, pandas and gnuplot and make a block easy to see; `--ascii-no-blanks` leaves them out. Section 8.6.3 gives the rule for the order of the columns.

**`index.csv`** lists every file with the format, target, projectile, process, product, quantity, entry, author, year, reference, the number of entries and datasets in the file, the number of variables, the column names, which uncertainties the file has (\`uncertainty\`: \`total\`, \`stat\`, \`sys\`, a combination such as \`total+sys\`, or \`none\`), the meaning of each variable (`variables`), the number of points, the incident-energy range and the unit. Use it to find a dataset, or to know where each file came from.

**Limits and cases to know about**

- **Products given row by row.** A dataset whose product is given in the data table (fission yields, fragment tables) is one file, with the product as the independent variable: the mass number `A_product`, or the atomic number and mass number `Z_product`, `A_product` (a 2D distribution). Earlier versions wrote one file for each product, which gave thousands of files for a heavily studied target; for 235U(n,f) with the quantity FY that was 10,618 files, now it is 1,338 (Section 8.6.2 gives fewer files still).
- **Names may repeat.** If two datasets would have the same name, the second gets `_2` before the extension.
- **Energies are in MeV.** The incident energy is the total laboratory energy (for heavy ions, the total energy of the ion), as in the CSV file.
- **Not the same as the CSV.** The ASCII files have fewer fields than the CSV file (no reference, status or raw values, apart from `index.csv`). Keep the CSV files if you need them.
- **CSV files from older versions** have no `dataset` column and no units for the `extra` column. `exfor_plot.py --data` still writes the ASCII files from them, but a dataset is then one file for each product, and the unit of a variable that is not an energy or an angle is `[?]`. Retrieve the data again to get the units.

#### 8.6.1 Labels of the independent variables

The columns that are not energies or angles carry a proper label, with the unit as recorded in EXFOR, not a question mark. The variables of the data file have these labels:

| Column | Label in the first row | Meaning |
| --- | --- | --- |
| `E_MeV` | `E[MeV]` | Incident energy |
| `E_out_MeV` | `Eout[MeV]` | Outgoing energy |
| `angle_deg` | `angle[deg]` | Angle |
| `product_Z` | `Z_product[-]` | Atomic number of the product (products given row by row) |
| `product_A` | `A_product[-]` | Mass number of the product (products given row by row) |

Other EXFOR data headings that are the independent variable of a dataset are written with these labels; the unit is the one of the EXFOR column, for example `[MeV]` or `[keV]`. The values are not converted, since the unit is stated in the first row:

| EXFOR heading | Label | Meaning |
| --- | --- | --- |
| `E-LVL` | `E_level` | Excitation energy of the residual-nucleus level |
| `E-EXC` | `E_excitation` | Excitation energy |
| `E-DGD` | `E_transfer` | Energy transfer, for example E(p) minus E(p') in a (p,p') measurement |
| `E-CM` | `E_cm` | Energy in the centre-of-mass system |
| `Q-VAL` | `Q_value` | Q-value |
| `COS`, `COS-CM` | `cos_theta`, `cos_theta_cm` | Cosine of the angle (laboratory, centre of mass) |
| `LVL-NUMB` | `level_number` | Number of the nuclear level |
| `MOMENTUM L`, `SPIN J` | `L`, `J` | Orbital angular momentum, spin |
| `KT` | `kT` | Temperature as thermal energy, for Maxwellian averages |
| `TEMP`, `THICKNESS` | `temperature`, `thickness` | Temperature, target thickness |
| `EN-DUMMY` | `E_dummy` | Incident energy given as a dummy variable |
| `MASS`, `ELEMENT` | `mass_number`, `atomic_number` | Mass number, atomic number (when not the product of a table) |

An EXFOR heading that is not in this list, and that varies in a dataset where nothing else does, is used with its EXFOR name as the label, for example `XYZ[unit]`; its meaning is then in the EXFOR entry. The meaning of each variable of a file is in the column `variables` of `index.csv`, for example `E_transfer[MeV] = energy transfer (EXFOR E-DGD)`. In the test, the data of H.Otsu (entry E2075) for 9Be(p,n), which have the energy transfer as the independent variable, give `E_transfer[MeV]  d2sigma/dOmega/dE[mb/sr/MeV]` and not an unlabelled column.

I could confirm the meaning of `E-DGD` from the text of that entry. The other labels follow the names and units of the EXFOR data headings as I know them; if you rely on one for a published result, check it in the EXFOR entry or in the EXFOR dictionary of data headings.

#### 8.6.2 Fewer files: `--ascii-format entry` and `--ascii-format quantity`

One file for each dataset is the default (`--ascii-format dataset`). For targets with very many datasets, and above all for fission yields, there are two formats with far fewer files. They stack the points of several datasets in one file, in the *long* form: one row for each point, with columns that tell the datasets apart. They are still plain text, in columns, with the units in the first row.

| `--ascii-format` | One file for each | Added columns that identify the dataset |
| --- | --- | --- |
| `dataset` (default) | Dataset (reaction record of a subentry) | None; the name has the author and the entry |
| `entry` | EXFOR entry (publication), process, quantity and unit | `sub` (subentry), and `product` and `branch` when they differ |
| `quantity` | Projectile, process, quantity and unit, with all the entries | `entry`, `author`, `sub`, and `product` and `branch` when they differ |

For 235U(n,f) with the quantity FY the numbers are: 1,427 files with `dataset`, 599 with `entry`, and 5 with `quantity`. The five files of `quantity` are one for each unit of the yield (the units differ between datasets, so they cannot be mixed): `U-235_n_F_FY_PC-FIS_all-entries.dat` (347 entries, 560 datasets, 10,132 points), `..._NO-DIM_...` (192 entries, 664 datasets, 5,411 points), `..._ARB-UNITS_...` (30 entries, 1,197 points), `..._PRD-FIS_...` (20 entries, 477 points) and `..._PRT-FIS_...` (10 entries, 134 points). The first one is 1.4 MB. Its first rows are:

```text
entry  author             sub  product  branch   E[MeV]     Z_product[-]  Eout[MeV]  A_product[-]  E_dummy[eV]  err_E[MeV]  fission_yield[%/fission]  err_fission_yield[%/fission]
10722  Strittmatter1977   003  82Ga     IND      2.53e-08   31            nan        82            nan          nan         0.011                     0.005
10722  Strittmatter1977   003  82Ge     IND      2.53e-08   32            nan        82            nan          nan         0.13                      0.009
```

In these files:

- `nan` means that the dataset does not give that variable, for example `Eout` when it has none, or the uncertainty when it is not given. A column appears only if at least one dataset has it.
- The text columns (`entry`, `author`, `sub`, `product`, `branch`) have no spaces, so that the file is read by any program that splits at spaces. The `branch` tells independent (`IND`), cumulative (`CUM`), chain (`CHN`), prompt (`PRE`) and other yields apart; do not average different branches.
- The uncertainty column is always present when any dataset has it, also for 2D data.
- The units of the value are the ones of the EXFOR data and differ between files of the same quantity, as the file names say.

To select what you need from a `quantity` file, filter the columns:

```python
import pandas as pd
d = pd.read_csv("data/U-235/ascii/U-235_n_F_FY_PC-FIS_all-entries.dat", sep=r"\s+")
cs137 = d[(d["product"] == "137Cs") & (d["branch"] == "CUM")]
print(cs137[["author", "E[MeV]", "fission_yield[%/fission]", "err_fission_yield[%/fission]"]].sort_values("E[MeV]"))
```

In the test this gives 37 points of the cumulative yield of 137Cs, from 29 entries.

```bash
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --ascii --ascii-format quantity
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --ascii --ascii-format entry
```

When the limit `--max-ascii` is reached with the default format, the program says so and suggests these two formats. `exfor_plot.py` has the same option and writes the formats for the plotted datasets (Section 14.6). The three formats write to the same folder; give each its own with `--ascii-dir` if you want to keep several.

#### 8.6.3 Layout of the files in each case

**The rule.** The columns are the independent variables that vary in the dataset, then the value and its uncertainty. When two or more variables vary, the **first column is the variable that labels the blocks**, and each block lists the following variables and the values, so that all the energies and values of one angle follow each other. A blank line separates the blocks. The order of the variables is: the angle, the incident energy `E`, the atomic number `Z` of the product, the outgoing energy `Eout`, the mass number `A` of the product, then other EXFOR variables. A variable that is constant in the dataset (a fixed beam energy or angle) is in the file name, for example `_E22.4MeV` or `_angle0deg`. The cases below are real files of the tests; the first row is always the column names with their units.

| Dataset | First row | Example file |
| --- | --- | --- |
| Excitation function | `E[MeV]  err_E[MeV]  sigma[mb]  err_sigma[mb]` | `Nb-93_d_92mNb_SIG_Tarkanyi2007_D4156-003.dat` |
| Angular distribution at one energy | `angle[deg]  dsigma/dOmega[arb_units]  err_stat_dsigma/dOmega[arb_units]` | `Nb-93_p_93Nb_DA_Fulmer1962_C1019-023_E22.4MeV.dat` |
| Neutron spectrum at one beam energy | `E_neutron[MeV]  d2sigma/dOmega/dE[mb/sr/MeV]  err_sys_d2sigma/dOmega/dE[mb/sr/MeV]` | `Li-7_p_n_DA_DE_Prajapati2012_33040-007_E18MeV.dat` |
| 2D: angle and outgoing energy | `angle[deg]  E_neutron[MeV]  yield_dd[particles/(MeV*uC*sr)]  err_yield_dd[particles/(MeV*uC*sr)]` | `Be-9_p_n_PY_DA_DE_Lychagin2003_A0834-002_E9.18MeV.dat` |
| 2D: angle and incident energy | `angle[deg]  E[MeV]  dsigma/dOmega[mb/sr]  err_dsigma/dOmega[mb/sr]` | `Nb-93_p_alpha_DA_Ferrero1979_D0431-007.dat` |
| 2D: incident and outgoing energy (angle fixed) | `E[MeV]  E_neutron[MeV]  d2sigma/dOmega/dE[mb/sr/MeV]  err_sys_d2sigma/dOmega/dE[mb/sr/MeV]` | `Li-7_p_n_DA_DE_Byrd1989_C1873-002_angle0deg.dat` |
| Three variables | `angle[deg]  E[MeV]  E_neutron[MeV]  yield_dd[particles/(MeV*uC*sr)]  err_stat_yield_dd[particles/(MeV*uC*sr)]` | `Be-9_p_n_PY_DA_DE_Lone1977_C1837-004.dat` |
| Another independent variable (Section 8.6.1) | `E_transfer[MeV]  d2sigma/dOmega/dE[mb/sr/MeV]  err_stat_d2sigma/dOmega/dE[mb/sr/MeV]  err_sys_d2sigma/dOmega/dE[mb/sr/MeV]` | `Be-9_p_n_DA_DE_Otsu1995_E2075-099_E392MeV_angle20deg.dat` |
| Mass yields | `A_product[-]  fission_yield[-]  err_fission_yield[-]` | `U-235_n_products_FY_CUM_Shima1978_10864-003.dat` |
| Nuclide yields | `Z_product[-]  A_product[-]  fission_yield[%/fission]  err_fission_yield[%/fission]` | `U-235_n_products_FY_IND_Strittmatter1977_10722-003_E2.53e-08MeV.dat` |
| Mass yields at several energies | `E[MeV]  A_product[-]  err_E[MeV]  fission_yield[%/fission]  err_fission_yield[%/fission]` | `U-235_n_products_FY_CHN_Younes2001_14014-002.dat` |

Two of them in full. The cross sections of 93Nb(p,x)4He at several angles and energies, the angle first (the angle 30 degrees, then the energies at that angle):

```text
angle[deg]  E[MeV]  dsigma/dOmega[mb/sr]  err_dsigma/dOmega[mb/sr]
30          19.9    2.6481                nan
30          24.6    4.4504                nan
30          29.7    6.0512                nan
30          34.6    7.8784                1.1975
```

The neutron spectra of 7Li(p,n) at 0 degrees for several beam energies, the beam energy first, then the neutron energies of that beam energy:

```text
E[MeV]  E_neutron[MeV]  d2sigma/dOmega/dE[mb/sr/MeV]  err_sys_d2sigma/dOmega/dE[mb/sr/MeV]
29.2    11.425          1.524                         0.28956
29.2    11.832          1.371                         0.26049
29.2    12.239          1.336                         0.25384
29.2    12.595          1.445                         0.27455
```

The energy-angle files read the same way in any program: the first column selects a block, for example `d[d.iloc[:, 0] == 30]` in pandas gives the energies and cross sections at 30 degrees. With `--ascii-no-blanks` the blank lines between the blocks are left out; the order of the rows does not change. The formats `entry` and `quantity` (Section 8.6.2) are long tables without blank lines, with the columns in the same order after the columns that identify the dataset.

#### 8.6.4 The format of the fission yields

A fission yield (the quantity `FY`) is a distribution over the fission products, so the product is the independent variable. In EXFOR the product of such a dataset is given row by row in the data table; each dataset is written as **one file**, and the product is described by its numbers:

| The dataset gives | Columns | Layout |
| --- | --- | --- |
| The yield by mass number (mass or chain yields) | `A_product[-]  fission_yield[unit]  err_fission_yield[unit]` | One row for each mass number, in increasing order |
| The yield by atomic number and mass number (nuclide yields) | `Z_product[-]  A_product[-]  fission_yield[unit]  err_fission_yield[unit]` | One block for each Z, listing its mass numbers and yields (an isotopic chain), a blank line between the blocks |
| Several incident energies in one dataset | `E[MeV]  A_product[-]  err_E[MeV]  fission_yield[unit]  err_fission_yield[unit]` | One block for each incident energy: a mass-yield curve |
| One yield for one nuclide | `fission_yield[unit]  err_fission_yield[unit]` | One row; the energy is in the name |

In the file name the word `products` stands for the many products, then come the quantity, the **branch** and the author, entry and subentry, and the fixed incident energy if there is one: `U-235_n_products_FY_IND_Strittmatter1977_10722-003_E2.53e-08MeV.dat`. The branch tells what the yield is: `CHN` chain (mass) yield, `CUM` cumulative, `IND` independent, `PRE` before neutron emission, and so on. They are different quantities and must not be mixed. The unit of the yield is in the first row and differs between datasets (`PC/FIS`, per cent per fission, is the most common; `NO-DIM`, `ARB-UNITS` and others also occur). The thermal energy of the example is 2.53e-08 MeV.

For 235U(n,f) with the quantity FY the 1,338 datasets give 1,427 files (the isomer yields of a dataset are a file of their own; Section 14.11): 485 with one variable, 502 with two, 18 with three and 422 with a single yield. The point of this layout is that the files can be read as they are for a plot of the mass-yield curve or of the nuclide chart (Section 14.10), and that a dataset is one file, not one for each fission product. For far fewer files use `--ascii-format entry` (599 files) or `quantity` (5 files, one for each unit), which stack the datasets with the columns `entry`, `author`, `sub`, `product` and `branch` (Section 8.6.2).

**Isomers.** When a table of products has the column `ISOMER` (Section 14.11), the yields of the ground state and of the isomers of a nuclide are not mixed: the isomers of a dataset are written in a file of their own, `U-235_n_products_FY_IND_Ford1984_12895-003_isomer-M.dat` next to `U-235_n_products_FY_IND_Ford1984_12895-003.dat`, with the same columns, and the column `isomer` of `index.csv` says `M` (or `M2`). In the stacked formats (`entry` and `quantity`) the column `product` has the state in the label: `85mKr` for the isomer, `85gKr` for the ground state. This is why the 1,338 datasets of 235U(n,f) give 1,427 files with the default format (40 of them files of isomers of a table of products).

#### 8.6.5 Names of the quantities, units and emitted particle in the columns

The first row names every column, in plain ASCII without spaces, with the unit in square brackets. The names are made from the data, in the same way as the labels of the plots (Section 14.13), so that a column says what it is: the quantity has its name and not its EXFOR code, the unit is written out, and the outgoing energy is the energy of the particle that is emitted.

**The value.** The name comes from the EXFOR quantity code:

| EXFOR quantity | Name in the file | Example of a first row |
| --- | --- | --- |
| `SIG` | `sigma` | `E[MeV]  err_E[MeV]  sigma[mb]  err_sigma[mb]` |
| `DA` | `dsigma/dOmega` | `angle[deg]  dsigma/dOmega[mb/sr]` |
| `DE` | `dsigma/dE` |  |
| `DA/DE` | `d2sigma/dOmega/dE` | `E_neutron[MeV]  d2sigma/dOmega/dE[mb/sr/MeV]  err_sys_d2sigma/dOmega/dE[mb/sr/MeV]` |
| `PY/DA/DE` | `yield_dd` | `angle[deg]  E_neutron[MeV]  yield_dd[particles/(MeV*uC*sr)]  err_yield_dd[particles/(MeV*uC*sr)]` |
| `FY` | `fission_yield` | `Z_product[-]  A_product[-]  fission_yield[%/fission]  err_fission_yield[%/fission]` |
| `NU`, `NU/DE`, `PN`, `PN/DE`, `PY`, `TTY`, `TTY/PY/DA/DE`, `POL/DA`, `SIG/RAT`, `TRN`, `WID` | `nu`, `nu_spectrum`, `Pn`, `Pn_spectrum`, `yield`, `thick_target_yield`, `thick_target_yield_dd`, `polarisation`, `sigma_ratio`, `transmission`, `width` |  |
| any other code | the code with the slash written as an underscore (`MLT_DA`) |  |

When the unit that EXFOR gives contradicts the quantity code (for example `DA` in `MB`, without sr), the name is not used and the column is written with the code and the unit as they are (`DA[mb]`); the reasons and the numbers are in Section 14.13.

**The unit.** It is the unit of the data, without spaces: `MB/SR/MEV` is `mb/sr/MeV`, `MUB` is `ub` (the micro sign is written `u`), `SR2` is `sr^2`, `P/MEVMUCSR` is `particles/(MeV*uC*sr)`, `PC/FIS` is `%/fission`, `ARB-UNITS` is `arb_units`, and a quantity without a unit (`NO-DIM`) has `-`. A unit that is not known stays as EXFOR writes it.

**The uncertainties** of a column have the same name with `err_` in front: `err_E[MeV]` for the incident energy (before `dE`), `err_sigma[mb]` for the cross section (before `dSIG`). When EXFOR gives the statistical or the systematic uncertainty of the value, in the columns `ERR-S` and `ERR-SYS`, the file has them as `err_stat_` and `err_sys_` in front of the name (`err_stat_sigma[mb]`, `err_sys_sigma[mb]`); `err_` is then the total uncertainty (`ERR-T` or `DATA-ERR`), and a dataset can have one, two or all three. A column of uncertainties is in the file when at least one point of the dataset has it, and it is `nan` for the points that have none. The incident energy has its uncertainty in every kind of file in which it is a column. The files have the uncertainties by default, also the 2D files; `--ascii-no-errors` leaves them out. The partial uncertainties `ERR-1`, `ERR-2` ... of EXFOR, which belong to the error sources named in the entry, are not written; they stay in the column `extra` of the data file.

**Datasets without uncertainty.** When EXFOR gives no uncertainty for a dataset, neither as a column nor as a statement in the entry, the file has no uncertainty column: the programs write what EXFOR contains and do not invent errors. The column `uncertainty` of `index.csv` says `none` for such a file, and the program prints how many files are in this case (`2 of the 6 files have no uncertainty column because EXFOR gives none for those data`). The deuteron data on 27Al giving 28Si of Section 16.7 are an example: of the 6 files, Okorokov 1971 (two files) has the total uncertainty (`err_`), Roy 1970 and Elekes 2000 have the statistical one (`err_stat_`), and Al-Quraishi 2000 and Lawergren 1968 have none, because their tables have only the columns `EN`, `E` and `DATA` (Al-Quraishi) or `E` and `DATA` (Lawergren) and the entries say nothing about the uncertainty of the values. If you know the uncertainty from the publication, add it to the file yourself.

**The outgoing energy.** The column is named after the particle whose energy it is: `E_neutron`, `E_proton`, `E_deuteron`, `E_triton`, `E_3He`, `E_alpha` or `E_gamma`; when it cannot be told (several kinds of data in a stacked file) it is `Eout`. EXFOR names the particle in the field after the quantity of the reaction (`G` is a gamma ray), and without it the process decides: (d,n) gives `E_neutron`.

**A spectrum coded as a cross section.** A cross section `SIG` without a modifier that is given against the energy of an emitted neutron, proton, deuteron, triton, 3He or alpha particle is an emission spectrum: its column is `dsigma/dE` and the unit has `/MeV`. This is the case of the 27Al(d,n)28Si data of Section 16.7, whose first row is

```text
E[MeV]  E_neutron[MeV]  dsigma/dE[mb/MeV]
```

and not `E[MeV]  Eout[MeV]  SIG[mb]`, which is what the earlier versions wrote. EXFOR gives the unit of these data as `MB`; the `/MeV` is added by the program (the rule and its limits are in Section 14.13), and the data of gamma-ray lines and of levels coded `SIG` keep `sigma[mb]`. The file name keeps the EXFOR quantity code (`..._SIG_...`).

**Files of earlier versions** have the EXFOR codes in the first row (`SIG[mb]`, `dSIG[mb]`, `Eout[MeV]`, `PY_DA_DE[P/MEVMUCSR]`); write them again with `--ascii` to get the names above. A program that reads the columns by name has to use the new names; the order of the columns did not change.

## 9. Worked examples

The examples cover projectile selection, loops over targets, and loading the tables with pandas.

### 9.1 Choose projectiles, quantity and energy

Deuteron and 3He cross sections on 63Cu between 10 and 40 MeV, with a custom file name:

```bash
python exfor_retrieve.py --target Cu-63 --projectiles d,he3 --quantity SIG \
    --emin 10 --emax 40 --prefix cu63
```

Neutron and photon cross sections on 56Fe:

```bash
python exfor_retrieve.py --target Fe-56 --projectiles n,g --quantity SIG
```

Everything except neutrons on 93Nb (54,185 points at the time of writing instead of 140,285):

```bash
python exfor_retrieve.py --target Nb-93 --projectiles=all,-n
```

Heavy ions only, restricted to a few beams:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles "12C,16O,Ne-*"
```

### 9.2 Natural targets and several targets in a loop

```bash
for t in Nb-93 Mn-55 Ti-nat Cu-nat; do
    python exfor_retrieve.py --target $t --projectiles d --quantity SIG
done
```

Each run scans the library again (20 seconds to a minute). The files of each target go to their own folder: data/Nb-93/, data/Mn-55/, data/Ti-nat/ and data/Cu-nat/. On Windows run the commands one after the other or use a small batch file.

### 9.3 Which datasets exist for one product?

```python
import pandas as pd
ds = pd.read_csv("data/Nb-93/EXFOR_NB-93_datasets.csv")
sel = ds[(ds["product"] == "41-NB-92-M") & (ds.quantity == "SIG")
         & (ds.projectile == "d")]
print(sel[["entry", "first_author", "year", "E_min_MeV", "E_max_MeV", "n_points"]])
```

For deuterons on 93Nb this lists the 92mNb datasets from several laboratories (Avrigeanu 2013, Tárkányi 2007, Ditrói 2016 and Aikawa 2018 at the time of writing).

### 9.4 Plot an excitation function from all datasets

For ready-made plots use `exfor_plot.py` (Section 14). The code below shows how to draw one product by hand with pandas.

```python
import pandas as pd, matplotlib.pyplot as plt
d = pd.read_csv("data/Nb-93/EXFOR_NB-93_data.csv")
sel = d[(d.projectile == "d") & (d.quantity == "SIG")
        & (d["product"] == "41-NB-92-M") & (d.reaction_type == "simple")]
fig, ax = plt.subplots()
for (entry, sub, author, year), g in sel.groupby(["entry", "subentry", "first_author", "year"]):
    ax.errorbar(g.E_MeV, g.value, yerr=g.dvalue, xerr=g.dE_MeV, fmt="o", ms=4,
                capsize=2, label=f"{author} {year} ({entry})")
ax.set_xlabel("Deuteron energy (MeV)"); ax.set_ylabel("Cross section (mb)")
ax.legend(); fig.savefig("nb92m.png", dpi=150)
```

### 9.5 Energy per nucleon for heavy ions

```python
import pandas as pd
d = pd.read_csv("data/Nb-93/EXFOR_NB-93_data.csv", low_memory=False)
hi = d[d.projectile == "12C"]
print(hi[["E_unit", "E_per_u_MeV", "E_MeV"]].drop_duplicates().head())
```

For rows with `E_unit` = MEV/A, `E_per_u_MeV` is the tabulated value (for example 180) and `E_MeV` the total energy (2160).

### 9.6 Update the local copy

```bash
python exfor_retrieve.py --target Nb-93 --update
```

This runs git pull on the existing clone before the search. Use it when you want data submitted since your last download. The full routine, with the check of the date of your copy and what to do if the update is skipped, is in Section 3.2.

### 9.7 Select the final product

Cross sections of 92mNb and 89Zr from deuterons on 93Nb:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m,Zr-89
```

With `--product Nb-92m` alone the script finds five datasets and 90 points (Buttsev 1986, Avrigeanu 2013, Tárkányi 2007, Ditrói 2016, Aikawa 2018 at the time of writing; the first gives its products in a table with an isomer flag, Section 14.11). All zirconium products of the same reaction, any isotope and any state:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product "Zr-*"
```

Neutron production on 208Pb by protons, photons and neutrons:

```bash
python exfor_retrieve.py --target Pb-208 --projectiles p,g,n --product n
```

Neutron-induced fission cross sections of 238U (reactions without a product):

```bash
python exfor_retrieve.py --target U-238 --projectiles n --quantity SIG --product none
```

Fission yield of 137Cs from neutrons on 235U (product taken from the data table, point by point):

```bash
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --product Cs-137
```

To see which products exist before choosing, run without `--product` and add `--summary-only`; then list them from the files with pandas:

```python
import pandas as pd
ds = pd.read_csv("data/Nb-93/EXFOR_NB-93_datasets.csv")
print(ds.groupby("product_label").n_points.sum().sort_values(ascending=False).head(10))
```

### 9.8 Save each dataset as an ASCII file: examples

`--ascii` writes every dataset as its own text file in columns, with the units in the first row; the format and its limits are described in Section 8.6. The examples below were run on the EXFOR snapshot used for the tests (October 2026).

**Example 1: an excitation function, one file for each laboratory.** Deuterons on 93Nb, the product 92mNb:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m --ascii
```

The folder `data/Nb-93/ascii/` then has five data files and `index.csv`:

```text
Nb-93_d_92mNb_SIG_Aikawa2018_E2589-003.dat
Nb-93_d_92mNb_SIG_Avrigeanu2013_D0713-003.dat
Nb-93_d_92mNb_SIG_Buttsev1986_F1217-003.dat
Nb-93_d_92mNb_SIG_Ditroi2016_D4344-004.dat
Nb-93_d_92mNb_SIG_Tarkanyi2007_D4156-003.dat
index.csv
```

`index.csv` tells what each file is (author, year, number of points, energy range, units):

```python
import pandas as pd
idx = pd.read_csv("data/Nb-93/ascii/index.csv")
print(idx[["first_author", "year", "n_points", "E_min_MeV", "E_max_MeV"]].sort_values("year"))
```

The five files have 43 (Tarkanyi 2007), 25 (Avrigeanu 2013), 9 (Ditroi 2016), 12 (Aikawa 2018) and 1 point (Buttsev 1986, one point at 7,300 MeV; its entry gives the products in a table with an isomer flag, which the programs now use, Section 14.11). To draw them again from the text files, with the author and year of the file name as the label (the file of Buttsev has no energy uncertainty, which the code allows for):

```python
import glob
import pandas as pd
import matplotlib.pyplot as plt

for f in sorted(glob.glob("data/Nb-93/ascii/*92mNb*.dat")):
    d = pd.read_csv(f, sep=r"\s+")              # the first row holds the names and units
    label = f.split("_")[4]                       # author and year, from the file name
    xerr = d["err_E[MeV]"] if "err_E[MeV]" in d else None      # not every dataset gives an energy uncertainty
    plt.errorbar(d["E[MeV]"], d["sigma[mb]"], xerr=xerr, yerr=d["err_sigma[mb]"], fmt="o", ms=3, label=label)
plt.xlim(0, 60)                                 # leave out the point at 7,300 MeV
plt.xlabel("E (MeV)"); plt.ylabel("cross section (mb)"); plt.legend()
plt.savefig("nb92m_from_ascii.png", dpi=120)
```

This draws the five datasets with their error bars (the point of Buttsev, at 7,300 MeV, is outside the limits of the figure). Any other program that reads space-separated columns can read the same files if it skips the first row; I tested numpy and pandas.

**Example 2: a 2D distribution in one file.** The double-differential neutron yield of protons on 9Be (quantity `PY/DA/DE`):

```bash
python exfor_retrieve.py --target Be-9 --projectiles p --product n --quantity PY/DA/DE --ascii
```

This gives 17 files. One of them is `Be-9_p_n_PY_DA_DE_Lychagin2003_A0834-002_E9.18MeV.dat`, the measurement at 9.18 MeV (the beam energy is in the name), with the angle, the neutron energy and the yield and its uncertainty in four columns. The first column is the angle: all the energies and yields of one angle follow each other, and a blank line separates the angles:

```text
angle[deg]  E_neutron[MeV]  yield_dd[particles/(MeV*uC*sr)]  err_yield_dd[particles/(MeV*uC*sr)]
0           0.3             580000000                        2842000
0           0.4             1140000000                       2394000
0           0.5             1460000000                       1752000
...
0           8.2             72000                            266.4

10          0.3             553000000                        2709700
10          0.4             1180000000                       2478000
```

It has 738 data lines: 10 angles and 80 neutron energies. Reading it takes three lines, and the first row gives the axis labels:

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

f = "data/Be-9/ascii/Be-9_p_n_PY_DA_DE_Lychagin2003_A0834-002_E9.18MeV.dat"
with open(f) as fh:
    aname, ename, zname, dname = fh.readline().split()      # the names with their units
angle, E, y, dy = np.loadtxt(f, skiprows=1, unpack=True)     # four columns; the blank lines are skipped
plt.scatter(E, angle, c=y, norm=LogNorm(), marker="s", s=14)
plt.xlabel(ename); plt.ylabel(aname); plt.colorbar(label=zname)
plt.savefig("map.png", dpi=120)
```

The result is a row of points for each of the 10 angles, coloured by the yield. For a filled map or a 3D surface of the same data, use `--map2d` or `--plot3d` of the plotting program (Section 16.6); the text file is for your own analysis or programs. The fourth column is the uncertainty of the yield (`dy` above); `--ascii-no-errors` leaves it out.

**Example 3: figure, data files and references in one command.** The plotting program writes the ASCII files of the datasets that it plots, so one command gives the figure, the data behind it and the bibliography:

```bash
python exfor_plot.py --target Nb-93 --projectiles d --product 92mNb --exclude-status SPSDD --emax 40 --ascii --references
```

This writes the plot `plots/Nb-93/Nb-93_d_92mNb.png`, the references `plots/Nb-93/Nb-93_references.txt` and `.bib` (Section 5.3), and the four text files in `data/Nb-93/ascii/`. They hold only what is plotted, after the filters: with `--emax 40` the file of Ditroi 2016 has 5 points (30.9 to 39.6 MeV) instead of 9, and the other three files are unchanged.

**Take care:** the retrieval (Example 1) and the plotting program write to the same folder, `data/Nb-93/ascii/`, and the file names are the same. Running Example 3 after Example 1 therefore replaces the Ditroi file by the shorter one. To keep both, give the plot its own folder:

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product 92mNb --exclude-status SPSDD --emax 40 \
    --ascii --ascii-dir data/Nb-93/ascii_plotted
```

In short: use `exfor_retrieve.py --ascii` for all the datasets of a selection, and `exfor_plot.py --ascii` for exactly the datasets of a figure.

**Example 4: fission yields, one file for each dataset or far fewer files.** A fission-yield dataset gives the yield of many fission products, so the product is the independent variable. Retrieve the yields of 235U(n,f):

```bash
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --ascii
```

This gives 1,427 files, one for each dataset (and one more for the isomers of a dataset), in `data/U-235/ascii/`. A dataset with the yield by mass number is one file with the label `A_product[-]` (for example `U-235_n_products_FY_CUM_Shima1978_10864-003.dat`):

```text
A_product[-]  fission_yield[-]  err_fission_yield[-]
102           0.838             0.014
103           0.611             0.04
104           0.396             0.005
106           0.0748            0.0005
```

A dataset with the yield by atomic number and mass number is a 2D distribution, one file with the yield and its uncertainty (`U-235_n_products_FY_IND_Strittmatter1977_10722-003_E2.53e-08MeV.dat`, 100 points, at the thermal energy given in the name):

```text
Z_product[-]  A_product[-]  fission_yield[%/fission]  err_fission_yield[%/fission]
31            82            0.011                     0.005

32            82            0.13                      0.009
32            83            0.048                     0.005
32            84            0.022                     0.005
```

For a heavily studied target even one file per dataset is a lot of files. Two formats stack several datasets in one file (Section 8.6.2):

```bash
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --ascii --ascii-format entry     # 599 files, one for each publication
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --ascii --ascii-format quantity  # 5 files, one for each unit
```

The `quantity` file with the yields in per cent per fission (`U-235_n_F_FY_PC-FIS_all-entries.dat`) has 10,132 points from 347 entries, with the columns `entry author sub product branch E[MeV] ... Z_product[-] A_product[-] ... fission_yield[%/fission] err_fission_yield[%/fission]`. To draw the cumulative yield of 137Cs against the neutron energy from all the datasets (37 points, 27 authors in the test):

```python
import pandas as pd
import matplotlib.pyplot as plt

d = pd.read_csv("data/U-235/ascii/U-235_n_F_FY_PC-FIS_all-entries.dat", sep=r"\s+")
cs = d[(d["product"] == "137Cs") & (d["branch"] == "CUM")]       # cumulative yield of 137Cs
for author, g in cs.groupby("author"):
    plt.errorbar(g["E[MeV]"], g["fission_yield[%/fission]"], yerr=g["err_fission_yield[%/fission]"], fmt="o", ms=4, label=author)
plt.xscale("log"); plt.xlabel("E (MeV)"); plt.ylabel("cumulative yield of 137Cs (per cent per fission)")
plt.legend(fontsize=6, ncol=2); plt.savefig("cs137_yield.png", dpi=120)
```

The `branch` column matters: independent (`IND`), cumulative (`CUM`), chain (`CHN`) and prompt (`PRE`) yields are different quantities and must not be mixed.

### 9.9 Half-lives next to the isotopes: examples

The half-lives are printed only with the option `--halflife` (Section 10.2); the database is the one of Section 10.2 and the half-lives are those of the NUBASE2020 evaluation. The numbers of the examples were obtained with a database that I built from the NUBASE2020 file to test the programs.

**Example 1: the summary of a retrieval.** Deuterons on 93Nb, with the half-lives of the target and of the products:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --halflife
```

```text
Target 41-NB-93 (stable): 60 datasets, 441 data points
Points by product (top): 93mMo (T1/2 6.85 h): 120, 92mNb (T1/2 10.116 d): 90, 89Zr (T1/2 78.360 h): 34, 90mY (T1/2 3.226 h): 30, 94mNb (T1/2 6.263 m): 23, 90Nb (T1/2 14.60 h): 16, 91mNb (T1/2 60.86 d): 15, 89gZr (T1/2 78.360 h): 13
```

The target is stable and is marked so. The unit of each half-life is the one of NUBASE (`h`, `d`, `m` for minutes, `y`, `s`, `ms` and so on). A `?` after a half-life would mean that more than one isomer was possible (Section 10.2).

**Example 2: the table of the products.** With `--summary-only` nothing is written and the products are listed in a table with a column `T1/2`:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --halflife --summary-only
```

```text
product        T1/2                   entries    points   (top 40 products)
93mMo          6.85 h                       5       120
92mNb          10.116 d                     5        90
89Zr           78.360 h                     3        34
90mY           3.226 h                      3        30
94mNb          6.263 m                      1        23
90Nb           14.60 h                      4        16
91mNb          60.86 d                      2        15
89gZr          78.360 h                     4        13
```

**Example 3: what EXFOR has, with the half-lives.** The catalogue of Section 5.1 gets a column `T1/2`, and the first line has the half-life of the target when it is a single isotope (What EXFOR has for Nb-93 (stable) ...; a natural target has none). Natural copper with deuterons:

```bash
python exfor_retrieve.py --target Cu-nat --projectiles d --quantity SIG --available --halflife
```

```text
projectile  quantity  product         T1/2  entries  datasets  points  E_min  E_max      years
----------  --------  ---------  ---------  -------  --------  ------  -----  -----  ---------
d           SIG       65Zn        243.94 d        6        10     229   2.77   8000  1991-2015
d           SIG       64Cu       12.7004 h        9        14     199   1.49   8000  1950-2026
d           SIG       62Zn         9.193 h        5         9     104  17.18   8000  1950-2015
d           SIG       63Zn         38.47 m        5         6      96    4.5    132  1950-2019
d           SIG       61Cu         3.343 h        6        10      73  15.49   8000  1950-2026
d           SIG       65Ni        2.5175 h        4         7      53  15.12   8000  1950-2026
d           SIG       59Fe        44.500 d        5         9      53   5.32   8000  1950-2026
d           SIG       60Co        5.2714 y        4         8      50  13.41   8000  2006-2026
```

The column `T12` of the CSV file of the catalogue has the same values.

**Example 4: which targets, and are they stable?** The search over all targets (Section 5.2) lists the half-life of each target; a natural target has none:

```bash
python exfor_retrieve.py --find --projectiles d --product Cu-64 --quantity SIG --halflife
```

```text
target  T1/2    entries  datasets  points~  year_min  year_max
------  ------  -------  --------  -------  --------  --------
Ni-nat          4               4       41      1991      2026
Ni-64   stable  2               2       35      2007      2009
Cu-nat          9              14      199      1950      2026
Cu-63   stable  5               5       60      1963      2015
Zn-nat          5               5       68      2003      2017
Zn-64   stable  2               2       25      1963      2008
Zn-66   stable  2               2       20      1963      2003
Zn-67   stable  1               1        5      1963      1963
```

**Example 5: the half-lives in the files, and the half-life that the authors used.** With the option, the datasets file has the NUBASE half-life of each product (`product_T12`, `product_T12_s`) and the half-life that the entry itself quotes (`exfor_T12`, `exfor_T12_s`), and the `index.csv` of the ASCII files has `product_T12`:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product "Nb-92m,Zr-89" --ascii --halflife
```

```python
import pandas as pd
idx = pd.read_csv("data/Nb-93/ascii/index.csv")
print(idx[["file", "product", "product_T12", "n_points"]].head(5))
```

```text
                                               file product product_T12  n_points
Nb-93_d_89gZr_SIG_CUM_Damdinsuren1990_A0471-016.dat   89gZr    78.360 h         1
      Nb-93_d_92mNb_SIG_Avrigeanu2013_D0713-003.dat   92mNb    10.116 d        25
   Nb-93_d_89gZr_SIG_M+_Avrigeanu2013_D0713-005.dat   89gZr    78.360 h         6
       Nb-93_d_92mNb_SIG_Tarkanyi2007_D4156-003.dat   92mNb    10.116 d        43
        Nb-93_d_89Zr_SIG_Tarkanyi2007_D4156-006.dat    89Zr    78.360 h        24
```

The datasets file of the retrieval of Example 1 lets you find the datasets in which the authors used another half-life than NUBASE, for example before renormalising or comparing them:

```python
import pandas as pd
ds = pd.read_csv("data/Nb-93/EXFOR_NB-93_datasets.csv")
ds = ds[ds["exfor_T12_s"].notna() & ds["product_T12_s"].notna()].copy()
ds["ratio"] = ds["exfor_T12_s"] / ds["product_T12_s"]
diff = ds[(ds["ratio"] - 1).abs() > 0.02]
print(len(ds), "datasets quote a half-life;", len(diff), "differ from NUBASE by more than 2 per cent")
print(diff[["product_label", "entry", "first_author", "year", "exfor_T12", "product_T12"]])
```

```text
39 datasets quote a half-life; 2 differ from NUBASE by more than 2 per cent

product_label entry   first_author  year exfor_T12 product_T12
         87mY A0471 Ts.Damdinsuren  1990    12.9HR     13.37 h
        93mMo D4156     F.Tarkanyi  2007    6.58HR      6.85 h
```

The two cases are the 87mY data of Damdinsuren 1990 (12.9 h against 13.37 h, 3.5 per cent) and the 93mMo data of Tarkanyi 2007 (6.58 h against 6.85 h, 4 per cent). `exfor_T12` is written as in the entry, with the unit of EXFOR (`HR` hours, `D` days, `MIN`, `SEC`, `YR`). The other 37 datasets agree with NUBASE within 2 per cent. The plots of Section 14.12 show the half-lives in their titles.

**Example 6: the light particles.** The particles that are products have their half-lives too: the neutron (n, the free neutron), the proton (p), the deuteron (d), the triton (t), 3He and the alpha particle. Protons on 7Li:

```bash
python exfor_retrieve.py --target Li-7 --projectiles p --quantity SIG --halflife
```

```text
Points by product (top): 7Be (T1/2 53.22 d): 1602, alpha (stable): 877, 7Li (stable): 404, 8Be (T1/2 81.9 as): 321, n (T1/2 609.8 s): 115, t (T1/2 12.32 y): 37, 6Li (stable): 11, none: 6
```

In the table of `--summary-only` the same products have the column `T1/2` (`alpha stable`, `n 609.8 s`, `t 12.32 y`), and 3He, p and d are `stable` (for example in 12C with alpha particles). The half-life of the neutron is that of the free neutron. The datasets file and the `index.csv` of the ASCII files have them too, and the titles of the plots: `7Li(p,x)n (T1/2 = 609.8 s)` and `7Li(p,a)α (stable)` in the figure (Section 14.12). Products that are not a nuclide have none: a photon (gamma), `none`, and the products given row by row in a table (fission yields). `8Be`, which decays at once into two alpha particles, has a half-life of 81.9 as (attoseconds), as in NUBASE2020.

## 10. Interpreting the results: good practice

The script retrieves what is in EXFOR; deciding which data to trust remains with you. Ten things to check before using the tables:

- **Duplicates and superseded data.** The same measurement can appear several times: in its original entry, in a later compilation or in a revised entry. Check the `status` column and the reference before counting datasets as independent, and see Section 10.1 for the status codes (SPSDD superseded, DEP dependent on another subentry, and others) and for which of them to exclude.
- **Number of datasets is not number of independent measurements.** Several datasets from one group usually share technique, monitor reactions and decay data, so their agreement does not rule out common systematic effects.
- **Mixed quantities.** With many projectiles the table contains cross sections, angular distributions, spectra, yields, transmissions and resonance parameters. Always filter on `quantity` (for example SIG) and on `value_unit` before plotting or averaging.
- **Cumulative and independent cross sections.** Look at the `branch` column. A cumulative cross section includes feeding from decaying precursors and is not comparable with an independent one.
- **Natural targets.** Cross sections for Ti-nat or Cu-nat refer to the natural element, so they cannot be compared directly with cross sections on single isotopes.
- **Units.** Check `raw_unit` when `value_unit` is not mb. Spectra and angular distributions have different units from cross sections.
- **Complex reactions.** Rows with `reaction_type` = complex combine several reactions (ratios, sums, differences); do not treat them as cross sections without reading the entry. A sum in which a term has a target that is a compound (polyethylene, uranium oxide, a carbon compound) is complex too; builds before the fix of 2026-10-07 read it as a simple reaction on the first term (Section 16.8).
- **Always plot before using the data.** EXFOR contains typing errors, outliers and very old data. For example, a copper dataset contains a value about ten times higher than its neighbours at one energy.
- **Uncertainties.** Most entries give one total uncertainty and no correlations. Absence of `err_stat` and `err_sys` does not mean that there are none.
- **Decay data.** Half-lives and gamma-ray intensities used by the authors are not extracted. They are in the DECAY-DATA field of the raw entry.

### 10.1 Status codes: which data to exclude

Every subentry of EXFOR has status codes. The programs keep them in the column `status` of the data and datasets files (separated by commas), and the pointers that some codes carry in the column `status_ref` of the datasets file, for example `SPSDD>D4046006`. The option `--exclude-status` removes the datasets that have a code.

| Code | What it says | How common in the library | What to do |
| --- | --- | --- | --- |
| `SPSDD` | Superseded: the data were replaced by newer data, named in the pointer, for example `(SPSDD,D4046006)`; sometimes only the reference of the new publication is given | 3,764 subentries in 852 entries (about 3 per cent of the entries) | Exclude in a final analysis or figure (`--exclude-status SPSDD`) |
| `DEP` | Dependent: the data depend on another subentry, for example they were derived from it or normalised with it | 21,284 subentries in 3,926 entries | Do not exclude as a rule: many are valid measurements (see below) |
| `OUTDT` | Outdated | 293 subentries in 87 entries | Consider excluding, as for SPSDD |
| `PRELM` | Preliminary | 630 subentries in 321 entries | Check whether final data of the same work exist |
| `CURVE` | The data were read from a curve of the publication, not from a table | 30,467 subentries in 6,717 entries | Keep, but know that the precision is lower |
| `TABLE`, `APRVD` and others | The data come from a table; approved by the author | very many | Nothing to do |

The counts are for the whole library of the snapshot of October 2026. The meaning of `SPSDD` and `CURVE` I confirmed from the text of the entries; for `DEP`, `OUTDT` and `PRELM` I give the usual reading and what the entries I looked at show, and I did not check them against the EXFOR dictionary.

**Should I always exclude SPSDD?** For a final analysis or a figure, as a rule yes: superseded data are an earlier version of data that are in EXFOR again, usually by the same authors, and counting both double-counts the measurement. It costs little, because there are few of them. In the tests: none in 93Nb(d,x), 208Pb(γ,n)207Pb or 209Bi(α,2n)211At; 65 points of one dataset in natTi(d,x) for 48V (12 datasets and 436 points become 11 and 371); 24 points and one entry in 100Mo(p,x)99mTc (382 points from 12 entries become 358 from 11); 44 points of 65Zn in natCu(d,x). But look before you decide, in these cases:

- **The replacement may not be in your selection.** The pointer names it (`status_ref`): for 48V in titanium it is a subentry of the same entry (`D4046006`); for the 99mTc data of Takacs 2003 it is entry `D4322`. If you retrieved only some projectiles, products or quantities, the replacement may be missing, and excluding the old data leaves a gap.
- **The old data may cover more.** A superseded dataset can reach an energy or a product that the new one does not; compare the energy ranges (`E_min_MeV`, `E_max_MeV` of the datasets file).
- **For a study of the history of the data** (how a cross section changed, or the dispersion between versions) keep them.

To see which datasets are superseded in a retrieval and where the replacement is:

```python
import pandas as pd
ds = pd.read_csv("data/Ti-nat/EXFOR_TI-0_datasets.csv")
sp = ds[ds["status"].str.contains("SPSDD", na=False)]
print(sp[["entry", "subentry", "first_author", "year", "product", "n_points", "status_ref"]])
```

In the test this prints one dataset: entry D4046, subentry D4046002, S.Takacs 1997, the product 48V, 65 points, `SPSDD>D4046006`. With `exfor_plot.py` the effect of the filter is seen with `--list`: run the command with and without `--exclude-status SPSDD` and compare the number of points and of entries.

**Where the filter acts.** The filter is an option of the plotting program only. `exfor_retrieve.py` has no status filter: it keeps every dataset in the data files and records the status, so the saved data can serve several figures with different choices. `exfor_plot.py` retrieves the data itself when you give `--target` (or a `--data` path that does not exist yet), so one command is enough: `python exfor_plot.py --target Mo-100 --projectiles p --product Tc-99m --exclude-status SPSDD`. The filter then acts on what is plotted, and also on the files written by the same command with `--ascii` and `--references`. In the test with 100Mo(p,x)99mTc, the command without the filter gives 382 points from 12 entries, 15 ASCII files and 12 references; with `--exclude-status SPSDD` it gives 358 points from 11 entries, 14 ASCII files and 11 references (the superseded entry D4115 is not in the files or in the reference list). The data file saved by both commands has all 382 points, with D4115. The ASCII files and the reference list written by `exfor_retrieve.py` (`--ascii`, `--references`) are made from everything it retrieved, superseded data included; if you want them without superseded data, write them with `exfor_plot.py ... --exclude-status SPSDD --ascii --references`.

A complete example, with the commands, their messages and the reference that disappears, is in Section 5.3: the data, the ASCII files and the references of 100Mo(p,x)99mTc with and without the superseded data.

**Do not exclude DEP as a rule.** A `DEP` dataset is not a duplicate; it depends on other data of the entry. In 197Au(n,x) with the quantity SIG there are 107 such datasets (12 per cent of 868), 96 of them dependent on a subentry of their own entry, and they include total cross sections and derived quantities. In a capture plot of 197Au(n,γ) (`--product Au-198 --process G`) excluding `DEP` removes 88 of the 10,770 points and 9 of the 99 entries; in other selections more is lost. Exclude it only if you have a reason, for example to leave out quantities derived from other data of the same entry.

**Retrieve again if your data are older.** Versions of the programs before this build read a status code only when it was written alone, `(SPSDD)`. In EXFOR 97 per cent of the SPSDD marks (3,645 of 3,764 subentries) have a pointer, `(SPSDD,D4046006)`, and so had no effect with `--exclude-status SPSDD`; the same holds for `DEP` (21,206 of 21,284) and `COREL`. `exfor_plot.py --data` reads the status from the data files, so **data files that were retrieved with an older version must be retrieved again** (delete the folder, or run `exfor_retrieve.py` again) before `--exclude-status` works on them. The datasets file has the new column `status_ref`; the data file keeps its columns.

### 10.2 Half-lives of the isotopes (NUBASE2020)

**What is printed.** The half-life is printed only when you ask for it with the option `--halflife` (in `exfor_retrieve.py` and in `exfor_plot.py`; `--halflife-db`, which gives the file, switches it on too). The programs then print the half-life next to the isotope when the data are retrieved; stable isotopes are marked `stable`. For the deuteron data on 93Nb (`python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --halflife`):

```text
Target 41-NB-93 (stable): 60 datasets, 441 data points
Points by product (top): 93mMo (T1/2 6.85 h): 120, 92mNb (T1/2 10.116 d): 90, 89Zr (T1/2 78.360 h): 34, 90mY (T1/2 3.226 h): 30, ...
```

With the option the half-life appears in the summary of `exfor_retrieve.py` (the target and the products; a column `T1/2` with `--summary-only`), in the catalogue of `--available` (a column `T1/2`, and `T12` in the CSV file), in the table of `--find` (the target), in six columns of the datasets file (below), and in the column `product_T12` of the `index.csv` of the ASCII files. In the titles of the plots made by `exfor_plot.py` it is in parentheses next to the isotope name: that of the product always (`(stable)` for a stable one) and that of the target when it is radioactive, for example `93Nb(d,x)92mNb (T1/2 = 10.116 d)` and `235U (T1/2 = 704 My)(n,f)`. The light particles that are products get their half-lives like any other nuclide: n (the free neutron, 609.8 s), p, d, 3He and alpha (stable) and t (12.32 y); a photon (gamma) has none. With saved data the plotting program takes the half-lives from the datasets file, or from the database if the file has none. The values of this section were obtained with a database that I built from the NUBASE2020 file to test the programs, not with the database of your installation (see "Check it on your database" below).

**Source and citation.** The half-lives are those of the NUBASE2020 evaluation. Cite it when you publish results that show or use them: F. G. Kondev, M. Wang, W. J. Huang, S. Naimi and G. Audi, The NUBASE2020 evaluation of nuclear physics properties, Chin. Phys. C 45, 030001 (2021). The data are distributed at https://www.anl.gov/phy/atomic-mass-data-resources.

**The database.** The programs read the SQLite file `nuclear_halflives.db` (table `halflives`, made by `build_halflife_db.py`; the columns used are `z`, `a`, `state`, `state_idx`, `exc_energy_kev`, `half_life` and `unit`). They look for it, in this order, in the option `--halflife-db`, in the constant `HALFLIFE_DB_DEFAULT` at the top of the half-life section of `exfor_retrieve.py` (empty in the repository), in the environment variable `EXFOR_HALFLIFE_DB`, and next to the script. The file is opened for reading only. Without the option `--halflife` the database is not opened and the output is the same as before; with the option and no database the programs print one note and carry on without half-lives.

**Making and updating the database.** The repository contains the two programs that make and query the file. Download the NUBASE table `nubase_4.mas20` (from https://www-nds.iaea.org/amdc or https://www.anl.gov/phy/reference/nubase-2020-nubase4mas20) and run `python build_halflife_db.py /path/to/nubase_4.mas20` (the `.txt` suffix is optional; `--out-dir` chooses the folder of `nuclear_halflives.db` and `nuclear_halflives.dat`). When a new evaluation is published, run it again on the new file, then check the result with `python exfor_retrieve.py --check-halflives --halflife-db /path/to/nuclear_halflives.db`. `python lookup_halflife.py 99mTc` (also `Al-28`, `242mAm`, `13028`; `--db FILE` or `EXFOR_HALFLIFE_DB` choose the file) prints the half-lives of a nuclide and its isomers.

**Which half-life belongs to the state in EXFOR?** EXFOR gives the state of a product as `G` (ground state), `M`, `M1`, `M2` ... or no state, while NUBASE lists, for one nuclide, the ground state and every isomer down to about 100 ns, so there are several half-lives to choose from. The rule used is:

| State in EXFOR | NUBASE state used |
| --- | --- |
| `G` | The ground state |
| No state (for example `92Nb`) | The ground state; the column `product_T12_basis` says that EXFOR gave no state |
| `M` or `M1` | The isomer of lowest excitation energy whose half-life is 1 ms or more |
| `M2`, `M3` | The second, the third such isomer |
| `G+M1`, `M+`, `L` and other codes | None: no half-life is given |

The isomers shorter than 1 ms are skipped because an activation or a decay measurement cannot see them, and the metastable state of the EXFOR products is the one that is measured. The rule comes from a comparison with what the authors themselves quote: the field `DECAY-DATA` of the EXFOR entries gives the half-life of the products used in the analysis (2,181 nuclide and state combinations in 5,410 entries). The results:

- **Ground state.** The NUBASE ground state agrees with the half-life quoted in the entries (within 40 per cent) for 96 per cent of the 376 nuclides with the state `G`. For products without a state, 580 of the 630 nuclides that have isomers agree with the ground state, and 13 with an isomer.
- **The lowest isomer is not always the right one.** For 25 nuclides the state `M` of EXFOR is not the isomer of lowest energy of NUBASE, because NUBASE lists isomers of nanoseconds or microseconds below it. Example: 110Ag has an isomer of 660 ns and one of 249.863 d; the activation product 110mAg is the second. Taking the lowest isomer would be right for 93.0 per cent of the nuclides in which any NUBASE state agrees with the entries (344 of 370); taking the lowest isomer of 1 ms or more is right for 98.9 per cent (366 of 370). With another limit the agreement is 95.9 per cent for 1 microsecond, 98.6 per cent for 10 ms and for 0.1 s, and 92.7 per cent for 1 s.
- **The number of the isomer.** The states `M1` and `M2` follow the same order, with the isomers of 1 ms or more counted.

**When more than one isomer is possible.** If the nuclide has more than one isomer of 1 ms or more, the choice is not certain. The program then looks for the half-life that the entry itself quotes (`DECAY-DATA`, present in 23 per cent of the entries) and takes the isomer whose NUBASE half-life is closest, within a factor of 2: `chosen with the half-life given in the EXFOR entry`. If the entry quotes none, it takes the number given by the rule and marks the half-life with `?` in the console, the datasets file and the titles of the plots. This is the case of 116In produced from 115In with neutrons:

```text
Points by product (top): 116In-M1+M2: 115, 116m1In (T1/2 54.29 m): 93, 116In (T1/2 14.10 s): 73, 116mIn (T1/2 54.29 m): 14, 116gIn (T1/2 14.10 s): 10, 116m2In (T1/2 2.18 s): 9
```

The entries of this selection quote 54.41 min, 53.73 min and 3,247 s for 116mIn (NUBASE 54.29 min, the isomer `m` at 127.267 keV) and 2.2 s and 2.16 s for 116m2In (the isomer `n` at 289.66 keV, NUBASE 2.18 s); the sum `116In-M1+M2` has no half-life. Without such values, the datasets with the state `M` of this nuclide would carry `54.29 m?`.

**Columns of the datasets file.**

| Column | Content |
| --- | --- |
| `product_T12` | NUBASE half-life of the product, for example `10.116 d`, `stable`; a `?` at the end means that more than one isomer was possible |
| `product_T12_s` | The same in seconds (empty for a stable nuclide) |
| `product_T12_basis` | How the state was chosen, for example `isomer m 135.5 keV (the only isomer with T1/2 >= 1 ms)` |
| `exfor_T12`, `exfor_T12_s` | The half-life quoted in the entry for the product, as written (`10.15D`) and in seconds |
| `target_T12` | NUBASE half-life of the target (`stable` for 93Nb); empty for a natural target |

**Check it on your database.** `python exfor_retrieve.py --check-halflives` (about a minute) compares the assignment with the half-lives quoted in all the entries and prints the agreement for each state. With the test database built from the NUBASE2020 file it gave:

| State in EXFOR | Nuclides | Rule alone | With the half-life of the entry |
| --- | --- | --- | --- |
| `G` | 376 | 96.0% | 96.0% |
| none | 1,228 | 91.6% | 91.6% |
| `M` | 345 | 94.2% | 95.1% |
| `M1` | 45 | 88.9% | 91.1% |
| `M2` | 31 | 87.1% | 93.5% |

The agreement is not 100 per cent in part because the authors do not always use the evaluated half-life or the state they declare. Run the command with your own database: if its layout is different from the one described above, the command fails or gives other numbers.

**Limits.**

- Products given row by row in a table (fission yields) have no half-life in the datasets file; in the console they get one when they are listed with Z and A.
- There is no half-life for a sum of states, a level or a natural target.
- In three cases the EXFOR state `M` agrees with the NUBASE ground state (104Nb, 124In, 146La), where NUBASE marks the order of the ground state and the isomer as uncertain or reversed; the rule gives the isomer.
- The half-life is that of the state itself. It is not the half-life that matters for a cumulative yield (the chain), and no data are corrected with it.
- The NUBASE2020 value can differ from the one used by the authors, for example 78.360 h for 89Zr against 78.4 h in the entries of Takacs and Ditroi: use the same half-life when you compare or renormalise datasets. The uncertainties of the half-lives are in the database and are printed by `lookup_halflife.py`; the programs here do not print them.

**Examples.** Retrieval, catalogue, target search and the files with half-lives: Section 9.9. Titles of the plots: Section 14.12. Selecting the products of a reaction by half-life, for the production of radionuclides: Section 18.1. If nothing is printed: Section 11.

## 11. Troubleshooting

Most problems come from the git download, from the projectile string, or from output that is too large.

| Problem | Cause and solution |
| --- | --- |
| `git: command not found`, or the clone fails | Install git, or let the script use the zip fallback. If a firewall or proxy blocks GitHub, set the proxy for git (`git config --global http.proxy ...`) or download the zip from the repository page in a browser (Code > Download ZIP), unzip it and run the script with `--master` pointing to the unzipped folder (it must contain `exforall`). |
| `Cannot interpret target` | Use one of the accepted notations (Nb-93, 93Nb, 41-NB-93, Ti-nat). The symbol must be a valid element symbol. |
| `unknown projectile '...'` | The name in `--projectiles` is not recognised. Run `python exfor_retrieve.py --list-projectiles`. Heavy ions are written 12C, C-12 or 6-C-12; for an element wildcard use `C-*` or `C*`. |
| `unknown product '...'` | The name in `--product` is not recognised. Write nuclides as Nb-92m, 92mNb, 41-NB-92-M or Zr-89; elements need a wildcard (`Zr-*`, not `Zr`); particles are n, p, d, t, he3, a, g. |
| `expected one argument`, when using an exclusion | A string starting with a minus sign is read as an option. Write `--projectiles=-n` or `--product=-n`, or put `all` first: `--projectiles all,-n`. |
| 0 datasets for the target | Check the isotope: natural targets (Ti-nat) and single isotopes (Ti-48) are different EXFOR targets. Check the projectile selection too, for example run once with `--projectiles all --summary-only`. EXFOR may simply have no data for that combination. |
| 0 datasets with `--product` | The product may be written with another state: use the nuclide without m or g (`Nb-92`) to match every state. EXFOR may give no product for the reaction (try `none`), or the product may be a column of the data table. Run without `--product` and with `--summary-only` to see the products available. |
| `Scanned 0 entries` | The `--master` folder does not contain `exforall`. Point `--master` to the correct folder or delete the folder and let the script download it again. |
| The output is huge or Excel cannot open it | Too many projectiles or quantities. Restrict `--projectiles` (for example `all,-n`), `--product`, `--quantity SIG` and `--emin`/`--emax`, or work with pandas. |
| `warning: N points have the incident energy in the unit '...'` | Those points have an energy in a unit that is not converted; `E_MeV` is empty. The original unit is in `E_unit` and the value in the entry. |
| The search is slow | The whole library is scanned each time. Use a faster disk (SSD) and more cores (`--jobs`). |
| `warning: could not parse <file>` | One entry has an unusual layout. The script skips it and continues. Report the entry number and consult the raw file. |
| Excel shows one column or strange characters | Import with Data > From Text/CSV, comma delimiter and UTF-8 encoding (Section 8.1). |
| Expected data are missing | The repository lags the EXFOR website for very recent submissions; run with `--update`. Also check the quantity filter: it matches exactly (SIG does not include SIG/RAT). |

Problems that are explained elsewhere in the manual: updating the EXFOR master files (`--update skipped`, no git, a ZIP copy) is in Section 3.2, step 4; the plotting program (`does not exist`, `unrecognized arguments`, no data found, an older script) is in Section 14.5; and which folder the programs use is in Section 3; the ASCII files of --ascii (the \[?\] unit, the limit of files) in Section 8.6.

**No half-lives are printed.** Check three things. First, the option `--halflife` (or `--halflife-db`) must be given: without it nothing about half-lives is printed or written. Second, if the option is given and the programs print the note `--halflife: no half-life database (...)`, the database file was not found (give it with `--halflife-db`) or has another layout; the text in parentheses says which (for example `no such table: halflives`). Third, the datasets file has the half-lives only if the data were retrieved with the option; the plotting program takes them from the database otherwise. A half-life followed by `?` is not an error: several isomers were possible (Section 10.2). `python exfor_retrieve.py --check-halflives` tests the database against the half-lives that the EXFOR entries quote.

## 12. Reproducibility and citation

Record the version of the EXFOR library you used. From the master folder:

```bash
git -C exfor_master log -1 --format="%H %cd"
```

`python exfor_retrieve.py --master-info` gives the same and also the date of the latest data update and whether GitHub has a newer snapshot (Section 3.2). Each retrieval prints the date of the master files it used.

If you publish results that show or use the half-lives printed by the programs, cite the NUBASE2020 evaluation: F. G. Kondev, M. Wang, W. J. Huang, S. Naimi and G. Audi, The NUBASE2020 evaluation of nuclear physics properties, Chin. Phys. C 45, 030001 (2021) (Section 10.2).

When publishing results obtained with the script:

- Cite the original publications of the datasets you use (`reference` column).
- Cite EXFOR: N. Otuka et al., Nucl. Data Sheets 120 (2014) 272, [DOI 10.1016/j.nds.2014.07.065](https://doi.org/10.1016/j.nds.2014.07.065); and *The experimental nuclear reaction data (EXFOR): Extended computer database and Web retrieval system*, Nucl. Instrum. Methods A 888 (2018) 31, [DOI 10.1016/j.nima.2018.01.045](https://doi.org/10.1016/j.nima.2018.01.045).
- Mention the EXFOR master files of the IAEA Nuclear Data Section ([github.com/IAEA-NDS/exfor\_master](https://github.com/IAEA-NDS/exfor_master)) and the snapshot date.

## 13. Limitations

The script has been tested on a limited set of targets and does not guarantee the correctness of EXFOR data.

- One target isotope (or natural element) per run; isomeric targets cannot be selected.
- Data are selected by target. Reactions in which your isotope is the projectile (inverse kinematics, for example 6He or 93Nb beams on hydrogen or carbon targets) are not returned; they appear when you search for the target they hit.
- Targets given inside the data table (not in the reaction field) are not handled.
- Tested on 93Nb, 55Mn, natTi, natCu, 63Cu, 56Fe, 238U, 140Ce, 46Ti and 45Sc with different projectile selections, and, for the spectra, the ASCII files, the axis labels and the half-lives, also on 27Al, 9Be, 7Li and 235U. Results for deuterons, protons, 3He and alphas were compared with EXFOR exports from the IAEA web interface. Neutron, photon, heavy-ion, pion and other data were checked for consistency of the parsing and the energy conversion, not entry by entry against the web interface. Product selection was tested on 93Nb, natCu, 208Pb, 235U and 238U, including fission-fragment tables. Unusual entry layouts may be skipped or incompletely parsed.
- No covariance information and no evaluated data are retrieved. The half-life of a nuclide, when you ask for it with `--halflife`, is the one of NUBASE2020; the half-life that an entry quotes in its `DECAY-DATA` field is read only to choose between isomers (Section 10.2).
- The uncertainties that the programs use are the total (`ERR-T` or `DATA-ERR`), the statistical (`ERR-S`) and the systematic (`ERR-SYS`) uncertainty of the value, and the uncertainty of the incident energy. The partial uncertainties `ERR-1`, `ERR-2` ... and the uncertainties of the angle and of the outgoing energy are not used; they stay in the column `extra` of the data file. A dataset that has no uncertainty in EXFOR has none in the files and no error bars (Section 8.6.5).
- The labels of the axes and the names of the columns of the ASCII files follow the EXFOR quantity codes and units, but the program has names for only 17 of the 104 codes in use (the others are shown as their code), takes the particle of an outgoing energy from the modifier or the process of the reaction, and writes dσ/dE (mb/MeV) for the cross sections that are neutron, proton, deuteron, triton, 3He or alpha spectra (7 subentries in the EXFOR snapshot of the tests). These are inferences, described in Section 14.13; `--xlabel` and `--ylabel` replace the labels.
- The assignment of a half-life to an isomer (the EXFOR states M, M1 and M2) is a rule that agrees with the half-lives quoted in the entries for 87 to 96 per cent of the nuclides, depending on the state (Section 10.2); a half-life followed by `?` is not certain.
- `--angle-labels` and `--energy-labels` label an evenly spaced selection when there are more distributions than can be labelled one above the other, about 25 to 30 in a plot of the usual size (Section 16.5).
- The script retrieves what is in EXFOR and does not guarantee that the data are correct.

## 14. Plotting the selected data (exfor\_plot.py)

`exfor_plot.py` draws the data selected with the same options as `exfor_retrieve.py` as excitation functions: one plot (one file) per target, projectile and product, one series per dataset, with error bars.

### 14.1 Requirements and use

- Python 3.8 or later and matplotlib (`pip install matplotlib`).
- Keep `exfor_plot.py` in the same folder as `exfor_retrieve.py`; it uses its parsers. The two files must have the same build date (`--version`): `exfor_plot.py` checks it at the start and stops with a message if the other file is older (Section 11).

There are two ways to use it:

1. **Retrieve and plot in one step**, with `--target` and the same selection options as the retrieval script (this needs the EXFOR master files of Section 3). The retrieved data are also saved in `data/<target name>/`, as `exfor_retrieve.py` writes them, so the plots can be redone later with `--data`; `--no-save-data` skips this.
2. **Plot files already written** by `exfor_retrieve.py` or by an earlier retrieve-and-plot run, with `--data`: a file, a wildcard or a folder such as `data/Nb-93` (no master files needed; CSV files from version 2.0 of the retrieval script are accepted). If the path does not exist yet, the data are retrieved first with the options of the command line and saved at that path (Section 14.5), so `--data data/Rb-93` also works before any retrieval.

```bash
python exfor_plot.py --target Nb-93 --projectiles d --product 92mNb,89Zr,90Nb
python exfor_plot.py --data data/Nb-93 --product "Zr-*" --logy
python exfor_plot.py --target Cu-nat --projectiles d --product Zn-65,Zn-63,Zn-62 --vline 40 --format png,pdf
```

Every combination of target, projectile and product gets its own plot and its own file. The plots of each target are written to a folder named after the target, inside `--out` (default: `plots`), that is `./plots/<target name>/`:

```text
plots/Nb-93/Nb-93_d_92mNb.png
plots/Nb-93/Nb-93_d_89Zr.png
plots/Nb-93/Nb-93_p_92mNb.png
plots/Cu-nat/Cu-nat_d_65Zn.png
```

File names read `<target>_<projectile>_<product>.<format>`. Natural targets are named Cu-nat, Ti-nat, and so on. The quantity is added to the name when it is not SIG, and the reaction type for reactions without a product (`U-238_n_none_F.png`). With several targets in the input (several CSV files), each target gets its own folder. `--prefix` replaces the target name at the start of the file names; `--format png,pdf,svg` writes several formats.

### 14.2 What is plotted

- One plot, with its own file, for every target, projectile, product and quantity. The default quantity is SIG (cross sections in mb), different from the retrieval script, which keeps all quantities. A plot title reads, for example, 93Nb(d,x)92mNb.
- One series per EXFOR subentry, labelled author and year, plus the branch when given (for example CUM). The same entry has the same colour and marker in every plot. Data digitised from a curve (status CURVE) have open markers. The colours are ten dark ones that are easy to see on a white background (red, blue, green, black, magenta, purple, brown, grey, teal and dark orange; none of them is yellow), taken in this order, and the marker changes every three entries; the colours are defined in the constant PALETTE at the top of the plotting program.
- Error bars use the total uncertainty `dvalue` of the point and `dE_MeV` (the energy bars only when the x axis is the incident energy); `--no-xerr` removes the energy bars. A point that has no total uncertainty but a statistical (`ERR-S`) or a systematic (`ERR-SYS`) one gets its error bar from it, the two added in quadrature when both are given, and the program says how many points are in this case. A dataset that has no uncertainty in EXFOR has no error bars.
- The scale is linear and starts at zero; use `--logx` and `--logy` for logarithmic axes, or `--auto-axes` to let the program choose the scales and the limits (Section 14.7).
- Complex reactions (ratios, sums) are left out unless you give `--include-complex`.
- One unit is plotted per quantity: mb for SIG, otherwise the most frequent unit, or the one given with `--unit`. Cross sections that EXFOR gives multiplied by the energy (units B\*EV, B\*KEV, B\*MEV, MB\*MEV) or by its square root (B\*RT-EV, common for neutron capture in the resonance region) are first divided by it, using the incident energy, and plotted in mb; --no-convert-units drops them instead. Points in another unit and points without the plotted coordinate are dropped, and the program says how many.
- Reactions without a product (fission, total, elastic, ...) get one plot per reaction type; `--by-process` does the same for any product, and `--process F` keeps only one type.
- A plot with up to 12 series has its legend inside; with more series there is no room inside, so the labels are written to the right of the plot, in columns of up to 24 labels (`--max-legend`, `--legend none`). Select datasets with `--entries` or `--exclude-entries` to reduce the number of series.
- `--combine` puts several panels in one figure instead (Section 14.3); the combined figures of a target are written to the same folder.

### 14.3 Options

| Option | Default | Meaning |
| --- | --- | --- |
| `--target` |  | Retrieve and plot in one step, for example Nb-93 or Ti-nat. Give either `--target` or `--data`. |
| `--data` |  | CSV file(s) written by `exfor_retrieve.py`, or a folder such as `data/Nb-93` (all its `*_data.csv` files); wildcards allowed (`"data/*/*_data.csv"`). A path that does not exist yet is retrieved first: the target is taken from its name and the selection from the other options (Section 14.5). |
| `--data-dir` | data | Retrieve mode (`--target`): the retrieved data are saved in `<data-dir>/<target name>/`, as `exfor_retrieve.py` writes them. Also the place of the ASCII files of `--ascii`. |
| `--data-prefix` | EXFOR\_\<target> | Retrieve mode (`--target`): prefix of the saved data files. |
| `--no-save-data` | off | Do not save the data that are retrieved (with `--target`, or for a `--data` path that did not exist). |
| `--projectiles`, `--product`, `--product-exact` | d,p,he3,a with --target (and for a retrieved `--data` path), all with --data; all | Projectile and product selection, with the syntax of Sections 7.1 and 7.6 (including the product groups heavy and residual). |
| `--quantity` | SIG | EXFOR quantity code(s), for example SIG, DA, NU, NU/DE, PN/DE, PY, FY or DA/DE. |
| `--branch` |  | Keep only these EXFOR branch codes, for example `DL` (delayed), `PR` (prompt), `CUM`, `IND`, `CHN`. A code matches the parts of the branch, so `DL` also selects `DL/GRP`; a leading `-` excludes (`DL,-GRP` gives the delayed totals only); `none` selects data without a branch (Sections 15 and 14.10). |
| `--emin`, `--emax` | none | Limits of the incident energy in MeV. |
| --facility | none | With --target: retrieve only the entries measured at a facility (ntof, gelina or a regular expression), as in exfor\_retrieve.py. For several targets retrieve first and plot each folder with --data. Section 16.10. |
| `--entries`, `--exclude-entries` |  | Keep only, or drop, these EXFOR entries, for example `D4344,D4156`, or these subentries, for example `C3057016` (the numbers of the legend and of the datasets file; Section 16.8). |
| `--exclude-status` |  | Drop datasets with these status codes, for example `SPSDD` (superseded data). Do not drop `DEP` as a rule (Section 10.1). |
| `--process` |  | Keep only these reaction types, for example F (fission), 2N, TOT. |
| `--by-process` | off | One plot per reaction type. |
| `--include-complex` | off | Also plot complex reactions. |
| --merge-products | off | Draw the selected products of a target and projectile in one plot, not one plot for each product; the quantities that have the same unit are merged too (EXFOR units that differ only in PRD or PRT written for P are the same unit), and the legend gives the product of each series, for example \[30P\] and \[n\]. Used for the plots that put the exclusive and the inclusive neutron data together (Section 16.9). |
| `--unit` | mb for SIG | Unit to plot. Without it, cross sections are plotted in mb and every other quantity gets one plot per unit (the unit is added to the file name). |
| `--no-convert-units` | off | Do not convert cross sections given as sigma x E or sigma x sqrt(E) (units B*EV, B*KEV, B*MEV, MB*MEV, B\*RT-EV) to mb; those points are dropped instead. |
| `--x` | E | x variable: `E` (incident energy), `angle`, `Eout` (outgoing energy, for spectra), or `A`, `Z`, `N` (mass number, atomic number or neutron number of the product, for fission yields; all the products are then in one plot; Section 14.10). |
| `--at-energy`, `--tol` | none; 0.5 | Keep the points whose incident energy is within `--tol` MeV of the value (for angular distributions and spectra). Points without an incident energy are dropped. |
| `--at-angle`, `--angle-tol` | none; 5 | Keep the points measured at this angle, within `--angle-tol` degrees (angular and double-differential data; Section 16). |
| `--by-energy` | off | One plot for each incident energy (rounded to 3 significant figures). |
| `--by-angle` | off | One plot for each angle (rounded to 0.1 degree). |
| `--angle-labels` | off | All angles in one plot, each distribution labelled with its angle in a column at the right of the data, so that no label covers a point (spectra, `--x Eout`; Section 16.5). |
| `--energy-labels` | off | All incident energies in one plot, each labelled with its energy in a column at the right of the data (angular distributions, `--x angle`). |
| `--stack` | 1 | Draw all angles (`--x Eout`) or all incident energies (`--x angle`) in one plot, and multiply the distributions by F, F^2, F^3 ... in order of increasing angle or energy, for example `--stack 10`, so that they do not overlap on a logarithmic y axis. The labels are drawn only with `--angle-labels` or `--energy-labels`, which write the factors; without them a note in the plot gives the rule (Section 16.5). |
| `--map2d` | off | 2D maps instead of curves: the value as colour over two variables (`--axes`, default outgoing energy against angle), one map per dataset and value of the third variable (Sections 16.5, 16.6 and 14.10). |
| `--plot3d` | off | 3D plots instead of curves: the value as the height and colour over two variables (`--axes`), one plot per dataset and value of the third variable (Sections 16.6 and 14.10). |
| `--axes` | Eout,angle | The two variables of `--map2d` and `--plot3d`, any two of `E` (incident energy), `Eout` (outgoing energy), `angle`, and `A`, `Z`, `N` (the mass number, atomic number and neutron number of the fission product), for example `E,Eout` or `A,Z`. With a product axis the products stay together: one map for each entry, branch and incident energy (Section 14.10). |
| `--style` | surface | With `--plot3d`: `surface`, `bars` (3D histogram) or `scatter` (the points). |
| `--elev`, `--azim` | 25; -60 | With `--plot3d`: elevation and azimuth of the view, in degrees. |
| `--ebins`, `--cmap` | 40; viridis | With `--map2d` and `--plot3d`: a variable with more distinct values than this is put in this many bins (otherwise each value has its own cell; A, Z and N always have one cell for each integer), and the colour map. |
| `--logz`, `--linz`, `--zlim` | auto | With `--map2d` and `--plot3d`: logarithmic or linear colour and height scale (default: logarithmic when the values span two decades or more) and value range, for example `--zlim 1e-3,10`. |
| `--ascii` | off | Also write each plotted dataset as its own ASCII file in columns, with the units in the first row (a 2D distribution: one file with the two variables, the value and its uncertainties, the variable that labels the blocks first), in `<data-dir>/<target>/ascii/`, with `index.csv` (Sections 8.6, 8.6.3 and 8.6.5). |
| `--ascii-format` | dataset | With `--ascii`: `dataset`, `entry` or `quantity`: one file for each dataset, for each EXFOR entry, quantity and unit, or for each projectile, process, quantity and unit (Section 8.6.2). |
| `--ascii-no-blanks` | off | With `--ascii`: no blank line between the blocks of a 2D file. |
| `--ascii-dir`, `--ascii-no-errors`, `--max-ascii` | `<data-dir>/<target>/ascii`; off; 5000 | Folder of the ASCII files; leave out the uncertainty columns; maximum number of files. |
| `--references` | off | Also write the list of references of the plotted datasets, for each target, next to the plots: `<target>_references.txt` and `.bib` (Section 5.3). |
| `--ref-format`, `--ref-authors` | txt,bib; 3 | Formats of the reference list (`txt`, `bib`, `csv`) and the number of authors written in full (otherwise the first author and "et al."; 0 = all). |
| `--max-plots` | 200 | Stop instead of writing more plots than this; `--list` shows them all. |
| `--master`, `--update`, `--jobs` |  | As in the retrieval script (used whenever data are retrieved). |
| `--auto-axes` | off | Choose linear or logarithmic axes and the limits of each plot from the data (Section 14.7). |
| `--linx`, `--liny` | off | Force a linear x or y axis (useful with `--auto-axes`). With `--map2d` and `--plot3d` they act on the first and the second variable of `--axes`. |
| `--logx`, `--logy` | off | Logarithmic axes (with `--map2d` and `--plot3d`: of the first and the second variable of `--axes`). |
| `--no-zero` | off | Do not force the linear y axis to start at zero. |
| `--xlim`, `--ylim` | auto | Axis limits as two numbers, for example `0,50`. |
| `--vline` |  | Vertical dashed line(s) at these x values, for example `--vline 40`. |
| `--combine` | off | Put several panels in one figure instead of one file per plot. The combined figures of each target are named `<target>_p1`, `<target>_p2`, ..., or one multi-page PDF. |
| `--cols`, `--max-panels` | 3; 9 | With `--combine`: panels per row and per figure. |
| `--sharex`, `--sharey` | off | With `--combine`: same axis in all panels of a figure. |
| `--separate` |  | One file per plot. This is now the default; the option is kept for compatibility. |
| `--legend`, `--max-legend` | panel; 12 | Legend in each plot, once per figure (with `--combine`) or none; the legend is inside the plot up to this many series; with more, the labels go to the right of the plot, in columns. With `--combine` a panel with more series has no legend (use `--legend figure`). |
| `--no-xerr`, `--no-yerr`, `--no-errorbars` | off | Hide the energy error bars, the vertical error bars, or both (Section 14.9). |
| --halflife, --halflife-db | off; see Section 10.2 | Print the NUBASE2020 half-life in parentheses next to the isotope name in the titles of the plots: the product always (stable for a stable one) and the target when it is radioactive, for example 93Nb(d,x)92mNb (T1/2 = 10.116 d); also in the files written when data are retrieved. The database is the one of exfor\_retrieve.py; --halflife-db also switches the option on (Section 10.2). |
| `--ms`, `--alpha`, `--hollow` | 4; 0.9; off | Marker size, transparency of markers and error bars (0 to 1) and open markers (edge only). For many points use smaller, more transparent or open markers, for example `--ms 2 --alpha 0.5` (Section 14.9). |
| `--title` |  | Plot title (replaces the automatic title). |
| --xlabel, --ylabel | from the data | Text of the x and y axis labels (and of the colour bar of the maps). By default they are made from the data: the name of the quantity, its unit in readable form and, for an outgoing energy, the name of the emitted particle (Section 14.13). |
| `--format`, `--dpi` | png; 150 | Output format (png, pdf, svg or a comma list) and resolution. |
| `--out`, `--prefix` | plots; target name | Parent folder (the plots of each target go to `<out>/<target>/`) and file name prefix. |
| `--list` | off | Print the plots with their file names (series, points, x range, and the axes with `--auto-axes`) and exit without plotting. |
| `--show`, `--version` |  | Open the figure window; show the version (with the date of the last change). |

### 14.4 Examples

List what would be drawn, without plotting:

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product "92mNb,89Zr,90Nb,93mMo" --list
```

Copper products with a line at the 40 MeV deuteron energy of IFMIF-DONES, in PNG and PDF, superseded datasets removed (the files go to `plots/Cu-nat/`):

```bash
python exfor_plot.py --target Cu-nat --projectiles d --product "Zn-65,Zn-63,Zn-62,Cu-64,Cu-61" \
    --exclude-status SPSDD --xlim 0,50 --vline 40 --format png,pdf
```

Neutron-induced fission of 238U on logarithmic axes:

```bash
python exfor_plot.py --target U-238 --projectiles n --product none --process F --logx --logy --emin 1e-6
```

Angular distribution of protons on 93Nb near 5.5 MeV:

```bash
python exfor_plot.py --data data/Nb-93 --projectiles p --quantity DA --x angle --at-energy 5.5 --tol 0.3
```

SVG instead of PNG (every plot is a separate file in the folder of its target):

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product "92mNb,89Zr" --format svg
```

Several panels in one figure, with one legend per figure (the combined figures go to the same folder):

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product "92mNb,89Zr,90Nb" --combine --legend figure
```

### 14.5 Notes

- The plots show the data as they are in EXFOR; check them for outliers before drawing conclusions (Section 10). In the natural copper data, for example, an old dataset (Bartell 1950, entry P0069) lies far above the others in some channels, and one 64Cu point of Diksic 1979 (entry C1131) is about ten times too high. Remove such entries with `--exclude-entries P0069,C1131`.
- With several incident energies in one angular distribution or spectrum dataset, use `--at-energy` so that only one energy is drawn.
- `--list` shows how many series each panel has; use it to decide which entries to keep before plotting.

**Data that have not been retrieved are retrieved automatically.** A `--data` path that does not exist yet (or a folder without data files) is retrieved first. The target is taken from the name of the path (`data/Rb-93`, `data/Ti-nat`, or a file such as `data/Nb-93/EXFOR_NB-93_data.csv`) and the selection from the options of the command line (`--projectiles`, `--product`, `--quantity`, `--emin`, `--emax`). The data are saved at that path and the plots are made from them, so this works from an empty folder:

```bash
python exfor_plot.py --data data/Rb-93 --projectiles 0 --quantity PN/DE --x Eout --logy
```

The program prints that it found no data and is retrieving them (Rb-93, 828 points, in the snapshot used for the tests). Notes:

- Without `--projectiles` the retrieval default d,p,he3,a is used, and the program says so; add `--projectiles all` to retrieve everything.
- The saved files contain only the selection that was retrieved. If you later want other products, projectiles or quantities, retrieve again with `exfor_retrieve.py`, or delete the folder so that it is retrieved again with the new selection.
- Retrieval needs the EXFOR master files (Section 3); they are downloaded the first time.
- With several paths, such as `--data data/Nb-93 data/Cu-nat`, the existing ones are read and only the missing ones are retrieved.
- `--no-save-data` plots the retrieved data without saving them; `--data-prefix` is not used for these paths: the file names follow the path (`EXFOR_NB-93_data.csv`).

The message `'data/foo' does not exist ... its name does not identify a target` appears only when the name of the path is not a target (use names such as `Nb-93` or `Cu-nat`), or when a wildcard matches no file. It also lists the folders found in `data/`, and any data files left in the current folder by older versions of the retrieval script (`EXFOR_RB-93_data.csv`; give that file name to `--data`). The path is relative to the folder where you run the command.

**If you still see the older message.** Older versions of `exfor_plot.py` did not retrieve missing data. They stopped with `'data/Nb-93' does not exist ... --data reads the files written by exfor_retrieve.py ...` and an example command for Rb-93, which is only an example: it retrieves another target and does not create `data/Nb-93`. If you see this message, you are running an older script. Replace both `exfor_plot.py` and `exfor_retrieve.py` with the current versions (they must be in the same folder) and check them with:

```bash
python exfor_plot.py --version
python exfor_retrieve.py --version
```

The current versions print the date of the last change, for example `exfor_plot 1.2 (build 2026-10-07)`; an older script prints an earlier version or no build date. You can also check `python exfor_plot.py -h`: in the current version the help text of `--data` says that a path that does not exist yet is retrieved first. If you need the data before you update, retrieve the target you want, not the one in the example (`python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG`).

### 14.6 Typical workflow

1. See what exists for the target, without writing files: `python exfor_retrieve.py --target Nb-93 --projectiles d --summary-only` (it lists the products).
2. Retrieve the data you need: `python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product Nb-92m,Zr-89`. The files go to `data/Nb-93/`.
3. See what would be drawn: `python exfor_plot.py --data data/Nb-93 --list`.
4. Plot: `python exfor_plot.py --data data/Nb-93`.
5. Remove outliers, superseded or unwanted datasets with `--exclude-entries` and `--exclude-status`, and adjust the axes (`--logy`, `--xlim`, `--vline 40`).

In `--data` mode every projectile found in the file is plotted unless you restrict it with `--projectiles`; with `--target` the default is d,p,he3,a, as in the retrieval script. The plotting program needs only the CSV files for steps 3 to 5, so you can repeat them without the EXFOR master files. If you skip steps 1 and 2 and give a data/\<target> path that does not exist, the plot program retrieves the data for you (Section 14.5). The plots go to a folder named after the target (here `plots/Nb-93/`), one file per projectile and product.

To keep the data behind a figure, add `--ascii`: the plotting program then writes each plotted dataset as a text file in columns with the units in the first row, in `<data-dir>/<target>/ascii/` (Section 8.6). With `--references` the same command also writes the list of references (Section 5.3), so that one command gives the figure, its data and its bibliography (example in Section 9.8). If you also use `exfor_retrieve.py --ascii`, give the plotting program its own folder with `--ascii-dir`, because the file names are the same.

`--ascii-format entry` or `--ascii-format quantity` stack the plotted datasets in fewer files (Section 8.6.2), which is useful when a selection has thousands of datasets, for example fission yields.

### 14.7 Automatic axes (--auto-axes)

`--auto-axes` lets the program choose, for each panel, a linear or logarithmic scale for each axis and the axis limits, from the data. Every decision is printed on the screen, and `--list` shows them without plotting.

| Item | Rule |
| --- | --- |
| x scale | Logarithmic when the bulk of the points (5th to 95th percentile) spans a factor of 50 or more and all are positive; otherwise linear. Angles are always linear (0 to 180 degrees). |
| y scale | Logarithmic when the bulk of the positive values spans 3 decades or more, or when the highest value is at least 100 times the median (resonances); otherwise linear. |
| Limits | Linear x starts at 0 when the data start near zero. Logarithmic axes are rounded to whole decades. Linear y starts at 0 and ends just above the highest point, including its error bar. |
| Outliers | A few points far outside the bulk (x beyond 3 times the 95th percentile, at most 5% of the points; y beyond 4 times the 98th percentile, at most 3%) are left out of the range, so one wrong value does not flatten the plot. The panel states how many points are outside the range, including zero or negative values on a logarithmic axis. Use `--xlim` and `--ylim` to see them. |
| Shared axes | With `--sharex` or `--sharey` the decision is made on all panels of the figure together (these options apply with --combine). |
| Your settings win | `--logx`, `--logy`, `--linx`, `--liny`, `--xlim` and `--ylim` override the automatic choice for that axis; the other axis stays automatic. |

Examples:

```bash
python exfor_plot.py --data data/Nb-93 --product "92mNb,89Zr,90Nb,93mMo" --auto-axes
python exfor_plot.py --target U-238 --projectiles n --product none --process F,TOT --auto-axes
python exfor_plot.py --data data/Cu-nat --auto-axes --liny --xlim 0,50
```

What to expect, from tests on real data:

- Deuterons on 93Nb: the 89Zr panel gets a logarithmic y axis (its values span almost four decades), while 92mNb and 93mMo stay linear.
- 238U neutron fission and total cross sections are drawn on logarithmic x and y axes.
- Deuterons on natural copper: the 65Zn panel is drawn from 0 to 52 MeV and says "7 points outside the range" (the GeV data). The 64Cu panel gets a logarithmic x axis, which shows those data, and reports one point outside the range: the 64Cu value of Diksic 1979 that is about ten times too high.
- The rules are heuristics. When a choice does not suit you, override it with the options above.

### 14.8 Example: fission, total and capture of 238U

To plot neutron-induced fission (F), total (TOT) and capture (G) of 238U in the resonance region on logarithmic axes:

```bash
python exfor_plot.py --target U-238 --projectiles n --product none,U-239 --process F,TOT,G \
    --logx --logy --xlim 1e-6,1e-3 --dpi 300
```

This writes three files to `plots/U-238/`: `U-238_n_none_F.png`, `U-238_n_none_TOT.png` and `U-238_n_239U.png` (the capture plot, titled 238U(n,g)239U).

Three points to know:

- `--product none` alone does not plot capture. In EXFOR, fission and total cross sections have no product, but capture leads to 239U, so it needs the product in the selection: `none,U-239`, or `--product all` (which also draws the fission-fragment yields). If a reaction type given with `--process` has no data, the program prints a note that says so.
- Much of the capture data in the resonance region are given as the cross section times the square root of the energy (unit B\*RT-EV; for 238U about 17,000 of the 24,000 capture points). The program converts them to mb with the incident energy, and says how many points it converted. With `--no-convert-units` those points are left out.
- The energy limits are in MeV: `--xlim 1e-6,1e-3` is 1 eV to 1 keV.

### 14.9 Many points: when the markers hide each other

With thousands of points, such as the neutron capture cross section of 197Au (10,715 points from 108 series), the markers lie on top of each other and the points behind cannot be seen. There are four remedies; use them alone or together.

| Remedy | Option | Effect |
| --- | --- | --- |
| Smaller markers | `--ms 2` (or 1) | The default size is 4. Small markers overlap much less. |
| Transparent markers | `--alpha 0.5` | Overlapping points add up, so dense regions look darker and the points behind show through. The default is 0.9. |
| Open markers | `--hollow` | Only the edge of each marker is drawn. |
| No error bars | `--no-xerr`, `--no-yerr`, `--no-errorbars` | Hide the energy error bars, the vertical error bars, or both. In dense regions the bars are often what hides the points. |

In addition, the series with many points are drawn first and the sparse ones on top, so that a small dataset is not hidden under a large one (this needs no option). In the 197Au plot, with this ordering and small markers, a sparse dataset between about 1 keV and 100 keV became visible above the dense band.

```bash
python exfor_plot.py --data data/Au-197 --projectiles n --product Au-198 --process G \
    --xlim 1e-8,20 --logx --logy --ms 2 --alpha 0.6 --no-xerr
```

A good starting point is `--ms 2 --alpha 0.5 --no-xerr`; add `--no-yerr` (or use `--no-errorbars` alone) when the vertical bars still clutter the plot, and `--hollow` when you want to see the outline of overlapping markers. The program prints a note when a plot has more than 1500 points and the default marker size is still used.

If this is not enough, reduce the number of series or points: select datasets with `--entries` or leave out some with `--exclude-entries`, restrict the energy range with `--xlim` or `--emin` and `--emax`, remove superseded data with `--exclude-status SPSDD` (Section 14.5), or draw the energy ranges one at a time. For the plots of spectra and angular distributions, the options of Section 16 (`--at-energy`, `--by-angle`, `--map2d`) separate the data instead of overlaying them. Remember that transparency and the order of drawing only change how the plot looks; they do not change the data.

### 14.10 Fission yields in 2D and 3D

A fission yield depends on the product, so the axes are the properties of the fission product: the **mass number A** and the **atomic number Z** (or the neutron number N = A minus Z), with the yield as the value; and, if the dataset has several beam energies, the **incident energy E**. The plotting program has `A`, `Z` and `N` as axes next to `E`, `Eout` and `angle`. What you can draw depends on what the dataset gives:

| The dataset gives the yield against | Plot | Axes | Option |
| --- | --- | --- | --- |
| A | 2D curve: the mass-yield curve | x = A, y = yield | `--x A` |
| A and Z | 2D map: the chart of the fission products | x = A (or N), y = Z, colour = yield | `--map2d --axes A,Z` (or `N,Z`) |
| A and Z | 3D plot | x = A (or N), y = Z, height and colour = yield | `--plot3d --axes A,Z` |
| E and A | 2D map and 3D plot: the mass-yield curve against the energy | x = E, y = A, colour or height = yield | `--map2d --plot3d --axes E,A` |

The examples were run on the 235U(n,f) data of the test snapshot; retrieve them first (`python exfor_retrieve.py --target U-235 --projectiles n --quantity FY`). Do not mix the branches (`--branch`) or the units (`--unit`) in one plot.

**Why the examples name an entry, and how else to choose the data.** The maps and 3D plots draw **one dataset at a time**: one map for each entry, branch and incident energy. The program does not average datasets from different laboratories into one picture, because that would hide the cases in which they disagree. A selection is therefore needed to limit the number of maps; `--entries` is only one way of making it. For 235U(n,f) with the quantity FY, without any selection there are 110 maps from 49 entries (92 of cumulative yields, 12 of independent yields, and a few of other branches; 4 of them are maps of isomers; the units are kept apart), more than anyone wants to look at. If more than `--max-plots` (default 200) maps would be written, the program stops and says so. The option --list tells the number before anything is drawn (see below). These selections were tested:

| You give | Result |
| --- | --- |
| `--entries 10722 --branch IND --unit PC/FIS` | 1 map, the dataset of the entry |
| `--branch IND --unit PC/FIS --at-energy 2.53e-8 --tol 1e-8` | 3 maps: the independent yields at the thermal energy of entries 10722 and 13600 (entry 13600 gives a second map for its isomers) |
| `--branch IND --unit PC/FIS` | 9 maps: every dataset of independent yields that has Z and A (one of them a map of isomers) |
| `--branch CUM --unit PC/FIS` | 90 maps: the cumulative yields (3 of them maps of isomers) |
| only `--quantity FY` | 110 maps from 49 entries, below the limit `--max-plots` of 200 (every branch and unit, each in its own map) |

`--branch` and `--unit` are needed in any case: independent, cumulative, chain and prompt yields are different quantities, and the units differ between datasets, so they cannot share a plot. A dataset that gives only one value of Z or of A cannot make a map; the program lists it (`needs at least 2 distinct A and 2 distinct Z values`) and goes on.

The mass-yield curve with `--x A` needs no entry at all: it puts all the selected datasets in one plot, one series for each dataset, so that they can be compared (the independent yields at the thermal energy: `--branch IND --unit PC/FIS --at-energy 2.53e-8 --tol 1e-8 --x A --logy` gives 142 points from 3 entries). To compare two datasets on a map, draw them one by one with `--entries`; to compare many at once, use the curve.

**How many entries and maps will there be? Ask before drawing.** Two commands tell it without writing anything:

```bash
# what EXFOR has: the entries and datasets of the selection made at retrieval (target, projectiles, product, quantity)
python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --available --summary-only

# what will be drawn: add --list to the plotting command (the filters --branch, --unit, --at-energy, --entries count)
python exfor_plot.py --data data/U-235 --projectiles n --quantity FY --branch IND --unit PC/FIS \
    --at-energy 2.53e-8 --tol 1e-8 --map2d --axes A,Z --list
```

The first says `527 entries, 1338 datasets, 17351 data points` for the fission yields of 235U(n,f). The second prints the number of entries and then each map that would be written, with the entry, the branch, the incident energy, the points, the number of A and Z values and the file name:

```text
142 points from 3 EXFOR entries, 1 target(s).
  note: no map plot for U-235 n->fragments FY 33030 |F| E = 2.5e-08 MeV: needs at least 2 distinct A and 2 distinct Z values

3 maps from 2 EXFOR entries would be written:
entry    branch          E  points         A x Z values   file
10722    IND      2.53e-08     100              25 x 14   plots/U-235/U-235_n_fragments_FY_PC_FIS_map_A-Z_E2.53e-08_IND_10722.png
13600    IND      2.53e-08      35               23 x 8   plots/U-235/U-235_n_fragments_FY_PC_FIS_map_A-Z_E2.53e-08_IND_13600.png
13600    IND M    2.53e-08       6                6 x 4   plots/U-235/U-235_n_fragments_FY_PC_FIS_map_A-Z_E2.53e-08_IND_isomer-M_13600.png
```

The first line counts the entries that have points left after all the filters (3 here, with the energy filter applied); the listing counts the entries that make a map (2 here: the third, entry 33030, gives too few values of A and Z, and the note says so; the entry 13600 gives two maps, one for the ground state and one for the isomers, marked M). Without the energy filter the same command lists 9 maps from 8 of the 13 entries with independent yields (263 points). If the number of maps is above `--max-plots` the listing says so. For the curve (`--x A`) `--list` gives the number of plots, series and entries: the independent yields at any energy, with `--branch IND --unit PC/FIS`, are 1,369 points from 58 entries in one plot. The filters of the plotting program (`--branch`, `--unit`, `--at-energy`, `--entries`) are applied by `--list` as in a real run, but not by `--available`, which only knows the selection of the retrieval.

**The mass-yield curve.** The chain yields (`--branch CHN`) at the thermal energy, against A, on a logarithmic yield axis:

```bash
python exfor_plot.py --data data/U-235 --projectiles n --quantity FY --branch CHN \
    --at-energy 2.53e-8 --tol 1e-8 --unit PC/FIS --x A --logy
```

This draws 173 points from two entries (Ajitanand 1978 and Shmid 1983), all the fission products in one plot, as the double-humped curve of the mass distribution, with the light fragments around A = 95 and the heavy ones around A = 139. The file is `plots/U-235/U-235_n_fragments_FY_PC_FIS_E2.53e-08MeV.png`. With `--branch CUM` the points of single nuclides scatter widely (several nuclides share one mass number), so use the chain yields for the mass-yield curve.

**The chart of the fission products, in 2D and in 3D.** The independent yields of the dataset of Strittmatter (entry 10722) at the thermal energy have both Z and A:

```bash
python exfor_plot.py --data data/U-235 --projectiles n --quantity FY --entries 10722 --branch IND \
    --unit PC/FIS --map2d --axes A,Z
python exfor_plot.py --data data/U-235 --projectiles n --quantity FY --entries 10722 --branch IND \
    --unit PC/FIS --plot3d --style bars --axes A,Z
```

The map has A horizontal, Z vertical and the yield as the colour (logarithmic), one cell for each (A, Z), empty where the dataset has no value. The yields form a diagonal band of 100 nuclides from Z = 31 to 44 and A = 82 to 106. The 3D plot has the same axes with the yield as the height of a bar. `--axes N,Z` puts the neutron number N on the horizontal axis, as in the chart of the nuclides; `--style surface` draws a surface instead of bars (empty cells stay empty). The files are `..._map_A-Z_E2.53e-08_IND_10722.png` and `..._3d-bars_A-Z_E2.53e-08_IND_10722.png`. If a dataset has several incident energies there is one map for each energy, with the energy in the title and in the file name.

**The mass-yield curve against the energy.** The yields before neutron emission (`PRE`) of Straede 1987 (entry 23591) have 12 energies and 98 mass numbers in several subentries; the program groups the subentries of one entry and branch:

```bash
python exfor_plot.py --data data/U-235 --projectiles n --quantity FY --entries 23591 --branch PRE \
    --unit PC/FIS --map2d --plot3d --axes E,A
```

The map has the incident energy horizontal, A vertical and the yield as the colour: the two maxima of the mass distribution are at all the energies (yields of 6 to 7 per cent per fission), and the valley between them fills in as the energy rises: the mean yield for A from 115 to 121 grows from 0.021 per cent per fission at 0.5 MeV to 0.20 at 6 MeV. Cells without a value (a mass number that a subentry does not give) stay empty.

**With your own plotting program.** The ASCII files (Section 8.6.4) are ready for it. The nuclide yields of one dataset are one file with the columns Z, A and yield, with a blank line between the Z blocks:

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

f = "data/U-235/ascii/U-235_n_products_FY_IND_Strittmatter1977_10722-003_E2.53e-08MeV.dat"
Z, A, y, dy = np.loadtxt(f, skiprows=1, unpack=True)          # the blank lines are skipped

plt.figure()                                                # 2D: A on x, Z on y, colour = yield
plt.scatter(A, Z, c=y, norm=LogNorm(), marker="s", s=110)
plt.xlabel("A"); plt.ylabel("Z"); plt.colorbar(label="FY (per cent per fission)")
plt.savefig("fy_2d.png", dpi=110)

fig = plt.figure()                                          # 3D: bars of height y over (A, Z)
ax = fig.add_subplot(projection="3d")
ax.bar3d(A - 0.45, Z - 0.45, np.zeros_like(y), 0.9, 0.9, y, shade=True)
ax.set_xlabel("A"); ax.set_ylabel("Z"); ax.set_zlabel("FY (per cent per fission)")
plt.savefig("fy_3d.png", dpi=110)
```

Retrieve with `--ascii` first (`python exfor_retrieve.py --target U-235 --projectiles n --quantity FY --ascii`). A mass-yield file (the columns A and yield) is plotted with `plt.errorbar(A, y, yerr=dy)`. In the stacked formats (`--ascii-format quantity`, Section 8.6.2) select the rows with `entry`, `branch` and `product` first.

**Limits.** Only datasets that give the product by A, or by Z and A, can be drawn this way; yields of single nuclides given in the reaction field (not in a table) are plotted against the energy as usual, one plot for each nuclide. A map needs at least two values of each axis. The map and the 3D plot use the mean of the points that fall in a cell (one point per cell for yields). The plot of Z against A shows the products of one dataset; to compare datasets draw them one by one with `--entries`.

### 14.11 How fission yields are stored in EXFOR

This section describes the EXFOR coding that Section 14.10 and the ASCII files of Section 8.6.4 rely on. The counts are for the fission yields (quantity `FY`) of 235U(n,f) in the October 2026 snapshot: 1,346 reaction records in 1,338 datasets.

**The reaction string.** It has the form `(target(projectile,process)product,branch,quantity)`, for example:

```text
(92-U-235(N,F)ELEM/MASS,IND,FY)        independent yields of many nuclides
(92-U-235(N,F)ELEM,CHG,FY,,MXW)        charge distribution, Maxwellian-averaged
```

**How the product is coded.** The product field tells how to read the data table:

| Product coded as | Records | What the data table has |
| --- | --- | --- |
| `ELEM/MASS` | 591 | One row for each nuclide, with the columns `ELEMENT` (Z) and `MASS` (A) |
| A nuclide, for example `44-RU-101` | 551 | The yield of that one nuclide, usually against the incident energy |
| `MASS` | 185 | One row for each mass number: the mass-yield curve |
| `ELEM` | 15 | One row for each Z: the charge distribution (branch `CHG`) |

Four records have no product. The programs write the first and third kinds as one file or one map for each dataset, with the product as the independent variable; the second kind is an ordinary excitation function of one product.

**The branch tells what kind of yield it is.** The codes in 235U(n,f) are: `CUM` 765 records, `IND` 220, `CHN` 110, `TER` 105, `PRE` 43, `PAR/IND` 24, `PR/PAR` 14, `SEC` 14, `PAR/CHN` 11, `CHG` 9, `PR` 9 and `TER/PAR` 6. `CUM`, `IND` and `CHN` are the cumulative, independent and chain yields, and `CHG` the charge distribution (I confirmed the last one from the text of an entry). `PRE` and `SEC` are the yields before and after neutron emission, and `TER` ternary fission, as I understand the EXFOR dictionary; I did not check these against it. Yields of different branches are different quantities and must not be mixed.

**The data table.** The start of the table of nuclide yields of Strittmatter (entry 10722, subentry 003):

```text
MASS       ELEMENT    DATA       DATA-ERR   MONIT      MONIT-ERR
NO-DIM     NO-DIM     PC/FIS     PC/FIS     PC/FIS     PC/FIS
  82.       31.        0.011      0.005      0.321      0.009
  82.       32.        0.130      0.009      0.321      0.009
```

`DATA` is the yield and `DATA-ERR` its uncertainty; `MONIT` is the reference value to which the measurement was normalised. The usual unit is `PC/FIS`, per cent per fission; other units (`NO-DIM`, `ARB-UNITS` and others) also occur, and the programs keep them apart.

**The incident energy** is in an `EN` column, or in a block of values valid for the whole table: the thermal energy appears, for example, as `EN-DUMMY` = 0.0253 eV. Data for a reactor spectrum carry a marker at the end of the reaction string, such as `MXW` or `SPA`, as I read them a Maxwellian and a spectrum average.

**Subentries.** One subentry holds one table, and a publication has several, for example one for the mass yields and one for the nuclide yields.

**Ratios.** Some yields are coded as a ratio of two reactions, for example the yields of Shima 1978 relative to 101Ru, `((92-U-235(N,F)ELEM/MASS,CUM,FY,,SPA)/(92-U-235(N,F)44-RU-101,CUM,FY,,SPA))`. They are numbers without a unit, not yields. In 235U(n,f), 4,988 of the 17,351 `FY` points are of this kind (4,926 of them `NO-DIM`). The programs call them complex reactions and leave them out of the plots unless you give `--include-complex`; the CSV files contain them (the column `reaction_type` is `complex`).

**Isomers.** When the products are listed by Z and A, a column `ISOMER` can say which state of the nuclide the row is: 0 the ground state, 1 the first isomer, 2 the second isomer. In 235U(n,f) 997 points in 201 datasets (103 entries) have this column. The flags 1 and 2 are on nuclides with well-known isomers (85mKr, 133mTe, 132mSb, 99mNb, 91mY, 115mCd and the second isomers of 120In, 122In and 130In), which supports this reading. The programs use the flag: a row with `ISOMER` 0 has the product code `36-KR-85-G`, with 1 `36-KR-85-M` and with 2 `36-KR-85-M2` (labels `85gKr`, `85mKr`, `85m2Kr`). The totals do not change (1,338 datasets, 17,351 points), but the yields of the isomers are no longer mixed with those of the ground state:

- `--product Kr-85m` selects the isomer (16 datasets, 26 points); `--product Kr-85` selects all the states (42 datasets, 53 points).
- In the plots against A, Z or N the isomers are a series of their own (`... isomer M` in the legend). In the maps and 3D plots they are a map of their own (`..._isomer-M_...` in the file name, `M` in the listing of `--list`): in 235U(n,f) there are 4 of the 110 maps. A map of isomers needs at least two values of A and Z, so many datasets give none.
- In the ASCII files of a table of products the isomers of a dataset are a file of their own, `..._isomer-M.dat`, with the column `isomer` in `index.csv` (Section 8.6.4).
- The ground state rows with the flag 0 and the rows without the column are treated alike in the maps and the ASCII files (the state `G` is not a separate map).

In one entry (13295, Wolfsberg 1971) the column `ISOMER` holds other numbers (0.0015, 0.3, 7.7 and so on) that are not state flags; the programs ignore a value that is not a whole number from 0 to 9. The flag is also kept in the column `extra` of the data file.

**What the programs read.**

| In EXFOR | In the data file |
| --- | --- |
| `ELEMENT` and `MASS` columns | `product_Z`, `product_A`, and the product code, for example `36-KR-85-M` |
| `MASS` column only | `product_A`; the product code is `MASS-<A>` |
| `DATA`, `DATA-ERR` | `value`, `dvalue` (with the unit in `value_unit`) |
| `EN`, or `EN-DUMMY` and similar | `E_MeV` (not `EN-DUMMY`, which is kept in `extra`) |
| The branch (`CUM`, `IND`, ...) | `branch` |
| `MONIT`, `DATA-ERR1`, `DECAY-FLAG`, ... | `extra` (as text), with the units in `extra_units` |

Two limits to know. The monitor values are not used, and the fission yields given in the reaction string only by the nuclide (the second kind in the table above) are not treated as a distribution over the products but as one excitation function for each nuclide.

### 14.12 Half-lives in the titles of the plots

With the option `--halflife` the title of a plot has the half-life in parentheses next to the isotope name: the product always (`(stable)` for a stable product, also for the light particles n, p, d, t, 3He and alpha), and the target when it is radioactive. The same option and the same database as in `exfor_retrieve.py` (Section 10.2); `--halflife-db` gives the file and switches the option on too. Natural copper with deuterons, the products 64Cu and 65Zn:

```bash
python exfor_plot.py --target Cu-nat --projectiles d --product "Cu-64,Zn-65" --exclude-status SPSDD --halflife
```

This gives 385 points in 2 plots from 14 entries, and the titles

```text
natCu(d,x)64Cu (T1/2 = 12.7004 h)
natCu(d,x)65Zn (T1/2 = 243.94 d)
```

written as T with the subscript 1/2 in the figure. Without the option the titles are `natCu(d,x)64Cu` and `natCu(d,x)65Zn`; the file names and the data do not change. For a radioactive target the half-life of the target is in the title too; the cross section of 235U(n,f) with the target `235U (T1/2 = 704 My)(n,f)`:

```bash
python exfor_plot.py --target U-235 --projectiles n --process F --product none --halflife
```

**Saved data.** The plotting program takes the half-lives from the datasets file next to the data file if it has them (it has them when the data were retrieved with `--halflife`); otherwise it looks them up in the database:

```bash
python exfor_plot.py --data data/Cu-nat --projectiles d --product Cu-64 --halflife
```

**Other plots.** The maps and the 3D plots of single products (Section 16) have the half-life in their titles in the same way, for example `93Nb(p,el)93Nb (stable) [DA]` for the elastic scattering of protons on 93Nb. The plots against A, Z or N of the fission yields (Section 14.10), where many products share one plot, have none. A half-life followed by `?` means that the state `M` of the product could be more than one isomer and no half-life is quoted in the entry (Section 10.2). Without a database the plots are made as usual and one note says that no half-life was found.

### 14.13 Axis labels: quantity, unit and emitted particle

The labels of the axes are made from the data, not fixed. The y axis (and the colour bar or the vertical axis of the maps and 3D plots) has the name of the quantity and its unit; the x axis of a spectrum names the particle whose energy it is.

**Quantity and unit.** The name comes from the EXFOR quantity code and the unit is the unit of the data, written in the usual form. Before this version only the cross section had a proper label; every other quantity was written as its code and the unit as in EXFOR, for example `PY/DA/DE (P/MEVMUCSR)`.

| Quantity code | Unit in EXFOR | x axis | Label of the y axis |
| --- | --- | --- | --- |
| `SIG` | `mb` | incident energy | Cross section (mb) |
| `DA` | `mb/sr` | angle | dσ/dΩ (mb/sr) |
| `DA` | `ARB-UNITS` | angle | dσ/dΩ (arb. units) |
| `DA/DE` | `mb/sr/MeV` | outgoing energy | d²σ/dΩdE (mb/sr/MeV) |
| `PY/DA/DE` | `P/MEVMUCSR` | outgoing energy | Double-differential yield (particles/(MeV µC sr)) |
| `FY` | `PC/FIS` | mass number A | Fission yield (% per fission) |
| `NU` | `NO-DIM` | incident energy | Neutron multiplicity ν̄ (a dimensionless quantity has no unit) |
| any other code | any | any | the code and the unit as in EXFOR, for example `XYZ (FOO)` |

The quantity names known to the program are SIG, DA, DE, DA/DE, FY, NU, NU/DE, PN, PN/DE, PY, PY/DA/DE, TTY, TTY/PY/DA/DE, POL/DA, SIG/RAT, TRN and WID (other codes are written as they are). The columns of the ASCII files have the same names, in plain ASCII (Section 8.6.5). The units are rewritten from the EXFOR spelling: `MB/SR/MEV` becomes mb/sr/MeV, `MUB` µb, `SR2` sr², `PC/FIS` % per fission, `PRD/FIS` products per fission, `ARB-UNITS` arb. units, `B*EV` b·eV, `P/MEVMUCSR` particles/(MeV µC sr). A unit that the program does not know stays as EXFOR writes it; in the data of the tests these were `GAM/100N`, `MUB/SRGEVC` and `NUC/PART`.

**The particle on the outgoing-energy axis.** With `--x Eout` (and on the maps and 3D plots) the label names the particle whose energy it is: Neutron energy, Proton energy, Deuteron energy, Triton energy, 3He energy, Alpha particle energy or Photon energy. EXFOR names the particle in the field after the quantity of the reaction (`G` is a gamma ray, `N` a neutron); without that field the program takes the process, so (d,n) gives Neutron energy, or a light-particle product. When none of these tells it, the label stays Outgoing energy (MeV).

**A cross section that is a spectrum.** Some data of EXFOR are coded as cross sections (`SIG`) although they are emission spectra: the cross section is given against the energy of the emitted particle (an example is in Section 16.7). A distribution against an energy is per unit of energy, so for the quantity `SIG` without a modifier that is given with the energy of an emitted neutron, proton, deuteron, triton, 3He or alpha particle the label is dσ/dE (mb/MeV). EXFOR writes the unit of these data as `MB`; the `/MeV` is added by the program because the x axis is an energy, it is not stated in EXFOR.

**What follows the EXFOR definitions and what the program infers.** The labels follow EXFOR where EXFOR says something, and I checked how far that reaches over the whole EXFOR snapshot of the tests (137,042 subentries with a quantity code and a unit of the data):

- **The unit** is the unit that EXFOR gives for the data, only written differently (`MB/SR/MEV` as mb/sr/MeV). 1.35 per cent of the subentries (1,869, with 100 different units) have a unit that the program does not know; it stays as EXFOR writes it, for example `GAM/100N`. The only unit that is added to what EXFOR says is the `/MeV` of the emission spectra above.
- **The name of the quantity** comes from the EXFOR quantity code. The table has 17 of the 104 codes in use, which are 88.9 per cent of the subentries; the others are shown as their code with their unit. The most frequent ones without a name are `RI` (2,201 subentries), `STF` (1,161), `SPC` (1,113), `INT` (751), `KE` (630), `AMP` (562), `DA/DA/DE` (531) and `POL/DA/DE` (437). I wrote the names from my knowledge of the EXFOR quantity codes; I did not check them against the EXFOR Dictionary, which is not in the repository of master files.
- **The code and the unit are compared.** If the unit that EXFOR gives contradicts the code, the label shows the code and the unit as they are and does not give it a name, and the plotting program prints a note. This is so for 601 subentries (0.4 per cent): 568 of them have the quantity `DA` with a unit without sr (`MB` or `B`, for example in entries 10096 and 10048), 24 have `DA/DE` without sr, 7 have `SIG` with a per-sr unit and 2 have `DE` with `GAM/100N`.
- **The particle on the outgoing-energy axis** is inferred from the modifier or from the process of the reaction, as described above, not from the EXFOR data heading `E`, which only says energy.

So the labels are as reliable as the coding of EXFOR; where EXFOR is ambiguous or inconsistent, the label either shows what EXFOR writes or states what the program inferred, and `--xlabel` and `--ylabel` always override it.

The rule is narrow on purpose. In the EXFOR snapshot of the tests, 394 subentries (in 150 entries) have the quantity `SIG` with a column of outgoing energy, and most of them are cross sections for a gamma-ray line or for a discrete level, in mb, not per MeV: 288 have the modifier `G` (gamma production), 8 have another modifier (REL, DG), and 71 have none: 64 of these are reactions that do not name a single emitted particle (the process is X, 2N, 3N, F and so on) and 7 are the case below; the count could not read the coding of the remaining 27. They keep the label Cross section (mb), with the x axis Photon energy for the gamma-ray data. Only 7 subentries in 2 entries (the (d,n), (d,p) and (d,α) data of Al-Quraishi 2000 on 27Al and 56Fe, entry C1151, and one more) fall under the rule. If the rule does not suit a dataset, the label is changed with the options below.

**The label follows the data, not the x axis.** The rule looks at whether the points have an outgoing energy, so the label is dσ/dE (mb/MeV) also when these data are plotted against the incident energy, which gives vertical lines (two lines for two beam energies). When the program finds spectra plotted against the incident energy it prints a note and suggests `--x Eout --by-energy`.

**Your own labels.** `--ylabel` and `--xlabel` replace the automatic text, for example `--ylabel "cross section (mb)"`. They apply to all the plots of the command.

```bash
python exfor_plot.py --data data/Al-27 --projectiles d --product Si-28 --quantity SIG --x Eout --by-energy
```

gives the x axis Neutron energy (MeV) and the y axis dσ/dE (mb/MeV); with `--ylabel "sigma (mb)"` the y axis is the text you give.

### 14.14 Evaluated data over the EXFOR data (`--endf`)

`--endf FILE ...` draws the cross section of an evaluated nuclear data file in ENDF-6 format (ENDF/B, JEFF, JENDL, CENDL, BROND, TENDL ...) as a line over the EXFOR points of the same target and reaction. It works for neutron-induced cross sections (quantity SIG, incident energy on the x axis). The files are read by `endf_reader.py`, which must be in the same folder as `exfor_plot.py`.

```bash
python exfor_plot.py --target U-238 --projectiles n --product none --process F --logx --logy \
       --endf n_092-U-238.endf --endf-label "ENDF/B-VIII.0"
python exfor_plot.py --data data/Fe-56 --projectiles n --process TOT,EL --endf endf-b8/ jeff33/Fe056.jeff
```

- `--endf` takes files, wildcards and folders (from a folder only the files whose first material is the target of a plot are read). Several files give several lines, so that evaluations can be compared. Each line is labelled with the library and version that the file states (for example "ENDF/B-VIII.0"); `--endf-label` gives the names, one per file, in the order of the files. A file may hold several materials; the one of the plotted target is used.
- The reaction type of the plot selects the cross section (File 3, MT number): TOT 1, EL 2, NON 3, INL 4 (the sum of MT 51 to 91 if the file has no MT 4), 2N 16, 3N 17, F 18 (the sum of MT 19, 20, 21 and 38 if there is no MT 18), NA 22, NP 28, 4N 37, G 102, P 103, D 104, T 105, HE3 106, A 107, 2A 108, 3A 109, 2P 111, PA 112. Plots of other quantities, angles, spectra, natural targets or isomeric products get no line, and a note says why. The line is in the unit of the plot (mb by default).

#### Which ENDF files can be plotted

| Kind of file | Can it be plotted? |
| --- | --- |
| **Pointwise (PENDF)** neutron file: the cross sections are tabulated at all energies, resonances included (made by NJOY or PREPRO from an evaluation) | **Yes, over its whole energy range, resonances included. This is the recommended kind.** |
| **Evaluated (ENDF-6) neutron file as distributed by ENDF/B, JEFF, JENDL, CENDL, TENDL ...**, with the resolved resonances stored as parameters (File 2) | **Partly.** The line starts above the resolved resonance range, where File 3 holds the whole cross section; the resonances themselves are not drawn (the program does not reconstruct them). `--endf-full` adds the background below that range, marked as such in the legend. |
| Files of other incident particles (protons, deuterons, photons ...), thermal scattering, decay, fission yields, covariances, angular distributions or spectra (Files 4 to 6) | **No.** Only neutron-induced cross sections in File 3 (the quantity SIG, incident energy on the x axis) are read. A note says why a plot gets no line. |

So an ordinary evaluated file is accepted, but for the resonance region of a plot you need a pointwise file.

#### Where to get the files

- **Evaluated libraries** (resonance parameters, not pointwise): [ENDF/B-VIII.0 at the NNDC](https://www.nndc.bnl.gov/endf-b8.0/download.html)
  (the "Neutron Reaction" sublibrary is one zip file of about 300 MB, one ENDF-6 file per nuclide); the same files are
  in the [IAEA-NDS download area](https://www-nds.iaea.org/public/download-endf/); [JEFF-3.3 at the OECD-NEA](https://www.oecd-nea.org/dbdata/jeff/jeff33/);
  [JENDL (JAEA Nuclear Data Center)](https://wwwndc.jaea.go.jp/ftpnd/ftpnd.html); [TENDL](https://tendl.web.psi.ch/tendl_2023/tendl2023.html) (PSI).
  The file names differ from library to library; give them to `--endf` as they are.
- **Pointwise files**: make them from an evaluated file with [NJOY](https://github.com/njoy/NJOY2016) (modules `RECONR`, then `BROADR` for a temperature)
  or with the PREPRO codes of the IAEA-NDS. The result is a PENDF file. I have not found a ready-made PENDF download of these
  libraries that I could verify, so check the library's own page; if you find one, it works directly.
- A single evaluated cross section can also be retrieved from the [IAEA-NDS ENDF retrieval page](https://www-nds.iaea.org/exfor/endf.htm).

Only the NNDC download page and the IAEA-NDS ENDF/B-VIII.0 index were opened when this was written; the other links are the usual
addresses of those data centres and their layout changes, so if one fails, search the library name on the site of the data centre.

- **Resonances.** An evaluated file stores the resolved resonance range as resonance parameters (File 2); File 3 holds only the smooth background there. The program does not reconstruct the resonances, so by default the line starts where File 3 is the whole cross section: above the resolved range, and above the unresolved range when the file says that File 3 is only a background there (flag LSSF = 0). A note tells where. To see the resonances use a **pointwise (PENDF) file**, the file that NJOY or PREPRO write after reconstructing and Doppler broadening the resonances; its resonance range is tabulated in File 3 and is drawn over the whole range. `--endf-full` draws File 3 over the whole range also for a file with resonance parameters (then only the background in the resonance range, as the legend says).
- The line covers the energy range of the plotted data (a little wider), or `--emin`, `--emax`, `--xlim`; `--endf-full` uses the whole file. `--endf-lw` sets the line width and `--endf-sub` the number of points inserted in each interval that is not linear-linear (default 12). The y range still comes from the EXFOR data (`--auto-axes`) or `--ylim`; on a linear y axis the peaks of an evaluation can be far above the data.
- `python endf_reader.py FILE` prints what the reader finds in a file (materials, the cross sections of File 3 and the resonance ranges), which helps when a line is missing.
- Tested only with synthetic ENDF and PENDF files that I wrote (`python tests/test_endf.py`; an independent parser, `endf-parserpy`, reads them with the same values). It has **not** been tried on real library files, so compare your first plots with the library's own plots before relying on the lines.

## 15. Example: beta-delayed neutron spectra and neutron yields

This chapter shows how these data are coded in EXFOR and how to retrieve and plot them with the two programs. The numbers come from the EXFOR snapshot used for the tests (October 2026) and will change as EXFOR grows.

### 15.1 Beta-delayed neutron spectra of individual precursors

For an individual precursor (a fission product that emits neutrons after a beta decay), EXFOR codes the decay as a reaction without incident particle:

| Item | EXFOR coding |
| --- | --- |
| Target | The precursor, for example 93Rb (not the nucleus that emits the neutron). |
| Projectile | Code `0`: no incident particle (`--projectiles 0`). |
| Process and product | `B-` and the daughter nucleus, for example 93Sr. |
| Quantity | `PN` (neutron emission probability, also given for energy windows with the branch PAR) and `PN/DE` (the neutron spectrum). |

Retrieve and plot the spectra of 93Rb:

```bash
python exfor_retrieve.py --target Rb-93 --projectiles 0 --quantity "PN,PN/DE"
python exfor_plot.py --data data/Rb-93 --projectiles 0 --quantity PN/DE --x Eout --logy
```

For 93Rb the snapshot has 829 spectrum points from four entries (Reeder 1980, Kratz 1983, Greenwood 1985 and Rudstam 1974). The program writes one plot per unit, here `plots/Rb-93/Rb-93_none_93Sr_PN_DE_ARB-UNITS.png` (three datasets in arbitrary units) and `plots/Rb-93/Rb-93_none_93Sr_PN_DE_1_KEV.png` (Rudstam, in 1/keV). The plot title reads 93Rb(β−)93Sr \[PN/DE\].

Other precursors with `PN` or `PN/DE` data in the same snapshot include 94Rb, 137I, 87Br and 135Sb, each with several datasets. There is no list of precursors in the programs: give the precursor as the target, and use `--summary-only` to see what exists.

### 15.2 Delayed neutrons from fission

For delayed neutrons emitted after fission, the target is the fissioning nucleus, the projectile is the particle that induces fission, the process is F and there is no product. The branch tells what kind of neutrons the data describe:

| Branch | Meaning |
| --- | --- |
| `PR` | prompt neutrons |
| `DL` | delayed neutrons, total |
| `DL/GRP` | delayed neutrons by delayed-neutron group |
| `DL/CUM`, `DL/IND` | delayed neutrons by precursor, cumulative or independent |

The quantity `NU` is the number of neutrons per fission and `NU/DE` the neutron spectrum. Select the kind of neutrons with `--branch`:

```bash
python exfor_retrieve.py --target U-235 --projectiles n --quantity "NU,NU/DE" --product none

# delayed-neutron spectra
python exfor_plot.py --data data/U-235 --projectiles n --quantity NU/DE --branch DL --x Eout --logy

# total delayed yield against incident neutron energy (without the groups)
python exfor_plot.py --data data/U-235 --projectiles n --quantity NU --branch "DL,-GRP" --auto-axes
```

`--branch DL` keeps the parts of the branch that equal DL, so it selects `DL` and `DL/GRP`; `DL,-GRP` keeps the delayed totals only. Without `--branch` the prompt and delayed data would be drawn together.

What the snapshot has for 235U: 2,938 delayed-spectrum points (Egorov, Sharfuddin 1988, Batchelor 1956 and Tanczyn 1986), all at one incident energy (1.8 eV), with the spectra of the delayed-neutron groups as separate series; and delayed yields in the units PRT/FIS, PART/FIS and PC/FIS, plotted in separate files because the units differ.

### 15.3 Neutron yields

- **Neutrons per fission:** quantity `NU` (see 15.2); with `--branch PR` the prompt neutron multiplicity, with `--branch DL` the delayed one.
- **Neutrons produced by a reaction or in a target:** use the neutron as product (`--product n`) with the quantity `PY` (product yield), `TTY` (thick-target yield), or the double-differential forms such as `PY/DA/DE`. Neutron production cross sections are SIG with `--product n`.

```bash
python exfor_retrieve.py --target Be-9 --projectiles d,p,a --product n --quantity "PY,TTY"
python exfor_plot.py --data data/Be-9 --quantity PY --auto-axes
```

Yields come in many units (for example PRD/MUCOUL, products per microcoulomb, or PRD/INC, per incident particle). The programs do not convert them: the plotting program writes one plot per projectile and unit, so yields in different units are never mixed.

### 15.4 Practical notes

- For spectra use `--x Eout` (outgoing energy). If the data have several incident energies, choose one with `--at-energy`, for example `--at-energy 14 --tol 0.5`.
- Many spectra are given in arbitrary units, so only their shapes can be compared; the programs do not normalise them.
- The delayed-neutron group numbers are usually in the text of the entry, not in a column; look at the raw entry (Section 8.2, column `entry`) to identify them.
- Energies given as bins (E-MIN and E-MAX) are drawn at the middle of the bin.
- Check the unit and the branch of every plot before comparing datasets (Section 10).

## 16. Example: neutron spectra from charged-particle reactions

This chapter shows how to retrieve and plot the spectra of neutrons emitted in (α,n), (p,n), (d,n) and similar reactions. The numbers come from the EXFOR snapshot used for the tests (October 2026) and will change as EXFOR grows.

### 16.1 How these data are coded

| Item | EXFOR coding |
| --- | --- |
| Target | The target nucleus, for example 9Be. |
| Projectile | The charged particle: `a` (alpha), `p`, `d`, `he3`, `t`. |
| Product | The neutron: `--product n`. The reaction type is usually X (anything), so the plot title reads 9Be(p,x)n. |
| `DA/DE` | Double-differential cross section: neutron energy and angle (unit mb/sr/MeV). |
| `DE` | Neutron energy spectrum, integrated over angle. |
| `PY/DA/DE` | Double-differential yield, in units such as P/MEVMUCSR (per MeV, per microcoulomb, per steradian) or P/IN/MEVSR (per incident particle). |
| `TTY/PY/DA/DE` | Thick-target double-differential yield. |

The targets with most data in the snapshot (reaction strings and entries): for (p,n), lead (108 and 28), 27Al (105 and 29), natural carbon (78 and 18), 7Li (76 and 28), natural iron (71 and 18) and 9Be (55 and 28); for (α,n), 27Al (30 and 9), lead (30 and 7), natural carbon (20 and 5) and 9Be (16 and 3); for (d,n), 9Be (74 and 23), natural lithium and 7Li.

### 16.2 Retrieve

```bash
python exfor_retrieve.py --target Be-9 --projectiles a,p,d --product n --quantity "DA/DE,DE,PY/DA/DE,TTY/PY/DA/DE"
```

For 9Be this gives 135 datasets and 37,188 points (deuterons 24,251, protons 12,477, alphas 460).

### 16.3 Choose the incident energy and the angle

These datasets contain many incident energies and angles. If they are not separated, one plot would draw all of them together; the program warns when a plot mixes several energies or angles. Choose what to plot:

| You want | Option |
| --- | --- |
| One incident energy | `--at-energy E --tol T` (within T MeV of E) |
| One angle | `--at-angle A --angle-tol T` (within T degrees of A, default 5) |
| One plot for every incident energy | `--by-energy` |
| One plot for every angle | `--by-angle` |

See what exists first:

```bash
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity DA/DE --x Eout --list
```

The spectrum of neutrons from 256 MeV protons on 9Be at 30 degrees, on logarithmic axes:

```bash
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity DA/DE --x Eout \
    --at-energy 256 --tol 1 --at-angle 30 --logy --auto-axes
```

The file is `plots/Be-9/Be-9_p_n_DA_DE_mb_sr_MeV_E256MeV_A30deg.png` and the title reads 9Be(p,x)n \[DA/DE\] E = 256 MeV, θ = 30°. The energy and the angle are part of the file name, so different selections do not overwrite each other.

One plot for every angle at that energy (four plots, at 7.5, 30, 60 and 150 degrees):

```bash
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity DA/DE --x Eout \
    --at-energy 256 --tol 1 --by-angle --logy
```

With `--by-energy --by-angle` the program writes one plot for every combination of energy and angle; for 9Be alphas that is already dozens of plots. The program stops when more than `--max-plots` (default 200) plots would be written, and `--list` shows all of them without plotting.

### 16.4 Practical notes

- Use `--x Eout` for the spectra. For the angular distribution of the neutrons (quantity `DA`) at one energy use `--x angle`.
- Quantities with different units are never mixed: each unit gets its own plot, and the unit is in the file name. Cross sections (mb/sr/MeV) and yields (P/MEVMUCSR, P/IN/MEVSR) cannot be compared directly.
- Incident energies are usually in the data table. Many entries give a fixed beam energy once, in the COMMON block of the first subentry; the retrieval script applies it to all the data of the entry. If an entry does not give the energy in a column at all, `--at-energy` drops its points; select such an entry with `--entries` and read the energy from the raw entry.
- Energies and angles are compared with a tolerance (`--tol`, `--angle-tol`); datasets measured at slightly different energies need a tolerance large enough to be drawn together.
- Neutron production cross sections integrated over the spectrum are plotted with `--quantity SIG --product n` against the incident energy (no `--x Eout`).
- Check the unit, the incident energy and the angle of every plot before comparing datasets (Section 10).

### 16.5 Several angles in one plot, and 2D maps

Instead of one plot for every angle (`--by-angle`), there are two ways to see the whole energy-angle distribution at once.

**All angles in one plot, each labelled.** `--angle-labels` draws every angle as its own distribution and writes the angle in a bold label with a white box. The labels do not stand on the data: they are in a column to the right of all the points, and the x axis is extended to the right to make room for them. They follow the order of the last points of the distributions and are kept apart, so that they do not overlap, and a thin line of the colour of the dataset joins a label to the last point of its distribution when this ends before the rightmost one. If the points of a plot have no angle, the program prints a note and draws no labels; without --stack it warns that the labelled distributions may overlap. With `--stack 10` the distributions are multiplied by 10, 100, 1000 ... in order of increasing angle, so that they do not overlap; with the labels, each label says the factor, for example `30° (x10^3)`. The legend lists each dataset once. If there are too many distributions to label one above the other in the plot (more than about 25 to 30 in a plot of the usual size), an evenly spaced selection is labelled and the program says so (115 energies of one dataset gave 27 labels in the test); select fewer with `--at-energy`, `--at-angle` or `--entries`. With `--xlim` the x range is not extended, and the labels stand inside the range you gave.

```bash
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity PY/DA/DE --x Eout \
    --at-energy 9.18 --tol 0.05 --angle-labels --stack 10 --logy
```

This draws the ten angles measured at 9.18 MeV (0 to 140 degrees), from the bottom (0 degrees, factor 1) to the top (140 degrees, factor 10^9), in the file `plots/Be-9/Be-9_p_n_PY_DA_DE_P_MEVMUCSR_E9.18MeV.png`. Use `--stack` only on a logarithmic y axis, and remember that the curves are scaled: the factors are written on the labels. For angular distributions of several incident energies (`--x angle`) the same is done with `--energy-labels`, and each distribution is labelled with its energy.

**The labels are optional.** They are drawn only with `--angle-labels` (or `--energy-labels`). `--stack` alone draws the same scaled distributions with no labels, writes a small note in the plot ("distributions multiplied by 10^i, i = 0, 1, 2 ... in order of increasing angle"), and prints a note in the console; in earlier builds `--stack` also switched the labels on. Without `--stack` and without a label option the points of all the angles stay in one series, and the program advises `--by-angle` or `--at-angle`.

**2D maps.** `--map2d` draws outgoing energy (x) against angle (y) with the value as colour. The energies are put in `--ebins` bins (default 40, logarithmic when the energies span a factor of 50 or more), the angles in bins half-way between the measured angles, and each cell shows the mean of the points in it; empty cells are white. There is one map per dataset and incident energy, because the colours of different datasets cannot be mixed; the colour scale is logarithmic when the values span two decades or more (`--logz`, `--linz`, `--zlim`).

```bash
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity "TTY/PY/DA/DE" \
    --entries C0838 --map2d
```

This writes one map for each incident energy of the entry (3, 3.4, 3.7 and 4 MeV in the snapshot; a fifth energy has too few points), for example `plots/Be-9/Be-9_p_n_TTY_PY_DA_DE_P_MEVMUCSR_map_E3.7MeV_C0838003.png`. A dataset needs at least two angles and three outgoing energies to give a map; points without angle or outgoing energy are counted and left out.

Which to choose: the labelled curves show the shapes and the uncertainties of a few angles; the map shows the whole distribution when there are many angles and energies, but only for one dataset at a time and without error bars.

### 16.6 3D plots and other pairs of variables

Both `--map2d` and `--plot3d` work on any two of the three variables of a double-differential distribution: `E` (incident-particle energy), `Eout` (outgoing-particle energy) and `angle`. Choose them with `--axes`; the value is the colour of the map, or the height and colour of the 3D plot. There is one plot per dataset and per value of the third variable, which is shown in the title and in the file name.

| `--axes` | One plot per | Typical use |
| --- | --- | --- |
| `Eout,angle` (default) | incident energy | Energy-angle distribution of the emitted particles at one beam energy. |
| `E,Eout` | angle | Outgoing spectrum as a function of the beam energy, at a fixed angle. |
| `E,angle` | outgoing energy (or none) | Angular distributions as a function of the beam energy, for example elastic scattering. |

**Three styles.** `--plot3d --style surface` (the default) draws a surface over the cells; `--style bars` draws a 3D histogram; `--style scatter` draws the measured points. Empty cells stay empty in the surface and bars. The surface is best for a dense grid; bars and scatter are clearer when the data are sparse.

```bash
# energy-angle surface of the neutrons from 9.18 MeV protons on 9Be
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity PY/DA/DE \
    --at-energy 9.18 --tol 0.05 --plot3d

# the same as 3D bars, with 20 energy bins, and as a map
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity PY/DA/DE \
    --at-energy 9.18 --tol 0.05 --plot3d --style bars --ebins 20 --map2d

# incident energy against outgoing energy, at 0 degrees
python exfor_plot.py --data data/Be-9 --projectiles p --product n --quantity "TTY/PY/DA/DE" \
    --entries C0838 --at-angle 0 --angle-tol 1 --axes E,Eout --plot3d

# incident energy against angle for the elastic scattering of protons on 93Nb
python exfor_plot.py --data data/Nb-93 --projectiles p --product Nb-93 --quantity DA --unit NO-DIM \
    --emin 5.18 --emax 5.3 --axes E,angle --plot3d --style bars --logz
```

The first command writes `plots/Be-9/Be-9_p_n_PY_DA_DE_P_MEVMUCSR_3d-surface_Eout-angle_E9.18_A0834002.png`; the file names contain the kind of plot (`map`, `3d-surface`, `3d-bars`, `3d-scatter`), the two variables, the value of the third one and the entry.

**Scales and cells.** A variable with at most `--ebins` distinct values (default 40; angles and a few beam energies) gets one cell per value; a variable with more values is put in `--ebins` bins. Energy axes are logarithmic when the values span a factor of 50 or more (`--logx` and `--logy` force the first and the second variable of `--axes`, `--linx` and `--liny` force a linear scale). The height and colour are logarithmic when the values span two decades or more (`--logz`, `--linz`, `--zlim`). On a logarithmic axis the 3D plot shows powers of ten as tick labels. Each cell holds the mean of the points that fall in it. Change the view with `--elev` and `--azim`.

**Limits.** A dataset needs at least two distinct values of each of the two variables to give a plot; a plot that cannot be made is reported and skipped. A dataset where the third variable has many values gives many plots (`--max-plots` stops the program at 200); select one value with `--at-energy` or `--at-angle`. Datasets measured at only a few energies give sparse surfaces with gaps; use `--style bars` for them. The 3D plots carry no error bars.

### 16.7 A spectrum coded as a cross section: 27Al(d,n)28Si

The retrieval of deuterons on 27Al giving 28Si (`--target Al-27 --projectiles d --product Si-28`) has six datasets and 748 points, with beam energies from 1.4 to 11.2 MeV. The only one with the quantity `SIG` has two incident energies only, 5.0 and 7.0 MeV. This is correct: it is how EXFOR has it. The entry is C1151 (S. I. Al-Quraishi et al., Phys. Rev. C 62, 044616 (2000), *Low energy deuteron-induced reactions on 27Al and 56Fe*), subentry 004, and its data table starts like this:

```text
REACTION   (13-AL-27(D,N)14-SI-28,PAR,SIG)
STATUS     (CURVE) Data taken from Figs. 7 and 10
DATA                 3         93
EN         E          DATA
MEV        MEV        MB
5.0          2.765E-01  2.822E+01
5.0          4.877E-01  4.083E+01
5.0          7.522E-01  3.746E+01
```

The column `EN` is the beam energy (5.0 and 7.0 MeV, with 53 and 40 points) and the column `E` is the energy of the emitted neutron (0.28 to 13.4 MeV at 5 MeV and 0.36 to 10.15 MeV at 7 MeV). The 93 points are therefore the neutron spectra at two beam energies, read from two figures (the status is `CURVE`), and not an excitation function. The same entry codes the (d,p) and (d,α) data of 27Al and of 56Fe in the same way (subentries 004 to 009).

With the incident energy as the x axis the data are two vertical lines. To see them as spectra, plot them against the outgoing energy, one plot for each beam energy (the program prints this advice when it finds such data plotted against the incident energy; the y label is dσ/dE (mb/MeV) in both cases, because it follows the data and not the x axis):

```bash
python exfor_plot.py --data data/Al-27 --projectiles d --product Si-28 --quantity SIG --x Eout --by-energy
```

The x axis is Neutron energy (MeV) and the y axis dσ/dE (mb/MeV); at 5 MeV the values fall from 41 mb/MeV near 0.5 MeV to 1 mb/MeV near 7.6 MeV and stay below 2 mb/MeV above 8 MeV. Earlier versions wrote Outgoing energy (MeV) and Cross section (mb). The labels are explained in Section 14.13. EXFOR gives the unit of these data as `MB`, not `MB/MEV`: the program labels them per MeV because they are a neutron spectrum, which is an interpretation. I have not checked it in the paper, so look at Figs. 7 and 10 of the publication before you quote the unit, and use `--ylabel` if it differs.

For a spectrum, EXFOR would normally use the quantity `DE` (dσ/dE, mb/MeV) or `DA/DE`; such data are plotted as in Sections 16.3 to 16.6.

With `--ascii` the same dataset is written as a file of three columns, `Al-27_d_28Si_SIG_PAR_Al-Quraishi2000_C1151-004.dat`, whose first row is `E[MeV]  E_neutron[MeV]  dsigma/dE[mb/MeV]` (Section 8.6.5): the beam energy, the neutron energy and the spectrum, with a blank line between the two beam energies.

That file has no uncertainty column, and the plot has no error bars: the table of this dataset in EXFOR has only the columns `EN`, `E` and `DATA`, and the entry gives no uncertainty in its text either (the column `uncertainty` of `index.csv` says `none`, Section 8.6.5).

### 16.8 Neutron spectra at several angles from alpha particles on 27Al: a script

The script `plot_Al27_alpha_neutron_spectra.sh` (in the folder `examples` of the repository, or next to the programs) retrieves the data and draws the neutron spectra of alpha particles on 27Al at all the angles, one plot for each incident energy and kind of data. Run it from any folder (the folder of the programs is the variable PROGRAMS at the top of the script, and the data and the plots go to the folders DATA and OUT):

```bash
bash plot_Al27_alpha_neutron_spectra.sh              # or: PYTHON=python3 bash plot_Al27_alpha_neutron_spectra.sh
```

It writes 28 plots in `plots_Al27_alpha_n/` (7 at low energies and 21 at high energies), in PNG and PDF, and the list of references of the data in `data/Al-27/EXFOR_AL-27_references.txt` and `.bib`. **What EXFOR has** (snapshot of 2026-09-28): two groups of data, coded in different ways.

- *Low energies, the reaction 27Al(α,n)30P.* The thick-target neutron spectra of G. J. H. Jacobs and H. Liskien, Ann. Nucl. Energy 10 (1983) 541 (entry D0757), at alpha energies of 4 to 5.5 MeV and five angles, their integral over the angles, the mean neutron energy, and the neutron yield per incident alpha particle from 3.08 MeV (Brandenburg 2023, entry C3065, and Jacobs 1983). EXFOR codes them as reactions to 30P with the quantity `MLT` (neutron multiplicity), not with the neutron as product, so a search with `--product n` does not find them.
- *High energies, the neutron emission (α,xn).* Spectra with the neutron as product, from 30 MeV up; there are none below 30 MeV. The nearest data to the low-energy ones are angular distributions of the neutron yield (quantity `PY/DA`, arbitrary units, 11 points) from 4.8 to 8.8 MeV.

| Quantity (unit) | Alpha energy (MeV) | Angles (degrees) | Entry |
| --- | --- | --- | --- |
| `MLT/DA/DE` (P/IN/MEVSR), thick target, product 30P | 4, 4.5, 5, 5.5 | 0, 30, 60, 100, 140 | D0757, Jacobs 1983 |
| `MLT/DE` (PRT/IN/MEV), integrated over the angles, product 30P | 4, 4.5, 5, 5.5 | integrated | D0757, Jacobs 1983 |
| `MLT` (PRT/INC, neutron yield) and `KE` (MeV, mean neutron energy), product 30P | 3.08 to 5.5 and 4 to 5.5 | integrated | C3065, Brandenburg 2023; D0757, Jacobs 1983 |
| `PY/DA/DE` (P/IN/MEVSR), thick target | 30, 40, 50 | 0, 30, 45 | A0490, Dhar 2003 |
| `DA/DE` (mb/sr/MeV) | 140 | 20, 30, 45, 60, 120 | C0841, Kalend 1983 |
| `PY/DA/DE`, thick target | 400, 720 | 0, 7.5, 15, 30, 60, 90 | E2079, Satoh 2007 (E1810, Kurosawa 1999, is superseded) |
| `DA/DE` | 540 | 0, 15, 30, 50, 80, 110 | E1750, Sato 2001 |
| `PY/DA/DE`, thick target | 620 | 10, 30, 45, 60, 90, 125, 160 | C1051, Heilbronn 1999 |
| `DA/DE` | 920 | 5, 10, 20, 30, 40, 60, 80 | E2050, Heilbronn 2007 |
| `PY/DA/DE`, thick target | 1600, 3200, 6000 | 10, 30, 45, 60, 80, 135 | C3057, Ratliff 2023 |

The `PY/DA/DE` and `MLT/DA/DE` data are neutron yields from thick targets per incident alpha particle, per MeV and per steradian; `MLT/DE` is the same integrated over the angles; the `DA/DE` data are double-differential cross sections. They have different units and are never drawn in the same plot. **A lesson of this case**: before you conclude that EXFOR has no data, look at the catalogue of the target and the projectile with all the products (`python exfor_retrieve.py --target Al-27 --projectiles a --available`), because the same measurement can be coded with the residual nucleus (here 30P) and a quantity whose name does not say neutron, and a search with the neutron as product misses it.

**What the script does.** All the angles of a plot are drawn together, each labelled at the right of the data, with `--stack 10` so that the curves do not overlap on the logarithmic axes (Section 16.5). The data of Jacobs and Liskien are selected with `--product P-30 --quantity MLT/DA/DE --at-energy E --tol 0.1` (one plot for each of the four energies; then their integral over the angles with the four energies in one plot, the neutron yield, and the mean neutron energy), and the others with `--product n --quantity DA/DE,PY/DA/DE --x Eout --at-energy E --tol 1 --logx`. `--exclude-status SPSDD` leaves out the superseded data of Kurosawa 1999 at 400 and 720 MeV. The first command of the script also writes the list of references of all the data (`--references`). The entry C3057 is treated apart:

- It has dual-thick-target measurements: an upstream aluminium target of 20, 40 or 60 g/cm² and a downstream one of 60 g/cm². Each configuration is a dataset of its own, and the thick-target yield depends on the thickness, so the script draws each subentry in a plot of its own, selected with `--entries C3057016` (a subentry number, as in the legend) and titled with the thickness. That is 12 plots: three at 1600 MeV, six at 3200 MeV (two datasets for each thickness, subentries 016 to 018 and 055 to 057; the entry does not say what distinguishes them) and three at 6000 MeV. Drawn together, the datasets of 3200 MeV hide each other.
- Six other subentries of the entry (104 to 109) are aluminium plus polyethylene targets, coded as a sum of two reactions. They are complex reactions and are left out. Before the fix of 2026-10-07 the programs read them as simple reactions on 27Al and drew them with the aluminium data (Section 10).

**The cross sections of the reaction.** The same data folder serves the (α,n) cross section to 30P and the neutron production cross section (the commands are at the end of the script):

```bash
python exfor_plot.py --target Al-27 --projectiles a --product P-30 --process N --include-complex \
    --exclude-status SPSDD --logy --xlim 2,32 --ylim 0.1,1000
python exfor_plot.py --target Al-27 --projectiles a --product n --quantity SIG --include-complex --logy
```

The first draws 922 points from 6 entries between 2.5 and 31 MeV. EXFOR has no separate total (α,n) cross section: all the (α,n) data are coded as the reaction to 30P. The second is the neutron production cross section, σ(α,xn), 138 points from 3 entries: it includes every channel that emits a neutron and is not the (α,n) cross section.

**The script in full.** It is the file `plot_Al27_alpha_neutron_spectra.sh`:

```bash
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
PROGRAMS=${PROGRAMS:-"$(cd "$(dirname "$0")" && pwd)"}   # folder of exfor_retrieve.py and exfor_plot.py (default: the folder of this script)
DATA=${DATA:-"$PROGRAMS/data"}                   # the retrieved data are in "$DATA/Al-27"
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
```

The angles of the `DA/DE` and `PY/DA/DE` data are in the first paragraphs of this section; to see the same data as maps instead, use the optional line 4 of the script (Section 16.6 describes the maps).

For another isotope or projectile, and to get the exclusive, the inclusive and the combined plots without choosing the energies and the quantities by hand, use the general script of Section 16.9.

### 16.9 All the neutron spectra and yields of an (x,n) reaction: exclusive, inclusive and combined

The script `plot_neutron_emission.py` (in the folder `examples` of the repository, or next to the programs) does for any isotope what Section 16.8 does by hand for 27Al and alpha particles. It makes three kinds of plots:

- **exclusive**: the reaction to the residual nucleus, (x,n), for example 27Al(α,n)30P. EXFOR codes it with the residual as product, and with quantities such as `MLT`, `MLT/DE`, `MLT/DA/DE` and `KE`.
- **inclusive**: the neutron emission, (x,xn), with the neutron as product, and the quantities `DA/DE`, `PY/DA/DE`, `PY`, `TTY` and so on.
- **combined**: the two in one plot, only where both exist and have the same unit; the legend gives the product of each series.

The exclusive reaction is a part of the inclusive one, so the combined plot is for comparing them; they are different quantities and are also plotted apart.

```bash
python plot_neutron_emission.py Al-27                      # alpha particles, the default
python plot_neutron_emission.py Be-9 --out plots_Be9       # another isotope
python plot_neutron_emission.py Al-27 --projectile he3     # (3He,n); also p, d and t
python plot_neutron_emission.py Al-27 --dry-run            # list the plots without making them
```

Other options: `--formats png,pdf`, `--data-dir`, `--master`, `--keep-superseded` (do not leave out the superseded data), `--with-cross-sections` (also `SIG`), `--ascii` (one ASCII file for each dataset), `--no-retrieve` (use the data already retrieved). The projectile gives the residual nucleus: the target with Z increased by the charge of the projectile and A by its mass minus one (30P for 27Al and alpha).

**Paths.** The script can be run from any folder. The folders of the programs, of the retrieved data, of the plots and of the EXFOR master files are four constants at the top of the script, `PROGRAMS_DIR`, `DATA_DIR`, `OUT_DIR` and `MASTER_DIR`; each can be replaced on the command line (`--programs-dir`, `--data-dir`, `--out`, `--master`), and `--programs-dir` also by the variable `EXFOR_PROGRAMS_DIR`. If `PROGRAMS_DIR` does not exist, the folder of the script is used, so that the script also works when it is kept next to the programs; if the programs are in none of them, it stops with a message that lists the folders it tried. The bash script of Section 16.8 has the same settings as the variables `PROGRAMS`, `DATA` and `OUT` at its top, which can also be set when it is run (`PROGRAMS=/path/to/programs DATA=/path/to/data OUT=plots bash plot_Al27_alpha_neutron_spectra.sh`); paths with spaces are handled.

**What the script does.** It retrieves both kinds of data once, with the list of references (`data/<isotope>/EXFOR_*_references.txt` and `.bib`), sorts the datasets into families and draws each family in the way that suits it:

| Family | EXFOR quantities | Plot |
| --- | --- | --- |
| `spectra_angles` | `DA/DE`, `PY/DA/DE`, `MLT/DA/DE`, `TTY/PY/DA/DE` | one plot for each incident energy, all the angles in it, labelled and stacked (Section 16.5) |
| `spectra_integrated` | `DE`, `PY/DE`, `MLT/DE` | spectrum integrated over the angles, all the energies in one plot with energy labels |
| `angular` | `DA`, `PY/DA`, `MLT/DA` | against the angle, energy labels |
| `yield` | `PY`, `TTY`, `MLT` | against the incident energy |
| `mean_energy` | `KE` | mean neutron energy against the incident energy |

The plots are in `plots_neutron_emission/<family>/<exclusive, inclusive or combined>/`.

**Rules.**

- **Units are never mixed.** One plot for each unit; the quantities of one unit go into one plot (`MLT` and `PY` for the neutron yield per incident particle), and the units that differ only in PRD or PRT written for P are the same unit.
- **Superseded data** (`SPSDD`) and **complex reactions** (sums and ratios, including sums with a compound target) are left out.
- **Spectra at several angles** are combined only at an incident energy that both kinds have. A subentry that repeats the angles of another subentry of the same entry at the same energy is a different configuration (for example a target thickness) and gets a plot of its own (`--entries` with a subentry number, Section 16.8).
- **Many energies**: with more than 20 energies the curves are not stacked, and the labels are thinned (Section 16.5).

**Coverage.** The script writes `coverage.csv` (every dataset that was retrieved, the plots it is in, or why it is in none: superseded, complex reaction, no incident energy, quantity or product that is not handled), prints a summary and keeps the log of the plot commands in `plots_neutron_emission_log.txt`. A dataset that is in no plot is never silent.

**Results.**

- *27Al and alpha particles.* 35 plot commands, 38 plots (each also in PDF): 25 spectra at several angles (4 exclusive from 4 to 5.5 MeV, Jacobs and Liskien 1983, and 21 inclusive: 9 energies from 30 to 920 MeV and 12 target configurations of Ratliff 2023), the integrated spectra (exclusive, inclusive and combined), 5 angular distributions (in different units), 4 yield plots (exclusive, inclusive in two units, combined), and the mean neutron energy. 38 of the 46 retrieved datasets are in a plot; 6 are complex (aluminium plus polyethylene, Ratliff 2023) and 2 are superseded (Kurosawa 1999).
- *9Be and alpha particles* (the reaction 9Be(α,n)12C, the classic neutron source). 14 plots; all 74 datasets are in a plot.

The exclusive and the inclusive yields of 27Al are drawn together only where they have the same unit (neutrons per incident alpha particle); the neutron yield per microcoulomb of the inclusive data has no exclusive counterpart and stays in its own plot.

### 16.10 Data measured at n\_TOF (CERN): yields, resonance parameters and strength functions

The option `--facility` (new in `exfor_retrieve.py` 2.3 and `exfor_plot.py` 1.3) keeps only the EXFOR entries measured at a given facility. With `--facility ntof` the entries of the n\_TOF facility at CERN are selected. They hold much more than cross sections, so the quantities are chosen with `--quantity`.

**How n\_TOF entries are identified.** Two criteria are used together (in a test with the master files of 9 October 2026 they give 84 entries):

1. The FACILITY field carries the CERN institute code `2ZZZCER` and the text nTOF, n-TOF or n\_TOF (for example `(SYNCY,2ZZZCER) CERN nTOF facility (EAR1)`). This finds about 71 entries.
2. Entries whose FACILITY text is missing or does not name the facility, but whose TITLE, INSTITUTE or REFERENCE names n\_TOF together with CERN (for example 22796 and 23027 on Os, 23126 on Np, 22931 on 232Th, 23670 on natC(n,p) and (n,d)). This adds about 13 entries; with the first criterion alone they would be lost.

Other "neutron TOF" facilities (GELINA, IUCF, NBS linac, and so on) do not match. `--facility gelina` selects GELINA, and any other text is a regular expression searched in the FACILITY and INSTITUTE fields, for example `--facility "LANSCE|WNR"`. The entries with a FACILITY text are identified by the facility only; the identification does not judge whether the data belong to the collaboration.

**Quantities found at n\_TOF.** Count of entries (one entry may carry several quantities):

| Code | Quantity | Entries |
| --- | --- | --- |
| `SIG` | Cross section | about 54 |
| `WID` | Resonance width (neutron, capture, fission) | about 37 |
| `WID/STR` | Resonance strength | about 30 |
| `RYL` | Reaction yield (capture yield against neutron energy) | 26 |
| `RI` | Resonance integral | 7 |
| `DA` | Angular distribution | 2 |
| `STF` | Strength function | 1 (243Am, entry 23254) |
| `PY`, `DE` | Gamma-ray yield and energy (234U(n,γ), entry 23758) | 1 |
| `INT`, `EN`, `POL/DA`, `WID/RED` | Integral, resonance energy, polarisation, reduced width | 1 each |

Level densities are not in EXFOR as a data quantity for n\_TOF. The level spacing D0 appears only in the text of some entries (ASSUMED or ANALYSIS fields, for example 23254, 23237 and 22893), so there is nothing to retrieve. A strength function is coded only for 243Am.

**First look: which targets, and how much.**

```bash
python exfor_retrieve.py --facility ntof --find --quantity RYL,WID,WID/STR,RI,STF,PY,DE,INT,DA --summary-only --max-rows 100
```

This lists the targets with such data (54 in the test) with the number of entries, datasets and points. Without `--quantity` the 65 targets with any quantity are listed. The default projectile of `--facility ntof` is the neutron.

**Retrieve one target or all.**

```bash
# one target: reaction yield and resonance parameters of 197Au, with ASCII files and the references
python exfor_retrieve.py --facility ntof --target Au-197 --quantity RYL,WID,WID/STR --ascii --references

# all targets (without --target, or with --target all): one folder data/<target> for each; about 7 minutes
python exfor_retrieve.py --facility ntof --quantity RYL,WID,WID/STR,RI,STF,PY,DE,INT,DA --out data_ntof --ascii
```

The retrieval of all targets runs the search once for each target found, so it takes several minutes; the entries of the facility are read only once. The folders are the usual ones (Section 4), and the dataset table has the columns `facility` and `institute`.

**Resonance parameters.** In the entries with widths the resonance energy is not an incident-energy column: the REACTION field has two items, `(95-AM-243(N,0),,EN)` for the energy and `(95-AM-243(N,EL),,WID)` for the width, and the energy is the DATA column of the first. The program takes the energy from that column, so the width, the strength and so on are written against the resonance energy (column `E[MeV]` in the ASCII files, for example 4.4016e-05 MeV for the resonance at 44.016 eV). Use `--logx` for plots over many decades. A quantity that is a single number for the whole dataset, such as a strength function, is written as a header line and the value.

**Plots.**

```bash
# capture yield of 197Au against neutron energy
python exfor_plot.py --data data_ntof/Au-197 --projectiles n --quantity RYL --logx --auto-axes

# resonance widths of 243Am
python exfor_plot.py --data data_ntof/Am-243 --projectiles n --quantity WID --logx

# retrieve and plot in one step, only the n_TOF data
python exfor_plot.py --target Au-197 --facility ntof --projectiles n --quantity RYL --logx --auto-axes
```

The axis labels follow the quantity: Reaction yield, Resonance width (meV), Resonance strength, Strength function, Resonance integral. The yield of 197Au has more than ten thousand points (two datasets of Massimi 2010, entry 23067), so the plot is a dense band; restrict the range with `--emin` and `--emax` (MeV) to look at one resonance. For several targets, retrieve with `exfor_retrieve.py --facility ntof` and plot each folder with `--data`; `exfor_plot.py --facility` works with `--target` only.

**A script for all of it.** `plot_ntof_data.sh` (in `examples` of the repository) lists the targets, retrieves them (ASCII files, references) and plots the yields, the widths and strengths, and the resonance integrals and strength functions of every target. The paths are variables at the top (`PROGRAMS`, `DATA`, `OUT`), as in Section 16.8:

```bash
bash plot_ntof_data.sh              # all targets
bash plot_ntof_data.sh Au-197 Am-243  # only these two
```

**Cautions.** The counts above are from a scan of the BIB blocks and depend on the EXFOR version (`--master-info`). New n\_TOF entries may be coded without any facility text; look at the `facility` column of the dataset table, and use `--entries` to add or remove entries by hand. Quantities that are not cross sections may need a unit check; resonance energies are in MeV in the tables, as for any energy.

### 16.11 The n\_TOF data of a table of reactions

`plot_ntof_reactions.py` (in `examples` of the repository) plots the n\_TOF data for a list of reactions: 7Li(n,n't)α, 9Be(n,2n)2α, 6Li(n,t)α, 11B(n,el), (n,γ) on Cr, Fe, Ni, W, Zr, Mo and Pb isotopes, 56Fe(n,n'γ) and (n,xn), natC(n,p) and (n,d), 50Cr(n,p)50V, 14N(n,p)14C, 33S(n,α)30Si, 35Cl(n,p)35S, 209Bi(n,γ)210mBi and 7Be(n,p) and (n,α). The table is the list `REACTIONS` at the top of the script (name, targets, EXFOR reaction type); edit it to add reactions. The paths `PROGRAMS_DIR`, `DATA_DIR`, `OUT_DIR` and `MASTER_DIR` are set there too and can be replaced with `--programs-dir`, `--data-dir`, `--out` and `--master`.

```bash
python plot_ntof_reactions.py --list                    # the table, with numbers
python plot_ntof_reactions.py                          # all reactions, cross sections (about 5 minutes)
python plot_ntof_reactions.py --only 5,6,10            # Cr, Fe and Zr (n,g)
python plot_ntof_reactions.py --also RYL,WID           # besides SIG: reaction yields and resonance widths
python plot_ntof_reactions.py --coverage-only          # only the table of what EXFOR has
python plot_ntof_reactions.py --no-retrieve            # plot again from the data already retrieved
```

The script retrieves each target with `--facility ntof --projectiles n` (Section 16.10), counts the datasets of each reaction, writes `coverage_ntof.csv`, and draws what exists in `<out>/<number>_<reaction>/<target>/` with the references (`.txt` and `.bib`). The energy axis is logarithmic, and so is the cross-section axis (`--linear` changes both).

**What the EXFOR master files of 9 October 2026 have for the table.** Cross sections (SIG) or yields (RYL) measured at n\_TOF exist for 6Li(n,t), (n,γ) on 50Cr, 53Cr, 54Fe, 57Fe, 58Ni, 62Ni, 63Ni, 90Zr, 91Zr, 92Zr, 94Zr, 96Zr, 204Pb, 206Pb, 207Pb and 209Bi, natC(n,p) and (n,d), 14N(n,p), 33S(n,α), 35Cl(n,p) and 7Be(n,p). There are no n\_TOF entries for 7Li(n,n't), 9Be(n,2n), 11B(n,el), 52Cr, 54Cr, 56Fe, 64Ni, W, Mo, natPb, 208Pb, 50Cr(n,p), 56Fe(n,n'γ) and (n,xn) and 7Be(n,α) (only widths of 7Be are coded); the table says "no n\_TOF data in EXFOR" for them. This can change with new entries, and an entry coded without any n\_TOF text would also be missed (Section 16.10).

**What the plots show.**

- Many (n,γ) entries have the cross section only as a Maxwellian average (a column `KT`, for example 30 keV), with no incident energy; these points are in the CSV and ASCII files but are not drawn, and the program prints "No point has the coordinate E". The continuous data are the reaction yields (`RYL`, with `--also RYL`), which have 10,000 to 120,000 points. The thermal point (0.0253 eV) is drawn when the entry has it.
- The 6Li(n,t) data of Amaducci 2019 are not absolute 6Li(n,t) cross sections: they are ratios without unit that contain 6Li(n,t) (complex reactions in EXFOR, entry 23453). Subentry 002 is the ratio 235U(n,f)/6Li(n,t) (140 points, the lower band of the plot) and subentries 008 to 012 are the ratio 10B(n,a)/6Li(n,t) in five energy ranges (36, 71, 139, 278 and 1387 points, the upper band at about 4); the 235U(n,f) cross sections of the same entry (subentries 013 to 017) belong to the target 235U. In the plot of complex reactions (with --include-complex) exfor\_plot.py now gives the datasets of one entry that are different reactions their own colour and marker, and the legend names the reaction (for example 235U(n,f) / 6Li(n,t)4He and 10B(n,a)7Li / 6Li(n,t)4He); datasets of the same reaction share one legend entry; the script draws them in a separate plot (`Li-6_ratio_...`) with the label "Ratio to a reference reaction", with `--include-complex`.
- 209Bi(n,γ): EXFOR codes the product as 210Bi without isomer state, so 210mBi and the 210Po that comes from it are not separated.
- A mixed entry such as 23759 (GELINA and n\_TOF, 92Zr) is included whole.

## 17. More examples for different cases

Each example below was run on the EXFOR snapshot used for the tests (October 2026). The counts quoted will change as EXFOR grows. Commands are written for the default folders: the data go to `data/<target name>/` and the plots to `plots/<target name>/`.

### 17.1 Activation and production cross sections

**Long-lived activation products of a material.** Deuterons on 93Nb, the products 92mNb, 91mNb, 88Zr and 89Zr, with superseded datasets removed and the 40 MeV deuteron energy of IFMIF-DONES marked:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles d --quantity SIG --product "Nb-92m,Nb-91m,Zr-88,Zr-89"
python exfor_plot.py --data data/Nb-93 --exclude-status SPSDD --vline 40 --auto-axes
```

This retrieved 15 datasets and 163 points and wrote five plots: `Nb-93_d_92mNb.png`, `Nb-93_d_91mNb.png`, `Nb-93_d_88Zr.png`, `Nb-93_d_89Zr.png` and `Nb-93_d_89gZr.png`. The last one exists because `Zr-89` matches every state of 89Zr, and some authors give the ground state separately.

**Isomers and ground states.** Natural titanium with deuterons, the isomer 44mSc, the ground state 44gSc and the monitor product 48V. Write `m` or `g` after the mass to select one state; without it all states are selected (Section 7.6):

```bash
python exfor_plot.py --target Ti-nat --projectiles d --product "Sc-44m,Sc-44g,V-48" --exclude-status SPSDD
```

In the snapshot this gives 219 points for 44mSc (9 datasets), 109 for 44gSc (5 datasets) and 371 for 48V (11 datasets; the filter leaves out one superseded dataset of S.Takacs 1997, entry D4046, 65 points, replaced by data of the same entry; without the filter it is 436 points in 12 datasets).

**The same product from different projectiles.** Which projectiles make 65Zn on natural copper? First look at all of them without writing files, then plot the ones you want:

```bash
python exfor_retrieve.py --target Cu-nat --projectiles all --product Zn-65 --quantity SIG --summary-only
python exfor_plot.py --target Cu-nat --projectiles p,d,a --product Zn-65 --exclude-status SPSDD
```

The summary lists protons (34 datasets), alphas (15), deuterons (10), 3He (6) and 7Li (3). The plots are written one per projectile (`Cu-nat_p_65Zn.png`, `Cu-nat_d_65Zn.png`, `Cu-nat_alpha_65Zn.png`); the program does not overlay different projectiles in one plot.

**Heavy-ion induced reactions.** 12C on 93Nb has 76 datasets, 734 points and 36 products. Look at the products, then plot one:

```bash
python exfor_retrieve.py --target Nb-93 --projectiles 12C --quantity SIG --summary-only
python exfor_plot.py --target Nb-93 --projectiles 12C --product Pd-101 --exclude-status SPSDD
```

The energy on the x axis is the total laboratory energy of the 12C beam in MeV (Section 8.4), and the file is `plots/Nb-93/Nb-93_12C_101Pd.png`. Add `--projectiles "12C,16O"` to include oxygen-16 as well.

**Photonuclear reactions.** The cross section of 208Pb(γ,n), product 207Pb, with 972 points from 10 entries up to 21 MeV (the giant dipole resonance):

```bash
python exfor_plot.py --target Pb-208 --projectiles g --product Pb-207 --exclude-status SPSDD
```

Not every photon dataset has a tabulated energy. For 93Nb with the product 92Nb, most of the simple reactions are bremsstrahlung yields without an incident energy, so the plot program reports that no point has the coordinate E.

**Neutron-induced reactions.** (n,2n) on 93Nb, with `--process 2N` to keep only that reaction type:

```bash
python exfor_plot.py --target Nb-93 --projectiles n --product Nb-92 --process 2N
```

This writes three plots, for 92mNb (66 series, 350 points), 92Nb (13 series, 46 points) and 92gNb (1 point), because the authors code the final state in different ways.

**Alpha particles on 27Al: the (α,n) cross section.** The reaction 27Al(α,n)30P makes 30P (half-life 2.5 minutes). EXFOR has no separate total (α,n) cross section: every (α,n) cross section of 27Al is coded as the reaction to 30P, which is the total over the final states. The cross section from the threshold at 2.5 MeV up to 31 MeV, on logarithmic axes (the values span 0.2 to 500 mb), with the energy and the cross-section ranges chosen so that no data are cut:

```bash
python exfor_plot.py --target Al-27 --projectiles a --product P-30 --exclude-status SPSDD \
    --logy --xlim 2,32 --ylim 0.1,1000
```

This draws 815 points from 5 entries (six datasets: Williamson 1960, Flynn 1978 twice, Sahakundu 1979, Frantsvog 1982 and Roy 2025) in `plots/Al-27/Al-27_alpha_30P.png`. The program says what it leaves out: 107 points of a complex reaction, 27 points in a unit that is not mb (Spassky 1968, relative units) and 15 points without an energy (Howard 1974). To draw every dataset of the (α,n) process that can be drawn in mb, give `--process N --include-complex`; this adds the data of Holmqvist 1986 (3 to 3.7 MeV), which EXFOR codes as "neutron production = (α,n) to 30P", and gives 922 points from 6 entries.

The neutron production cross section, σ(α,xn), is another quantity: it includes every channel that emits a neutron. EXFOR has 138 points from 3 entries, with the neutron as product:

```bash
python exfor_plot.py --target Al-27 --projectiles a --product n --quantity SIG --include-complex --logy
```

The data of Stelson 1964 (5 to 11 MeV) reach about 350 mb near 10 MeV, several times more than the (α,n) value of Sahakundu 1979 at 10.5 MeV (about 50 mb); I did not investigate why, so read the entries before relying on either. Everything for alpha particles on 27Al, one plot for each product (64 plots, 2,582 points from 54 entries; add `--quantity ALL` for the other quantities):

```bash
python exfor_plot.py --target Al-27 --projectiles a --exclude-status SPSDD --auto-axes
```

The neutron spectra at several angles of the same reaction, and the neutron yield per incident alpha particle from 3 to 5.5 MeV (quantity `MLT`, Brandenburg 2023 and Jacobs 1983), are in Section 16.8.

### 17.2 Neutron multiplicity

The prompt neutron multiplicity of 235U(n,f), against the incident neutron energy on a logarithmic x axis:

```bash
python exfor_plot.py --target U-235 --projectiles n --product none --quantity NU --branch PR \
    --unit NO-DIM --logx --auto-axes
```

This draws 96 points from 9 entries in `plots/U-235/U-235_n_none_NU_F.png`. `--branch PR` keeps the prompt neutrons (`DL` would give the delayed ones, Section 15), and `--unit NO-DIM` keeps the dimensionless values. Without `--unit`, the program writes one plot for every unit that the datasets use. Capture, total and fission cross sections of 238U are in Section 14.8, neutron spectra in Sections 15 and 16.

### 17.3 Working with the data

**A coverage table with pandas.** How many datasets exist for each product, over which energies and from which years (deuterons on 93Nb):

```python
import pandas as pd
ds = pd.read_csv("data/Nb-93/EXFOR_NB-93_datasets.csv")
ds = ds[(ds.projectile == "d") & (ds.quantity == "SIG") & (ds.reaction_type == "simple")]
cov = (ds.groupby("product_label")
         .agg(datasets=("entry", "size"), entries=("entry", "nunique"), E_min=("E_min_MeV", "min"),
              E_max=("E_max_MeV", "max"), first_year=("year", "min"), last_year=("year", "max"))
         .sort_values("entries", ascending=False))
print(cov.head(6))
```

In the snapshot the first rows are 93mMo (5 entries, 2000 to 2018), 92mNb (4 entries, 2007 to 2018), 90mY (3 entries) and 90Nb (3 entries). Note that the `E_max` of some products reaches 7,300 MeV: those are GeV-range datasets, which you can remove with `--emax 60` when retrieving or plotting.

**Several targets in one command.** Retrieve each target, then plot them together; every target keeps its own folder:

```bash
for t in Nb-93 Cu-nat; do
    python exfor_retrieve.py --target $t --projectiles d --quantity SIG
done
python exfor_plot.py --data data/Nb-93 data/Cu-nat --projectiles d --product "92mNb,Zn-65" --exclude-status SPSDD
```

The plots go to `plots/Nb-93/` and `plots/Cu-nat/`. Each product is plotted for every target that has it; for example, `Nb-93_d_65Zn.png` appears because one GeV-range point of 65Zn exists in the niobium data.

**Remove outliers and old datasets.** Look at the plots, identify the entry numbers (they are in the legend, in brackets, and in the datasets file) and exclude them. In the natural copper data, entry P0069 (Bartell 1950) is far above the other data in some channels, and entry C1131 (Diksic 1979) has a 64Cu value about ten times too high:

```bash
python exfor_plot.py --data data/Cu-nat --product Zn-65 --exclude-entries P0069,C1131 --exclude-status SPSDD
```

The opposite, plotting only some datasets, is `--entries D4344,D4156`. `--list` shows how many series each plot would have before you decide.

**Everything about one isotope in one go.** A full dump of all projectiles, all quantities, with the JSON files too:

```bash
python exfor_retrieve.py --target Mn-55 --projectiles all --json
```

For 55Mn this is 913 datasets and 59,716 points: `EXFOR_MN-55_data.csv` is 15 MB, `EXFOR_MN-55_data.jsonl` 48 MB. Use `--summary-only` first for heavily studied targets (Section 7.5).

**Redo plots later, without the EXFOR master files.** Plotting from the saved data needs only the CSV files; you can change the selection, the axes and the format as often as you like:

```bash
python exfor_plot.py --data data/Nb-93 --product 92mNb --logy --xlim 0,50 --format png,pdf
```

**Figures for a paper.** A clean single plot in vector formats at 300 dpi, without energy error bars, with smaller markers and your own title:

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product 92mNb --exclude-status SPSDD \
    --vline 40 --xlim 0,50 --no-xerr --ms 3 --title "93Nb(d,x)92mNb" --format pdf,svg --dpi 300
```

This writes `plots/Nb-93/Nb-93_d_92mNb.pdf` and `.svg`. If a plot has too many series, select datasets with `--entries` and keep the legend readable; with more than 12 series the legend moves to the right of the plot, in columns (Section 14.2).

### 17.4 A routine that works for any case

1. **Find out what exists:** `python exfor_retrieve.py --target X --available` (all projectiles, quantities and products with data, entries, energy ranges and years), or `--available entries` for the list of EXFOR entries; if the target is not known, `python exfor_retrieve.py --find --projectiles d --product Y` (Section 5). `--projectiles all --summary-only` gives a shorter summary.
2. **Retrieve only what you need:** repeat the command with the projectiles, product, quantity and energy limits chosen, and without `--summary-only`.
3. **Look before plotting:** `python exfor_plot.py --data data/X --list` prints the plots, their series, the x range and the file names.
4. **Plot with the right options for the quantity:** cross sections need nothing special; spectra need `--x Eout`; angular distributions `--x angle`; delayed or prompt data `--branch`; many energies or angles `--at-energy`, `--at-angle`, `--by-energy`, `--by-angle`, the label options or `--map2d` (Section 16).
5. **Clean up the selection:** `--exclude-status SPSDD`, `--exclude-entries`, `--emax`, and the axis options, then save the final figures in the format you need; add `--references` to write the list of references of the plotted datasets.

## 18. Further examples: isotope production, dosimetry, tables and figures

These examples were run on the same EXFOR snapshot as Section 17 (October 2026); the counts will change as EXFOR grows. The retrieve-and-plot commands (`--target`) also save the data in `data/<target name>/`, as described in Section 14.1.

### 18.1 Isotope production for nuclear medicine

**Excitation function of 99mTc from 100Mo(p,2n).** The product 99mTc from protons on 100Mo, with superseded datasets removed:

```bash
python exfor_plot.py --target Mo-100 --projectiles p --product Tc-99m --exclude-status SPSDD
```

This gives 358 points from 11 entries (14 series) between 3.3 and 64.8 MeV (the superseded data of S.Takacs 2003, entry D4115, replaced by entry D4322, are left out; without the filter it is 382 points from 12 entries), in `plots/Mo-100/Mo-100_p_99mTc.png`.

**Thick-target yields.** For production work the yield of a thick target is often more useful than the cross section. It has its own quantity code, `TTY`:

```bash
python exfor_plot.py --target Mo-100 --projectiles p --product Tc-99m --quantity TTY
```

The snapshot has two datasets, in two units (MBq/µAh, 61 points, and µCi/µAh, 7 points), so two plots are written: `Mo-100_p_99mTc_TTY_MBQ_MUAHR.png` and `Mo-100_p_99mTc_TTY_MUCI_MUAHR.png`. The programs do not convert between yield units. Yield data are scarce: for 68Zn(p,x)68Ga the snapshot has only 6 points in 2 datasets, and for 64Ni(p,x)64Cu only 5 points.

**Alpha-induced production of 211At.** 209Bi(α,2n)211At, restricted to the energies of a medical cyclotron:

```bash
python exfor_plot.py --target Bi-209 --projectiles a --product At-211 --exclude-status SPSDD --emax 40
```

Without `--emax` the plot includes 149 points up to 970 MeV; below 40 MeV there are 128 points from 5 entries.

**Choosing the products by half-life.** For the production of radionuclides the half-life decides which products are of interest: long enough to be transported and used, short enough to give a high activity and a small dose. With `--halflife` the datasets file has the half-life of each product in seconds (`product_T12_s`), and a selection is a filter. Natural copper with deuterons, the products with a half-life from 1 hour to 30 days:

```bash
python exfor_retrieve.py --target Cu-nat --projectiles d --quantity SIG --halflife
```

```python
import pandas as pd
ds = pd.read_csv("data/Cu-nat/EXFOR_CU-0_datasets.csv")
ds = ds[ds["product_T12_s"].notna()]
sel = ds[(ds["product_T12_s"] >= 3600) & (ds["product_T12_s"] <= 30 * 86400)]
t = (sel.groupby(["product_label", "product_T12"])
        .agg(entries=("entry", "nunique"), datasets=("dataset", "count"), points=("n_points", "sum"))
        .reset_index().sort_values("points", ascending=False))
print(t.head(8))
print(len(t), "products with 1 h <= T1/2 <= 30 d")
```

```text
product_label product_T12  entries  datasets  points
         64Cu   12.7004 h        9        14     199
         62Zn     9.193 h        5         9     104
         61Cu     3.343 h        6        10      73
         65Ni    2.5175 h        4         7      53
         57Ni     35.60 h        3         7      31
         52Fe     8.275 h        2         6      26
         56Mn    2.5789 h        2         6      24
         52Mn     5.591 d        2         6      23
24 products with 1 h <= T1/2 <= 30 d
```

The 65Zn (243.94 d) and 60Co (5.2714 y) of the catalogue of Section 9.9 are left out by the upper limit. Then retrieve or plot only the products that you keep, for example `--product "Cu-64,Zn-62,Cu-61"`, and the plots show their half-lives (Section 14.12). For a state `M` the half-life that is shown follows the rule of Section 10.2; an isomer with a `?` is worth a look in the entry.

### 18.2 Neutron dosimetry, capture and total cross sections

**Threshold reactions used as neutron dosimeters.** 27Al(n,α)24Na and 56Fe(n,p)56Mn. The option `--process` keeps one reaction type: `A` is the alpha emission and `P` the proton emission (the EXFOR process codes):

```bash
python exfor_plot.py --target Al-27 --projectiles n --product Na-24 --process A
python exfor_plot.py --target Fe-56 --projectiles n --product Mn-56 --process P
```

The first gives 738 points in 89 series from 83 entries (plus 7 points for a 24Na level in a separate file); the second 548 points in 86 series from 75 entries. With so many series the legend goes to the right of the plot in columns (Section 14.2); use `--entries` to compare chosen datasets only.

**Neutron capture over many decades.** 197Au(n,γ)198Au, from 10 meV to 20 MeV, on logarithmic axes:

```bash
python exfor_plot.py --target Au-197 --projectiles n --product Au-198 --process G \
    --xlim 1e-8,20 --logx --logy
```

This writes three files: `Au-197_n_198Au.png` (10,715 points from 108 series), `Au-197_n_198gAu.png` and `Au-197_n_198mAu.png`, because the authors code the state of the product in different ways. Data given as σ√E are converted to mb (Section 14.2). The energy limits are in MeV.

**Total neutron cross section in the fast region.** The total cross section of 56Fe from 1 to 20 MeV (reactions without a product, process TOT):

```bash
python exfor_plot.py --target Fe-56 --projectiles n --product none --process TOT --emin 1 --emax 20
```

This gives 6,363 points from 5 entries in `plots/Fe-56/Fe-56_n_none_TOT.png`.

### 18.3 Cumulative and independent yields

Some products are fed by the decay of a precursor. EXFOR records this in the branch: `CUM` (cumulative) includes the feeding, no code means independent or unspecified. Use `--branch` to separate them. In the natural copper data, 61Cu from deuterons has 48 cumulative points (3 entries) and 26 points without a branch code (4 entries):

```bash
python exfor_plot.py --data data/Cu-nat --projectiles d --product Cu-61 --branch CUM
python exfor_plot.py --data data/Cu-nat --projectiles d --product Cu-61 --branch none
```

The two commands write the same file name, so run them one at a time, or give them different output folders with `--out`. Do not draw cumulative and independent data in one plot to compare them as if they measured the same quantity.

### 18.4 Tables from the data

**A table for Origin or Excel.** The data of one product as a clean CSV, with the cross section in mb and its uncertainty (92mNb from deuterons on 93Nb, 90 points):

```python
import pandas as pd
d = pd.read_csv("data/Nb-93/EXFOR_NB-93_data.csv")
sel = d[(d.projectile == "d") & (d.quantity == "SIG") & (d["product"] == "41-NB-92-M")]
out = (sel[["first_author", "year", "entry", "E_MeV", "dE_MeV", "value", "dvalue"]]
       .rename(columns={"value": "sigma_mb", "dvalue": "dsigma_mb"})
       .sort_values(["entry", "E_MeV"]))
out.to_csv("nb92m_for_origin.csv", index=False)
```

The first rows are M.Avrigeanu, 2013, entry D0713, 3.43 ± 1.11 MeV, 0.131 ± 0.024 mb, and so on. Excel opens the file with Data > From Text/CSV (comma and UTF-8, Section 8.1). The value column is already in mb because the retrieval script converts the cross-section units.

**Who measured what, and when.** A table of the datasets for one product, with the energy range and the number of points (65Zn from deuterons on natural copper):

```python
import pandas as pd
ds = pd.read_csv("data/Cu-nat/EXFOR_CU-0_datasets.csv")
ds = ds[(ds.projectile == "d") & (ds.quantity == "SIG") & (ds.reaction_type == "simple")
        & (ds["product"] == "30-ZN-65")]
t = ds.drop_duplicates("entry")[["first_author", "year", "institute", "E_min_MeV", "E_max_MeV", "n_points"]]
t = t.sort_values("year")
t["year"] = t["year"].astype("Int64")
print(t)
```

The first rows are P.Jung 1991 (8.2 to 13.4 MeV, 2 points), S.Takacs 1996 (5.16 to 20.24 MeV, 44 points) and S.Takacs 2001 (5.30 to 48.90 MeV, 21 points). The column `institute` holds the EXFOR institute codes and sometimes free text, for example (3HUNDEB,2BLGVUB) for Debrecen and Brussels; `facility` describes the accelerator in free text and is not standardised, so do not use it for counting.

### 18.5 Figures

**A multi-panel figure for a paper.** Several products in one figure, two panels per row, one legend for all, in PNG and PDF. Without `--combine` every product gets its own file:

```bash
python exfor_plot.py --data data/Nb-93 --projectiles d --product "92mNb,89Zr,90Nb,93mMo,-89gZr" \
    --exclude-status SPSDD --combine --cols 2 --legend figure --auto-axes --emax 60 --format png,pdf
```

This writes `plots/Nb-93/Nb-93.png` and `Nb-93.pdf`, with four panels and the legend at the bottom. The item `-89gZr` removes the ground state of 89Zr: without it the product `89Zr` selects every state and a fifth panel for 89gZr appears (Section 7.6). With more than nine panels the figure is split into several files (`--max-panels`).

**All saved targets at once.** After retrieving several targets, plot a product from all of them. On Linux and macOS the shell expands the wildcard; on Windows list the folders:

```bash
python exfor_plot.py --data data/* --projectiles d --product "Zn-65,92mNb" --exclude-status SPSDD
```

With the folders `data/Nb-93` and `data/Cu-nat` this writes three plots, in `plots/Cu-nat/` and `plots/Nb-93/`. A product that a target has only as a stray data point is still plotted (here one GeV-range point of 65Zn in the niobium data), so check the plot list with `--list` first.

## 19. Changes from version 1

Version 2.0 adds the projectile selection; the default selection and the main outputs are unchanged.

- New in `exfor_plot.py` 1.4: `--endf` draws evaluated cross sections (ENDF-6 and PENDF files) over the EXFOR data, read by the new `endf_reader.py` (Section 14.14). New in the repository: `build_halflife_db.py` and `lookup_halflife.py` (Section 10.2); the default folders of the master files and of the half-life database are empty and are set by the options, the environment variables `EXFOR_MASTER` and `EXFOR_HALFLIFE_DB`, or the constants (Section 3).
- `--projectiles` accepts `all`, any subset of particle names, heavy ions, groups and exclusions (version 1: only d, p, he3, a). The default is unchanged.
- New options: `--list-projectiles`, `--summary-only` and `--version`.
- New columns in the data file: `projectile_code`, `projectile_Z`, `projectile_A`, `E_per_u_MeV`, `E_unit` and `E_source`. New columns in the datasets file: `projectile_code`, `projectile_raw`, `projectile_Z` and `projectile_A`. The projectile labels d, p, 3He and alpha are unchanged.
- Energies per nucleon and neutron wavelengths are converted; energies in unknown units are left empty with a warning (version 1 read them as MeV).
- EN-MEAN and EN-RSL-FW are used for the energy and its uncertainty.
- The data table is written while the entries are read (memory use is low) and is no longer sorted: rows follow the order of the EXFOR entries. The datasets file is still sorted.
- `--json` now writes `<prefix>_datasets.json` and `<prefix>_data.jsonl` instead of one file.
- Spellings GAMMA, He3 and p in a few EXFOR entries are recognised.

### Changes in version 2.2 and 1.2

Version 2.2 of `exfor_retrieve.py` and version 1.2 of `exfor_plot.py` (build 2026-10-07) have everything that this manual describes for 2.1 and 1.1, and the changes below. The data and datasets files written by 2.1 stay valid. The ASCII files do not: their columns have other names. And the half-lives are no longer printed unless you ask for them. `python exfor_retrieve.py --version` and `python exfor_plot.py --version` must print 2.2 and 1.2 with the build date 2026-10-07; if one of them shows an earlier version or build, or none, replace both scripts (they must be in the same folder).

- **Half-lives are an option.** `--halflife` prints the NUBASE2020 half-life next to each isotope in the summaries, the catalogue and the target search, writes it in the datasets file and in the ASCII index, and puts it in parentheses next to the isotope name in the titles of the plots (the product always, the target when it is radioactive). It is off by default. `--halflife-db` gives the database and switches it on too; `--no-halflife` no longer exists. The light particles n, p, d, t, 3He and alpha have their half-lives like any other nuclide. The database is looked for in `--halflife-db`, in the constant `HALFLIFE_DB_DEFAULT`, in the variable `EXFOR_HALFLIFE_DB` and next to the script (Sections 9.9, 10.2 and 14.12).
- **Default folder of the master files.** It is `MASTER_DEFAULT` at the top of `exfor_retrieve.py` (empty in the repository, or the variable `EXFOR_MASTER`) when it points to an existing folder, and otherwise `exfor_master` in the folder where the command is run, as before; `--master` overrides both (Section 3).
- **Axis labels** are made from the data: the name of the quantity and its unit written out (dσ/dΩ (mb/sr), Double-differential yield (particles/(MeV µC sr)), Fission yield (% per fission) ...) and, for an outgoing energy, the name of the emitted particle (Neutron energy, Photon energy ...). A cross section `SIG` that is a neutron, proton, deuteron, triton, 3He or alpha spectrum is labelled dσ/dE (mb/MeV), also when it is plotted against the incident energy, and the program then advises `--x Eout --by-energy`. When the unit that EXFOR gives contradicts the quantity code, the label shows the code and the unit as they are. `--xlabel` and `--ylabel` replace the labels (Sections 14.13 and 16.7).
- **Names of the columns of the ASCII files**: the quantities and the units are written out in plain ASCII instead of the EXFOR codes (`sigma[mb]`, `dsigma/dOmega[mb/sr]`, `d2sigma/dOmega/dE[mb/sr/MeV]`, `yield_dd[particles/(MeV*uC*sr)]`, `fission_yield[%/fission]`), and the outgoing energy is named after the emitted particle (`E_neutron`, `E_alpha`, `E_gamma`). The names and the rule for the spectra are those of the labels of the plots (Section 8.6.5).
- **Uncertainties in the ASCII files**: every kind of file, also the 2D files, has the uncertainties of the plotted quantities when the dataset gives them: `err_` for the total uncertainty of the value (it was `d`, for example `dSIG`), `err_stat_` and `err_sys_` for the statistical and the systematic one, which EXFOR gives as `ERR-S` and `ERR-SYS` and which were read but not written before, and `err_E` for the incident energy whenever it is a column. The column `uncertainty` of `index.csv` says which of them a file has, and the program prints how many files have none because EXFOR gives none. `--ascii-no-errors` leaves them out; `--ascii-errors` is no longer needed and is ignored (Section 8.6.5).
- **Error bars from the statistical or systematic uncertainty**: a point that has no total uncertainty but a statistical or a systematic one now has an error bar, the two added in quadrature when both are given (Section 14.2).
- **Labels of the angle and energy distributions**: with `--angle-labels` and `--energy-labels` the labels no longer stand on the curves, where they covered data. They are in a column to the right of all the points, the x axis is extended to make room for them, they do not overlap, and a thin line joins a label to the last point of a distribution that ends before the rightmost one. When there are too many distributions to label, an evenly spaced selection is labelled and the program says so (Section 16.5).
- **More EXFOR units are recognised**, for example `MICRO-B`, and the units that are not known are left as EXFOR writes them.
- **Colours of the series**: a palette of ten dark colours (red, blue, green, black, magenta, purple, brown, grey, teal and dark orange) replaces the one of 27 colours, which had yellow, light orange, pink and light green that were hard to see on white. Every colour has a contrast ratio of at least 3.9 against white (Section 14.2).
- **Sums with a compound target are complex reactions.** A reaction such as `((13-AL-27(A,X)0-NN-1,,PY/DA/DE,,TT)+(1-H-PLE(A,X)0-NN-1,,PY/DA/DE,,TT))`, aluminium plus polyethylene, was read as a simple reaction on 27Al because the second term has no mass number in its target code; it is now `complex` (60 reaction fields in 12 entries of the EXFOR snapshot of the tests, for example `1-H-PLE`, `92-U-OXI`, `6-C-CMP`). It matters for the data of entry C3057 (Ratliff 2023), whose six subentries of aluminium plus polyethylene were drawn with the aluminium data. Data retrieved with an earlier build have `simple` for them: retrieve them again (Sections 10 and 16.8).
- **`--entries` and `--exclude-entries` accept subentries**, for example `--entries C3057016`, as well as entries (Section 16.8).
- **An example script**, `plot_Al27_alpha_neutron_spectra.sh`, plots the neutron spectra at several angles from alpha particles on 27Al, one plot for each incident energy and each target configuration (Section 16.8).
- **`--merge-products`** (new in `exfor_plot.py`) draws the selected products of a target and projectile in one plot, with the quantities of one unit merged; the legend gives the product of each series. The emitted particle of an outgoing energy is now worked out for each row, so that the exclusive and the inclusive neutron data share the label Neutron energy (Section 14.3).
- **A general script for the neutron data of an (x,n) reaction**, `plot_neutron_emission.py`, makes the exclusive, the inclusive and the combined plots, and a coverage table of the datasets (Section 16.9).
- **Fixes**: `--stack` with more than about 250 distributions no longer stops with an overflow (the curves are drawn unscaled and the program says so), and the units `P/INC`, `PRT/IN/MEV` and `PRD/MUCOUL` are written out in the labels.
- **`--facility`** (new in `exfor_retrieve.py` 2.3 and `exfor_plot.py` 1.3, build 2026-10-09) keeps only the entries measured at a facility: `ntof` (n\_TOF at CERN, identified by the FACILITY field and by the title, institute and reference), `gelina`, or a regular expression. Without `--target` it retrieves every target of those entries, one folder each. The resonance energy of the width, strength and similar quantities is now taken as the energy of the points, the quantities `RYL`, `WID/STR`, `WID/RED`, `RI`, `STF`, `INT` and `EN` have their own axis labels, and `API_LEVEL` is 2: the two scripts must be updated together (Section 16.10).
- **The example scripts can be run from any folder**: the folders of the programs, the data, the plots and the master files are constants at the top of `plot_neutron_emission.py` (`PROGRAMS_DIR`, `DATA_DIR`, `OUT_DIR`, `MASTER_DIR`) and variables at the top of `plot_Al27_alpha_neutron_spectra.sh` (`PROGRAMS`, `DATA`, `OUT`), with options or variables to replace them (Sections 16.8 and 16.9).
- **The two scripts are checked against each other**: `exfor_plot.py` stops at the start, with a message that gives the version and the path of the file it found, when the `exfor_retrieve.py` next to it is too old (Section 11).
- **`--stack` no longer switches the labels on**: they are drawn only with `--angle-labels` or `--energy-labels`. `--stack` alone draws the scaled distributions without labels and puts a note in the plot that gives the scaling rule (Section 16.5).
- **New sections of the manual**: 8.6.5 (names in the ASCII files), 9.9 (half-lives, examples), 14.12 (half-lives in the titles of the plots), 14.13 (axis labels) and 16.7 (a spectrum coded as a cross section, 27Al(d,n)28Si). Section 13 lists what the programs do not do.
- **Corrected in the manual**: `--product Nb-92m` finds five datasets and 90 points, not four and 89; the fifth is the table of products of Buttsev 1986, which has an isomer flag (Sections 7.6, 8.6, 9.8 and 18.4). Section 16.8 said that EXFOR has no neutron spectra of alpha particles on 27Al below 30 MeV; this was wrong: the data of Jacobs and Liskien 1983 (entry D0757) are such spectra at 4 to 5.5 MeV, coded as reactions to 30P with the quantity MLT, which a search with the neutron as product does not find.
- **Upgrading**: replace both scripts together (they must be in the same folder). Write the ASCII files again with `--ascii`. A program that reads their columns by name needs the new names: `SIG[mb]` is now `sigma[mb]`, `dSIG[mb]` is `err_sigma[mb]`, `dE[MeV]` is `err_E[MeV]`, and `Eout[MeV]` is, for a (d,n) reaction, `E_neutron[MeV]`.

### Changes in version 2.1

Version 2.1 adds the selection of the final product; everything else is unchanged.

- New options `--product` and `--product-exact` (Section 7.6). The default, `all`, gives the same results as version 2.0.
- New columns in the data and datasets files: `product_label`, `product_Z`, `product_A` and `product_state`.
- The console summary lists the products with most points (a line in a normal run, 40 lines with `--summary-only`).
- Products given in the data table (fission fragments, mass yields) are filtered point by point and each point carries its own product.
- Output location: the files of each target now go to `<out>/<target name>/`, by default `data/<target name>/` (for example `data/Nb-93/`). Version 2.0 wrote them to the current folder.
- Spectra whose outgoing energy is given as a bin (E-MIN and E-MAX) or as a bin mean (E-MEAN) now have `E_out_MeV` (for a bin, its mid-point); before, those points had no outgoing energy.
- A COMMON block in the first subentry of an entry (for example a fixed beam energy) now applies to all the data of the entry; before, those points had no incident energy. This affects many neutron-production spectra.
- In `exfor_plot.py`: the new option `--branch` selects delayed or prompt data, quantities other than SIG get one plot per unit, decays are titled with the decay type (Section 15), and `--at-angle`, `--by-energy`, `--by-angle`, `--max-plots`, `--angle-labels`, `--energy-labels`, `--stack`, `--map2d`, `--plot3d`, `--axes` and `--style` handle spectra and double-differential data (Sections 16.1 to 16.6).
- In `exfor_plot.py`, a `--data` path that does not exist yet is now retrieved automatically instead of giving an error (Section 14.5).
- `--version` also prints the date of the last change (build), so that older scripts can be recognised.
- New in `exfor_retrieve.py`: `--available` (catalogue of a target or list of its entries), `--find` (search over all targets), `--max-rows`, and `--references`, `--ref-format` and `--ref-authors` (list of references as text, BibTeX or CSV). `exfor_plot.py` has the same three reference options and writes the references of the plotted datasets next to the plots (Section 5).
- The datasets file has a new column `authors`, and the year of an entry is now also found when the date has a month (`199203`) or is given as YYMM; before, those years were empty (Section 5.5).
- New in `exfor_retrieve.py`: `--master-info` (date of the latest data update of the master files, their git commit, comparison with GitHub), and every retrieval prints the date of the master files it used (Section 3.2).
- New in `exfor_plot.py`: `--ms`, `--alpha`, `--hollow`, `--no-yerr` and `--no-errorbars` for plots with many points, and the series with many points are now drawn first so that sparse datasets stay visible (Section 14.9).
- New in both programs: the product groups `heavy` (every nuclide with Z of 3 or more) and `residual` (the same without the target nucleus itself) for `--product` (Section 7.6).
- New in both programs: `--ascii` writes each dataset as its own ASCII file in columns, with the units in the first row (a 2D distribution as one file with three columns), plus `index.csv`; with `--ascii-dir`, `--ascii-errors` and `--max-ascii` (Sections 8.6 and 9.8). In 2.2 the 2D files have the uncertainties by default and `--ascii-errors` is no longer needed (see above).
- New in both programs: `--ascii-format entry` and `--ascii-format quantity` write fewer, longer ASCII files (one for each publication, or one for each quantity and unit), a dataset whose products are given row by row is one file with the product as the independent variable (235U(n,f) with FY: 1,338 files instead of 10,618, 599 with `entry`, 5 with `quantity`), and the independent variables that are not energies or angles have proper labels with their units, for example `E_transfer[MeV]` (Section 8.6). The data file has two new columns at the end, `dataset` and `extra_units`, and the datasets file has `dataset` (Section 5.5).
- New in both programs: in the ASCII files of a 2D distribution the first column is the variable that labels the blocks (the angle first, then the incident energy, then Z, then the outgoing energy, then A), all the following values of one block follow each other, and a blank line separates the blocks (`--ascii-no-blanks` leaves them out; Section 8.6.3). Section 8.6.4 describes the format of the fission yields.
- New in both programs: the `ISOMER` column of the tables of products (fission yields) is used. A row with the flag 0 has the product state G, 1 the state M and 2 the state M2, so that `--product Kr-85m` selects the isomer, the plots against A, Z and N draw the isomers as a series of their own, the maps and 3D plots as a map of their own, and `--ascii` writes them in a file of their own (`..._isomer-M.dat`). For 235U(n,f) with FY the datasets and points are the same (1,338 and 17,351), the number of files with `--ascii` is 1,427 (Sections 14.11 and 8.6.4). Section 14.11 also describes how fission yields are stored in EXFOR.
- Fix in `exfor_retrieve.py`: the STATUS codes that carry a pointer to another subentry, such as `(SPSDD,D4046006)` and `(DEP,10722002)`, are now read; before, only codes written alone, `(SPSDD)`, were, which are 3 per cent of the SPSDD marks. `--exclude-status SPSDD` therefore now removes the superseded data (for example 65 points of 48V in natTi(d,x)), and `--exclude-status DEP` works. The datasets file has a new column `status_ref` with the pointers. Data retrieved with an earlier version must be retrieved again (Section 10.1).
- New in `exfor_plot.py`: `--list` with `--map2d` or `--plot3d` lists the maps or 3D plots that would be written, with the number of entries (Section 14.10); the limit `--max-plots` counts the maps, not the plots of single products.
- New in both programs (2.1): the half-lives of the isotopes from the NUBASE2020 evaluation are printed next to the target and the products in the summaries, the catalogue and the target search, written in six new columns of the datasets file and in the ASCII index, and put in parentheses next to the isotope name in the titles of the plots, when a SQLite database of half-lives is found (`--halflife-db`); `--no-halflife` switched them off. The state of the EXFOR product (G, M, M1, M2, none) is assigned to a NUBASE state by a rule that was checked against the half-lives quoted in the entries; `--check-halflives` repeats that check on your database. The programs also read the `DECAY-DATA` field of the entries (Section 10.2). In 2.2 the half-lives are an option, `--halflife` (see above).
- New in `exfor_plot.py`: `A`, `Z` and `N` (the mass number, atomic number and neutron number of the fission product) as the x variable (`--x A`) and as axes of the 2D maps and 3D plots (`--axes A,Z`, `N,Z`, `E,A`), for the plots of fission yields (Section 14.10).
