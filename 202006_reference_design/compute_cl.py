import healpy as hp
import numpy as np
import sys
from glob import glob
import pickle
import h5py
from pathlib import Path

ellmax = int(1e4)

s4 = h5py.File("cmbs4_tophat.h5", mode="r")
cl = {}
telescope = sys.argv[1]
splits = int(sys.argv[2])
sites = ["chile", "pole"]

if telescope == "SAT":
    sites = sites[1:]
for folder in glob("output/*noise*"):
    folder = Path(folder)
    print(folder)
    output_filename = folder / f"C_ell_{telescope}_{splits}.pkl"
    for site in sites:

        for ch in [c for c in s4.keys() if s4[c].attrs["telescope"] == telescope]:
            tag = f"{telescope}-{ch}_{site}"
            ch_folder = folder / tag
            hitmap_filenames = list(ch_folder.glob(f"*hitmap*1_of_{splits}*"))
            assert(len(hitmap_filenames) == 1)
            hitmap_filename = hitmap_filenames[0]
            hitmap = hp.read_map(hitmap_filename)
            hitmap[hitmap == hp.UNSEEN] = 0
            sky_fraction = (hitmap > 0).sum()/len(hitmap)

            hitmap[hitmap>0] = np.sqrt(hitmap[hitmap>0])

            assert np.all(np.isfinite(hitmap))
            print(tag)
            cl[tag] = {}
            for s in range(1, splits+1):
                try:
                    filenames = list(ch_folder.glob(f"*KCMB*{s}_of_{splits}*"))
                    assert len(filenames) == 1
                    filename = filenames[0]
                except:
                    print(f"{ch_folder} NOT FOUND " + ("*" * 20))
                    continue
                print(f"reading {filename}")
                try:
                    m = hp.ma(hp.read_map(filename, (0, 1, 2)))
                    nside = hp.npix2nside(len(m[0]))
                except:
                    m = hp.ma(hp.read_map(filename))
                    nside = hp.npix2nside(len(m))

                assert np.all(np.isfinite(m))
                cl[tag][s] = hp.anafast(m*hitmap, lmax=min(3 * nside - 1, ellmax), use_pixel_weights=True) / np.mean(hitmap**2) / sky_fraction

    with open(output_filename, "wb") as f:
        pickle.dump(cl, f, protocol=-1)
