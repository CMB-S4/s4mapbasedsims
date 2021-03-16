import os

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

rootdir = Path("../output/")

instruments = "SAT", "LAT"
sites = "pole", "chile"


for pol in ["T", "P"]:

    if pol == "T":
        fixed_amp = {("SAT", "pole"): 10, ("LAT", "chile"): 10, ("LAT", "pole"): 10}
    else:
        fixed_amp = {("SAT", "pole"): 5, ("LAT", "chile"): 100, ("LAT", "pole"): 100}

    for instrument in instruments:
        bands = {
            "SAT": ["LFS1", "LFS2", "MFLS1", "MFHS1", "MFLS2", "MFHS2", "HFS1", "HFS2"],
            "LAT": ["ULFL1", "LFL1", "LFL2", "MFL1", "MFL2", "HFL1", "HFL2"],
        }[instrument]
        nside = {"SAT": 512, "LAT": 4096}[instrument]
        for site in sites:
            if site == "chile":
                if instrument == "SAT":
                    break
                # bands.remove("ULFL1")
            nband = len(bands)
            nrow, ncol = 4, 8
            plt.figure(figsize=[18, 7])
            # plt.suptitle("{} - {}".format(instrument, site))
            # plt.subplots_adjust(bottom=0.5)

            comp_folder = {
                "foregrounds": "foregrounds",
                "cmb": "cmb_r0",
                "cmb_tensor": "cmb_tensor_only_r3e-3",
            }
            for icomp, comp in enumerate(
                ["foregrounds", "cmb", "cmb_tensor", "noise+atmo"]
            ):
                iplot = icomp * ncol
                for band in bands:
                    if instrument == "LAT" and site == "pole":
                        band = band.replace("FL", "FPL")
                    print(instrument, site, comp, band)
                    iplot += 1
                    if site == "chile" and band == "ULFL1":
                        continue
                    cbar = False
                    if comp == "noise+atmo":
                        fnames = [
                            os.path.join(
                                rootdir,
                                "noise_atmo_7splits",
                                "{}-{}_{}".format(instrument, band, site),
                                "cmbs4_KCMB_{}-{}_{}_nside{}_1_of_1.fits".format(
                                    instrument, band, site, nside
                                ),
                            ),
                        ]
                        cbar = True
                    else:
                        fnames = [
                            os.path.join(
                                rootdir,
                                comp_folder[comp],
                                "{}-{}_{}".format(instrument, band, site),
                                "cmbs4_KCMB_{}-{}_{}_nside{}_1_of_1.fits".format(
                                    instrument, band, site, nside
                                ),
                            ),
                        ]
                    print(fnames)
                    assert len(fnames) == 1

                    m = None
                    for fname in fnames:
                        if not os.path.isfile(fname):
                            continue
                        if m is None:
                            m = hp.read_map(fname, [1, 2] if pol == "P" else 0)
                    if m is None:
                        continue
                    good = m != hp.UNSEEN
                    m[good] *= 1e6
                    amp = fixed_amp.get(
                        (instrument, site)
                    )
                    if pol == "P":
                        bad = m[0] == hp.UNSEEN
                        m = np.sqrt(m[0] ** 2 + m[1] ** 2)
                        m[bad] = hp.UNSEEN
                    hp.mollview(
                        m,
                        cmap="coolwarm",
                        sub=[nrow, ncol, iplot],
                        title="{}-{}".format(comp, band),
                        unit="$\mu$K",
                        cbar=cbar,
                        min=0 if pol == "P" else -amp,
                        max=amp,
                        xsize=1600,
                        margins=[0.001, 0.01, 0.001, 0.01],
                    )
            fname = "components_{}_{}.{}.png".format(instrument, site, pol)
            plt.savefig(fname)
