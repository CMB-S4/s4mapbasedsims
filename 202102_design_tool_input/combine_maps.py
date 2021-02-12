import os
import healpy as hp
import numpy as np
from astropy.table import QTable

all_combined = {
    "combined_foregrounds": ["dust", "synchrotron", "freefree", "ame"]
    + ["cib", "ksz", "tsz"],
    "cmb_lensing_signal": ["cmb", "-cmb_unlensed"],
}

s4 = QTable.read("../202102_design_tool_run/instrument_model/cmbs4_instrument_model.tbl", format="ascii.ipac")

num = 0

for output_content, components in all_combined.items():
    for nside in [512]:
        for telescope in ["SAT"]:
            for row in s4:
                band = row["band"]
                if row["telescope"] == telescope:
                    output_filename = f"output/{nside}/{output_content}/{num:04d}/cmbs4_{output_content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"
                    if not os.path.exists(output_filename):
                        combined_map = np.zeros((3, hp.nside2npix(nside)), dtype=np.float32)
                        for content in components:
                            sign = 1
                            if content.startswith("-"):
                                sign = -1
                                content = content[1:]
                            filename = f"output/{nside}/{content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"
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
