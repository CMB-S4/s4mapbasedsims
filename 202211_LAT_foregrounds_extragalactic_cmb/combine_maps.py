import os
import healpy as hp
import numpy as np
from astropy.table import QTable

# Dipole needs to be the last component, I remove dipole
# from previous map before adding dipole
extragalactic = ["cib", "ksz", "tsz", "radio"]
all_combined = {
    "combined_cmb_unlensed_dipole": ["cmb_unlensed_solardipole", "dipole"],
    "combined_cmb_lensing_signal": ["cmb", "-cmb_unlensed_solardipole"],
    "combined_foregrounds_mediumcomplexity": [
        "dust",
        "synchrotron",
        "freefree",
        "ame",
        "co",
    ]
    + extragalactic,
    "combined_foregrounds_lowcomplexity": [
        "dust_low",
        "synchrotron_low",
        "freefree",
        "ame",
        "co_low",
    ]
    + extragalactic,
    "combined_foregrounds_highcomplexity": [
        "dust_high",
        "synchrotron_high",
        "freefree",
        "ame_high",
        "co",
    ]
    + extragalactic,
}

s4 = QTable.read(
    "../202102_design_tool_run/instrument_model/cmbs4_instrument_model.tbl",
    format="ascii.ipac",
)

num = 0

for output_content, components in all_combined.items():
    for telescope in ["LAT"]:
        nside = 512 if telescope == "SAT" else 4096
        for row in s4:
            band = row["band"]
            if row["telescope"] == telescope:
                output_filename = f"output_lsq/{nside}/{output_content}/{num:04d}/cmbs4_{output_content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"
                if not os.path.exists(output_filename):
                    combined_map = np.zeros((3, hp.nside2npix(nside)), dtype=np.float64)
                    for content in components:
                        print(content)
                        sign = 1
                        if content.startswith("-"):
                            sign = -1
                            content = content[1:]
                        if content == "dipole":
                            filename = f"output_lsq/{nside}/cmbs4_cmb_solar_dipole_uKCMB_nside{nside}.fits"
                        else:
                            filename = f"output_lsq/{nside}/{content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"
                        try:
                            m = hp.read_map(
                                filename, dtype=np.float64, field=(0, 1, 2), nest=True
                            )
                            if content == "cmb_unlensed_solardipole":
                                m[0] = hp.remove_dipole(m[0], nest=True)
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
