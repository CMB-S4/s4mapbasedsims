from pathlib import Path
import sys
import subprocess

folder = Path(f"jobs")
folder.mkdir(exist_ok=True, parents=True)

no_nside_sims = ["cib", "ksz", "tsz", "radio", "cmb", "cmb_unlensed"]
nside_sims = ["dust", "synchrotron", "freefree", "ame", "co"]

sims = nside_sims + no_nside_sims
from glob import glob
sims = list(glob("*low*.toml")) + list(glob("*high*.toml"))
sims = [s.split(".")[0] for s in sims]

from mapsims.channel_utils import parse_channels

instrument_parameters = (
    "../202102_design_tool_run/instrument_model/cmbs4_instrument_model.tbl"
)
chs = parse_channels("telescope:LAT", instrument_parameters)
for simulation_type in sims:
    config_file = simulation_type
    template = open("submit.slurm").read()
    hours = 4
    minutes = 30
    nside = 4096
    for channel in chs:
        tag = channel.tag.replace(" ", "_")
        filename = f"job_{simulation_type}_{nside}_{tag}.slurm"
        with open(folder / filename, "w") as f:
            print(f"sbatch jobs/{filename} &")
            f.write(
                template.format(
                    simulation_type=simulation_type,
                    nside=nside,
                    hours=hours,
                    minutes=minutes,
                    channels=tag,
                    run_channels=tag,
                    config_file=config_file,
                )
            )

        subprocess.run(["sbatch", f"jobs/{filename}"])
    #nside = 512
    #filename = f"job_{simulation_type}_{nside}_LAT.slurm"
    #with open(folder / filename, "w") as f:
    #   print(f"sbatch jobs/{filename} &")
    #   f.write(template.format(
    #       simulation_type=simulation_type,
    #       nside=nside,
    #       hours=hours,
    #       minutes=minutes,
    #       channels='LAT',
    #       run_channels='telescope:LAT',
    #       config_file=config_file
    #   ))

    #subprocess.run(["sbatch", f"jobs/{filename}"])
