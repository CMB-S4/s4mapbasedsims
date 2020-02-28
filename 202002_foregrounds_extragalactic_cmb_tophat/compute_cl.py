import healpy as hp
from glob import glob
import pickle
import h5py

ellmax = int(1e4)
import os.path

s4 = h5py.File("cmbs4_tophat.h5", mode="r")
cl = {}
for folder in glob("output/512/*"):
    print(folder)
    component = os.path.basename(folder)
    output_filename = f"output/512/C_ell/{component}.pkl"
    if os.path.exists(output_filename):
        continue

    for ch in [c for c in s4.keys() if s4[c].attrs["telescope"]=="SAT"]:
        try:
            filename = glob(folder + f"/0000/*{ch}*")[0]
        except IndexError:
            print(folder + f"/0000/*{ch}* NOT FOUND " + ("*"*20)) 
        print("reading " + filename)
        try:
            m = hp.read_map(filename, (0,1,2))
            nside = hp.npix2nside(len(m[0]))
        except:
            m = hp.read_map(filename)
            nside = hp.npix2nside(len(m))

        cl[ch] = hp.anafast(m, lmax=min(3*nside-1,ellmax))

    with open(output_filename, "wb") as f:
        pickle.dump(cl, f, protocol=-1)
