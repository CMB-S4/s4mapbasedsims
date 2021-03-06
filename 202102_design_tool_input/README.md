Design tool run inputs: foregrounds, CMB, extragalactic
=======================================================

Released on 12 February 2021 by @zonca

Executed with the same configuration of `202006_foregrounds_extragalactic_cmb_tophat`

It includes all galactic high resolution components with index not varying spatially and the extragalactic
components based on WebSky. Integrated on top-hat bandpasses based on the instrument model from `s4sim`.

## Instrument properties

See the documentation of the [`202102_design_tool_run`](https://github.com/CMB-S4/s4mapbasedsims/tree/master/202102_design_tool_run)

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

Dust, synchrotron, free-free and anomalous microwave emission using the "0" models, i.e. `SO_d0`, `SO_s0`, `SO_f0`, and `SO_a0`, see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/highres_templates.html#details-about-individual-models).

The CIB, KSZ and TSZ models are created from WebSky cosmological simulations, 
we also include one CMB realization generated with the same cosmological parameters used in the WebSky simulations both unlensed and lensed with the potential from the WebSky simulations,
see more details in [in the documentation](https://so-pysm-models.readthedocs.io/en/latest/models.html#websky).
For convenience, here are the [cosmological parameters assumed in WebSky](https://mocks.cita.utoronto.ca/data/websky/v0.0/cosmology.py).

All the models listed above will be part of PySM 3 once we upgrade them to nside 8192 and merge them in.

I also created a version of the lensed CMB realization with the dipole component replaced by the [HFI 2018 solar dipole](https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Map-making#HFI_2018_Solar_dipole)

## Available maps

HEALPix maps at high resolution for LAT (nside 4096) and low resolution for SAT (nside 512), these models are deterministic, so we have
a set for each resolution for all channels. All maps are full-sky.

Reference frame for the maps is **Equatorial**, pixel ordering is NESTED.
The `ell_max` for the harmonics transform is `3*Nside-1`.

**Location at NERSC**:

    /global/cfs/cdirs/cmbs4/dm/dstool_202102/input_pysm/

The naming convention is:

    {nside}/{content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"

where:

* `content` is `[dust, synchtrotron, freefree, ame]` for galactic components and `[ksz, tsz, cib]` for extragalactic components
* `content` for the available CMB is `[cmb, cmb_unlensed]`
*  CIB map for LFL1 and LFS1 are missing
* `num` is `0`
* `telescope` is `SAT` or `LAT`
* `band` is the channel band

Only exception are the CMB Solar Dipole maps:

    output/{nside}/cmbs4_cmb_solar_dipole_uKCMB_nside{nside}.fits

## Combined maps, inputs for the Design Tool

Also created a single set of maps which is the sum of all components. They are in NEST ordering (default for TOAST).

* `combined_foregrounds`: sum of `dust`, `synchrotron`, `freefree`, `ame`, `cib`, `ksz`, `tsz`
* `cmb_lensing_signal`: `cmb` minus `cmb_unlensed`
* `cmb_unlensed_solardipole`: `cmb_unlensed` with dipole removed, plus the Planck HFI 2018 solar dipole map
* `cmb_tensor`

They are in the same folder and same naming convention, e.g.:

    /global/cfs/cdirs/cmbs4/dm/dstool_202102/input_pysm/512/combined_foregrounds/0000/cmbs4_combined_foregrounds_uKCMB_SAT-LFS1_nside512_0000.fits

## Plots and verification

Make sure to check the "Known issues" section below.

Comparison of all the channels with on-the-fly PySM simulations ran without the pipeline, just at the center frequency of the lower and higher frequency channel.

### SAT

Plots are interactive, first click on the "Click here to toggle on/off the raw code" buttone, then click on the legend to select channel, double-click on plot to reset, zoom with scrolling.

* [Plot TT SAT](https://nbviewer.jupyter.org/gist/zonca/38e85587e02d5741425387f7ba2c8034)
* [Plot EE SAT](https://nbviewer.jupyter.org/gist/zonca/14873cd787be0d84b023e774b3269301)
* [Plot BB SAT](https://nbviewer.jupyter.org/gist/zonca/1381e3c785f5bd47d3b5152ff1806e32)

### LAT

* [Plot TT LAT](https://nbviewer.jupyter.org/gist/zonca/7c93b466fc247277edbbdf3308863ada)
* [Plot EE LAT](https://nbviewer.jupyter.org/gist/zonca/8c5faf168972950bbfdb78eae2768626)
* [Plot BB LAT](https://nbviewer.jupyter.org/gist/zonca/981e6bf2b698f83eee691025380db656)


## External analysis


## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `s4mapbasedsims` repo](https://github.com/CMB-S4/s4mapbasedsims/issues)

### Known issues


## Software

* PySM 3 is available at <https://github.com/healpy/pysm>
* `so_pysm_models` version 2.4.0
* `mapsims` version 2.4.0
