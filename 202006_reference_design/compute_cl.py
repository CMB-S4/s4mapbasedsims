import healpy as hp
import numpy as np
import pickle
import h5py
from pathlib import Path

ellmax = int(1e4)

s4 = h5py.File("cmbs4_tophat.h5", mode="r")
cl = {}
telescope = sys.argv[1]
splits = int(sys.argv[2])
sites = ["chile"]

local_folder = Path("output/") # local
output_base_folder = Path("/global/project/projectdirs/cmbs4/dm/dstool/output/") # project
output_base_folder = local_folder

for folder in output_base_folder.glob("*noise*"):
    folder = Path(folder)
    output_filename = local_folder / folder.name / f"C_ell_{telescope}_{splits}.pkl"
    for site in sites:

        for ch in [c for c in s4.keys() if s4[c].attrs["telescope"] == telescope]:
            tag = f"{telescope}-{ch}_{site}"
            ch_folder = folder / tag
            hitmap_filenames = list(ch_folder.glob(f"*wcov*1_of_{splits}*"))
            assert(len(hitmap_filenames) == 1)
            hitmap_filename = hitmap_filenames[0]
            hitmap = hp.ma(hp.read_map(hitmap_filename, (3, 5)))
            hitmap = 1/hitmap
            hitmap = hitmap.filled(0)

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

                for i_pol in [1,2]:
                    m[i_pol] *= hitmap[i_pol-1]
                norm = np.mean(hitmap[0]*hitmap[1])
                del hitmap
                assert np.all(np.isfinite(m))
                cl[tag][s] = hp.anafast(m, lmax=min(3 * nside - 1, ellmax), use_pixel_weights=True) / norm

    with open(output_filename, "wb") as f:
        pickle.dump(cl, f, protocol=-1)
