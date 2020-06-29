from pathlib import Path
import subprocess

folder = Path(f"jobs")
folder.mkdir(exist_ok=True, parents=True)

nside_sims = ["dust", "freefree", "synchrotron", "ame"]
no_nside_sims = ["cib", "ksz", "tsz", "cmb", "cmb_tensor", "cmb_unlensed", "cmb_unlensed_solardipole"]

import h5py
s4 = h5py.File("cmbs4_tophat.h5", mode="r")
sims = nside_sims + no_nside_sims

for simulation_type in sims:
    config_file = simulation_type if simulation_type in no_nside_sims else simulation_type + "_" + str(nside)
    template = open("submit.slurm").read()
    hours = 2
    minutes = 30
    nside = 4096
    for channels in s4.keys():
        if s4[channels].attrs["telescope"] == "LAT":
            filename = f"job_{simulation_type}_{nside}_{channels}.slurm"
            with open(folder / filename, "w") as f:
                print(f"sbatch jobs/{filename} &")
                f.write(template.format(
                    simulation_type=simulation_type,
                    nside=nside,
                    hours=hours,
                    minutes=minutes,
                    channels=channels,
                    run_channels=channels,
                    config_file=config_file
                ))

            subprocess.run(["sbatch", f"jobs/{filename}"])
    nside = 512
    filename = f"job_{simulation_type}_{nside}_SAT.slurm"
    with open(folder / filename, "w") as f:
        print(f"sbatch jobs/{filename} &")
        f.write(template.format(
            simulation_type=simulation_type,
            nside=nside,
            hours=hours,
            minutes=minutes,
            channels='SAT',
            run_channels='telescope:SAT',
            config_file=config_file
        ))

    subprocess.run(["sbatch", f"jobs/{filename}"])
