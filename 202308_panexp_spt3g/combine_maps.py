import os
import toml
import healpy as hp
import numpy as np
from astropy.table import QTable
from pathlib import Path

nside = 2048

extragalactic = ["cib_cib1", "ksz_ksz1", "tsz_tsz1", "radio_rg1"]
all_combined = {
    "combined_cmb_unlensed_dipole": ["cmb_c3", "dipole"],
    "combined_cmb_lensing_signal": ["cmb_c4", "-cmb_c3"],
    "combined_foregrounds_mediumcomplexity": [
        "dust_d10",
        "synchrotron_s5",
        "freefree_f1",
        "ame_a1",
        "co_co3",
    ]
    + extragalactic,
    "combined_foregrounds_lowcomplexity": [
        "dust_d9",
        "synchrotron_s4",
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

config = toml.load("common.toml")

instrument_model = QTable.read(
    config["instrument_parameters"],
    format="ascii.ipac",
)

num = 0
output_folder = config["output_folder"]

for output_content, components in all_combined.items():
    for row in instrument_model:
        try:
            print(row["tag"])
        except KeyError:
            print(row["band"])
        filename_template = config["output_filename_template"].format(
            tag="{tag}",
            band=row["band"],
            nside=nside,
        )
        output_filename = os.path.join(
            output_folder.format(tag=output_content),
            filename_template.format(
                tag=output_content,
            ),
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
                    filename = os.path.join(
                        output_folder.format(tag=content),
                        f"cmb_solar_dipole_uKCMB_nside{nside}.fits",
                    )
                else:
                    filename = os.path.join(output_folder, filename_template).format(
                        tag=content
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
                coord=config["output_reference_frame"],
                column_units=config["unit"],
                overwrite=True,
                dtype=np.float32,
            )
            print(20 * "*")
            print(output_filename)
            print(20 * "*")
