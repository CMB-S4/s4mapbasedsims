import os
import sys

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np

rootdir = "/global/project/projectdirs/cmbs4/dm/dstool/output/s4_reference_design_noise_atmo_7splits"

instruments = "SAT", "LAT"
sites = "pole", "chile"

for instrument in instruments:
    bands = {
        "SAT": ["LFS1", "LFS2", "MFLS1", "MFHS1", "MFLS2", "MFHS2", "HFS1", "HFS2"],
        "LAT": ["ULFL1", "LFL1", "LFL2", "MFL1", "MFL2", "HFL1", "HFL2"],
    }[instrument]
    nside = {"SAT" : 512, "LAT" : 4096}[instrument]
    for site in sites:
        if site == "chile":
            if instrument == "SAT":
                break
            #bands.remove("ULFL1")
        nband = len(bands)
        nrow, ncol = 3, 3
        iplot = 0
        plt.figure(figsize=[12, 8])
        #plt.suptitle("{} - {}".format(instrument, site))
        #plt.subplots_adjust(bottom=0.5)
        for band in bands:
            iplot += 1
            fname = os.path.join(
                rootdir,
                "{}-{}_{}".format(instrument, band, site),
                "cmbs4_KCMB_{}-{}_{}_nside{}_1_of_1.fits".format(instrument, band, site, nside),
            )
            if not os.path.isfile(fname):
                continue
            m = hp.read_map(fname)
            good = m != hp.UNSEEN
            m[good] *= 1e6
            amp = int(np.std(m[good]))
            hp.mollview(
                m,
                norm="hist",
                cmap="coolwarm",
                sub=[nrow, ncol, iplot],
                title=band,
                unit="$\mu$K",
                min=-amp,
                max=amp,
                xsize=1600,
                margins=[.001, .01, .001, .02],
            )
        fname = "collage_{}_{}.png".format(instrument, site)
        plt.savefig(fname)
