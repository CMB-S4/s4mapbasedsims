import os
import healpy as hp
import numpy as np

all_combined = {
    "combined_foregrounds": ["dust", "synchrotron", "freefree", "ame"]
    + ["cib", "ksz", "tsz"],
    "cmb_lensing_signal": ["cmb", "-cmb_unlensed"],
    "cmb_unlensed_solardipole_nest": ["cmb_unlensed_solardipole"],
}

import h5py

s4 = h5py.File("cmbs4_tophat.h5", "r")

num = 0

for output_content, components in all_combined.items():
    for nside in [512]:
        for telescope in ["SAT"]:
            for band in [b for b in s4.keys() if s4[b].attrs["telescope"] == telescope]:
                output_filename = f"output/{nside}/{output_content}/{num:04d}/cmbs4_{output_content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"
                if not os.path.exists(output_filename):
                    combined_map = np.zeros((3, hp.nside2npix(nside)), dtype=np.float32)
                    for content in components:
                        sign = 1
                        if content.startswith("-"):
                            sign = -1
                            content = content[1:]
                        filename = f"output/{nside}/{content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"
                        print(filename)
                        print(float(s4[band]["bandpass_frequency_GHz"][0]))
                        try:
                            combined_map += sign * hp.read_map(
                                filename, dtype=np.float32, field=(0, 1, 2)
                            )
                        except IndexError:
                            print("T only map")
                            combined_map[0] += sign * hp.read_map(
                                filename, dtype=np.float32, field=0
                            )
                    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                    combined_map = hp.reorder(combined_map, r2n=True)
                    hp.write_map(
                        output_filename,
                        combined_map,
                        nest=True,
                        coord="C",
                        column_units="uK_CMB",
                        overwrite=True,
                    )
                    print(20 * "*")
                    print(output_filename)
                    print(20 * "*")
