import os
import healpy as hp
import numpy as np
from astropy.table import QTable
from pathlib import Path

extragalactic = ["cib_cib1", "ksz_ksz1", "tsz_tsz1", "radio_rg1"]
all_combined = {
    "combined_cmb_unlensed_dipole": ["cmb_c3", "dipole"],
    "combined_cmb_lensing_signal": ["cmb_c4", "-cmb_c3"],
    "combined_foregrounds_mediumcomplexity": [
        "dust_d10",
        "synchrotron_s4",
        "freefree_f1",
        "ame_a1",
        "co_co3",
    ]
    + extragalactic,
    "combined_foregrounds_lowcomplexity": [
        "dust_d9",
        "synchrotron_s5",
        "freefree_f1",
        "ame_a1",
        "co_co1",
    ]
    + extragalactic,
    "combined_foregrounds_highcomplexity": [
        "dust_d12",
        "synchrotron_s7",
        "freefree_f1",
        "ame_a2",
        "co_co3",
    ]
    + extragalactic,
}

s4 = QTable.read(
    "instrument_model/cmbs4_instrument_model.tbl",
    format="ascii.ipac",
)

num = 0
output_folder = Path("/global/cfs/cdirs/cmbs4/dc/dc0/sky/")
output_folder = Path("output")

for output_content, components in all_combined.items():
    for row in s4:
        band = row["band"]
        print(band)
        nside = 512 if row["telescope"] == "SAT" else 4096
        output_filename = (
            output_folder
            / f"{output_content}/cmbs4_{output_content}_uKCMB_{band}_nside{nside}.fits"
        )
        if os.path.exists(output_filename):
            print("skip", output_filename)
        else:
            combined_map = np.zeros((3, hp.nside2npix(nside)), dtype=np.float64)
            for content in components:
                print(content)
                sign = 1
                if content.startswith("-"):
                    sign = -1
                    content = content[1:]
                if content == "dipole":
                    filename = (
                        output_folder
                        / f"dipole/cmbs4_cmb_solar_dipole_uKCMB_nside{nside}.fits"
                    )
                else:
                    filename = (
                        output_folder
                        / f"{content}/cmbs4_{content}_uKCMB_{band}_nside{nside}.fits"
                    )
                try:
                    m = hp.read_map(
                        filename, dtype=np.float64, field=(0, 1, 2), nest=True
                    )
                    combined_map += sign * m
                except IndexError:
                    print("T only map")
                    combined_map[0] += sign * hp.read_map(
                        filename, dtype=np.float64, field=0, nest=True
                    )
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)
            hp.write_map(
                output_filename,
                combined_map,
                nest=True,
                coord="C",
                column_units="uK_CMB",
                overwrite=True,
                dtype=np.float32,
            )
            print(20 * "*")
            print(output_filename)
            print(20 * "*")
