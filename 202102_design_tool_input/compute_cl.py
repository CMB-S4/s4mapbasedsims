import healpy as hp
from glob import glob
import pickle
import h5py

ellmax = int(1e4)
import os.path

from astropy.table import QTable


s4 = QTable.read("../202102_design_tool_run/instrument_model/cmbs4_instrument_model.tbl", format="ascii.ipac")
cl = {}
for folder in glob("output/512/*ame*"):
    print(folder)
    component = os.path.basename(folder)
    output_filename = f"output/512/C_ell_{component}.pkl"
    if os.path.exists(output_filename):
        continue

    for ch in s4:
        if ch["telescope"] == "SAT":
            try:
                filename = glob(folder + f"/0000/*{ch['band']}*")[0]
            except IndexError:
                print(folder + f"/0000/*{ch['band']}* NOT FOUND " + ("*" * 20))
            print("reading " + filename)
            try:
                m = hp.read_map(filename, (0, 1, 2))
                nside = hp.npix2nside(len(m[0]))
            except:
                m = hp.read_map(filename)
                nside = hp.npix2nside(len(m))

            #if m.shape[0] == 3 and m[1].sum() == 0:
            #    m = m[0]

            cl[ch['band']] = hp.anafast(m, lmax=min(3 * nside - 1, ellmax), use_pixel_weights=True)

    with open(output_filename, "wb") as f:
        pickle.dump(cl, f, protocol=-1)
