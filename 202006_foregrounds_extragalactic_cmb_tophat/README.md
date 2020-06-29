Tophat bandpasses simulation: high resolution foregrounds with spectral index not varying spatially and extragalactic
=====================================================================================================================

Released on 8 June 2020 by @zonca

Rerun of the `202002_foregrounds_extragalactic_cmb_tophat` set with fixed beams.

It includes all galactic high resolution components with index not varying spatially and the extragalactic
components based on WebSky. Integrated on top-hat bandpasses based on the instrument model from `s4sim`.

The last version of this file is [available on Github](https://github.com/CMB-S4/s4mapbasedsims/tree/master/202006_foregrounds_extragalactic_cmb_tophat).
The same folder contains all the configuration files used and the scripts to create SLURM jobs.

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/highres_templates.html#details-about-individual-models).

The CIB, KSZ and TSZ models are created from WebSky cosmological simulations, 
we also include one CMB realization generated with the same cosmological parameters used in the WebSky simulations both unlensed and lensed with the potential from the WebSky simulations,
see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/models.html#websky).
For convenience, here are the [cosmological parameters assumed in WebSky](https://mocks.cita.utoronto.ca/data/websky/v0.0/cosmology.py).

All the models listed above will be part of PySM 3 once we upgrade them to nside 8192 and merge them in.

I also created a version of the lensed CMB realization with the dipole component replaced by the [HFI 2018 solar dipole](https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Map-making#HFI_2018_Solar_dipole)

## Instrument properties

Bandpass for each channel is based on the figures in `s4sim.hardware.config`, PySM executes 10 equally spaced points between the low and the high limit, including both and integrates with the trapezoidal rule. Weighting is performed in `Jy/sr`, the same as PySM 2.

Using version `0+untagged.115.gc57d15d` of the `s4sim` package, see `cmbs4_tophat.h5` or `cmbs4_tophat.csv` for the actual values used for beam and bandpass.

## Available maps

HEALPix maps at high resolution for LAT (nside 4096) and low resolution for SAT (nside 512), these models are deterministic, so we have
a set for each resolution for all channels. All maps are full-sky.

Reference frame for the maps is **Equatorial**.
The `ell_max` for the harmonics transform is `3*Nside-1`.

**Location at NERSC**:

    /global/cscratch1/sd/zonca/cmbs4/map_based_simulations/202006_foregrounds_extragalactic_cmb_tophat

The naming convention is:

    {nside}/{content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"

where:

* `content` is `[dust, synchtrotron, freefree, ame]` for galactic components and `[ksz, tsz, cib]` for extragalactic components
* `content` for the available CMB is `[cmb, cmb_unlensed, cmb_lensed_solardipole]`
*  CIB map for LFL1 and LFS1 are missing
* `num` is `0`
* `telescope` is `SAT` or `LAT`
* `band` is the channel band

## Combined maps

Also created a single set of maps which is the sum of all components. They are also reordered to NEST (default for TOAST).

* `combined_foregrounds`: sum of `dust`, `synchrotron`, `freefree`, `ame`, `cib`, `ksz`, `tsz`
* `cmb_lensing_signal`: `cmb` minus `cmb_unlensed`
* `cmb_unlensed_solardipole_nest`: `cmb_unlensed_solardipole`, just reordered to HEALPix NEST
* `cmb_tensor_nest`: `cmb_tensor`, just reordered to HEALPix NEST

They are in the same folder and same naming convention, e.g.:

    /global/cscratch1/sd/zonca/cmbs4/map_based_simulations/202006_foregrounds_extragalactic_cmb_tophat/512/combined_foregrounds/0000/cmbs4_combined_foregrounds_uKCMB_SAT-LFS1_nside512_0000.fits

## Plots and validation

Only at NSIDE 512, comparison of all the channels with on-the-fly PySM simulations ran without the pipeline, just at the center frequency of the lower and higher frequency channel.

Plots are interactive, first click on the "Click here to toggle on/off the raw code" buttone, then click on the legend to select channel, double-click on plot to reset, zoom with scrolling.

* [Plot TT NSIDE 512](https://nbviewer.jupyter.org/gist/zonca/6b6f142babb63526be91dc9d61667b9f)
* [Plot EE NSIDE 512](https://nbviewer.jupyter.org/gist/zonca/822c19ee590112f2d11be7bb183850f5)
* [Plot BB NSIDE 512](https://nbviewer.jupyter.org/gist/zonca/af05f08e29dd26df82b85ea3137be5fa)

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `s4mapbasedsims` repo](https://github.com/CMB-S4/s4mapbasedsims/issues)

## Software

* PySM 3 is available at <https://github.com/healpy/pysm>
