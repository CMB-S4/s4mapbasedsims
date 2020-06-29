import healpy as hp
import sys
from glob import glob
import pickle
import h5py
from pathlib import Path

ellmax = int(1e4)
import os.path

s4 = h5py.File("cmbs4_tophat.h5", mode="r")
cl = {}
telescope = "SAT"
sites = ["chile", "pole"]
if telescope == "SAT":
    sites = sites[1:]
for folder in glob("output/*"):
    for site in sites:
        folder = Path(folder)
        print(folder)
        output_filename = folder / f"C_ell_{telescope}.pkl"
        if os.path.exists(output_filename):
            continue

        for ch in [c for c in s4.keys() if s4[c].attrs["telescope"] == telescope]:
            tag = f"{telescope}-{ch}_{site}"
            try:
                ch_folder = folder / tag
                filename = list(ch_folder.glob("*1_of_1*"))[0]
            except IndexError:
                print(f"{ch_folder} NOT FOUND " + ("*" * 20))
                sys.exit(1)
            print(f"reading {filename}")
            try:
                m = hp.read_map(filename, (0, 1, 2))
                nside = hp.npix2nside(len(m[0]))
            except:
                m = hp.read_map(filename)
                nside = hp.npix2nside(len(m))

            cl[tag] = hp.anafast(m, lmax=min(3 * nside - 1, ellmax))

        with open(output_filename, "wb") as f:
            pickle.dump(cl, f, protocol=-1)
