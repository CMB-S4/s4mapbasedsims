import os
import sys

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np

rootdir = "/global/project/projectdirs/cmbs4/dm/dstool/output/s4_reference_design_noise_atmo_7splits"
rootdir2 = "/global/cscratch1/sd/keskital/s4sim/reference_tool/out_v1/00000000/"

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
        nrow, ncol = 4, 8
        plt.figure(figsize=[18, 8])
        #plt.suptitle("{} - {}".format(instrument, site))
        #plt.subplots_adjust(bottom=0.5)
        for icomp, comp in enumerate(["sky", "noise", "atmosphere", "total"]):
            iplot = icomp * ncol
            for band in bands:
                iplot += 1
                if site == "chile" and band == "ULFL1":
                    continue
                cbar = False
                if comp == "sky":
                    fnames = [
                        os.path.join(
                            rootdir2,
                            "{}_foreground_{}_{}_filtered_telescope_all_time_all_bmap.fits".format(
                                site, instrument, band,
                            )
                        ),
                        os.path.join(
                            rootdir2,
                            "{}_cmb-unlensed_{}_{}_filtered_telescope_all_time_all_bmap.fits".format(
                                site, instrument, band,
                            ),
                        ),
                    ]
                elif comp in ["noise", "atmosphere"]:
                    fnames = [
                        os.path.join(
                            rootdir2,
                            "{}_{}_{}_{}_filtered_telescope_all_time_all_bmap.fits".format(
                                site, comp, instrument, band,
                            )
                        ),
                    ]
                else:
                    fnames = [
                        os.path.join(
                            rootdir,
                            "{}-{}_{}".format(instrument, band, site),
                            "cmbs4_KCMB_{}-{}_{}_nside{}_1_of_1.fits".format(
                                instrument, band, site, nside),
                        ),
                    ]
                    cbar = True

                m = None
                for fname in fnames:
                    if not os.path.isfile(fname):
                        continue
                    if m is None:
                        m = hp.read_map(fname, [1, 2])
                    else:
                        m2 = hp.read_map(fname, [1, 2])
                        good = m != hp.UNSEEN
                        m[good] += m2[good]
                if m is None:
                    continue
                good = m != hp.UNSEEN
                m[good] *= 1e6
                amp = int(np.std(m[good]) * np.sqrt(2))
                bad = m[0] == hp.UNSEEN
                m = np.sqrt(m[0] ** 2 + m[1] ** 2)
                m[bad] = hp.UNSEEN
                hp.mollview(
                    m,
                    norm="hist",
                    cmap="coolwarm",
                    sub=[nrow, ncol, iplot],
                    title="{}-{}".format(comp, band),
                    unit="$\mu$K",
                    cbar=cbar,
                    min=0,
                    max=amp,
                    xsize=1600,
                    margins=[.001, .01, .001, .02],
                )
        fname = "components_{}_{}.P.png".format(instrument, site)
        plt.savefig(fname)
