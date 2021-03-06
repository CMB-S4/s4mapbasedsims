import os
os.environ["OMP_NUM_THREADS"] = "64"
import healpy as hp
import numpy as np
import sys
import pickle
from pathlib import Path

from compute_cl_utils import build_inverse_cov_weights

from astropy.table import QTable
ellmax = int(1e4)

cl = {}
telescope = sys.argv[1]
splits = int(sys.argv[2])
sites = ["chile", "pole"]

s4 = QTable.read("instrument_model/cmbs4_instrument_model.tbl", format="ascii.ipac")
s4 = s4[s4["telescope"] == telescope]

local_folder = Path("output/")  # local
output_base_folder = Path("output/")  # project
output_base_folder = local_folder

noise_folder = output_base_folder / "noise_atmo_7splits"

for folder in output_base_folder.glob("*noise*"):
    folder = Path(folder)
    for site in sites:
        output_filename = local_folder / folder.name / f"C_ell_{telescope}_{site}_{splits}.pkl"
        if output_filename.exists():
            continue

        for row in s4:
            ch = row["band"]
            tag = f"{telescope}-{ch}_{site}"
            ch_folder = folder / tag
            if not ch_folder.exists():
                continue
            wcov_filenames = list((noise_folder / tag).glob(f"*wcov*1_of_{splits}*"))
            assert len(wcov_filenames) == 1
            wcov_filename = wcov_filenames[0]
            temp_weights, pol_weights = None, None
            if "noise" in str(folder.resolve()):
                temp_weights, pol_weights, _ = build_inverse_cov_weights(
                    wcov_filename
                )

            print(tag)
            cl[tag] = {}
            for s in range(1, splits + 1):
                try:
                    filenames = list(ch_folder.glob(f"*KCMB*{s}_of_{splits}*"))
                    assert len(filenames) == 1
                    filename = filenames[0]
                except:
                    print(f"{ch_folder} NOT FOUND " + ("*" * 20))
                    continue
                print(f"reading {filename}")
                m = hp.ma(hp.read_map(filename, (0, 1, 2)))
                nside = hp.npix2nside(len(m[0]))

                if temp_weights is None:
                    print(f"using uniform weighting")
                    temp_weights = np.logical_not(m.mask[0])
                    pol_weights = temp_weights

                m[0] *= temp_weights
                m[1:] *= pol_weights
                assert np.all(np.isfinite(m))
                cl[tag][s] = hp.anafast(
                    m, lmax=min(3 * nside - 1, ellmax), use_pixel_weights=True
                )

                cl[tag][s][0] /= np.mean(temp_weights ** 2)
                cl[tag][s][1:] /= np.mean(pol_weights ** 2)

        with open(output_filename, "wb") as f:
            pickle.dump(cl, f, protocol=-1)
