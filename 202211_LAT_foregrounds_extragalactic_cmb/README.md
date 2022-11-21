Foregrounds and CMB for CMB-S4
==============================

Released on 21 November 2022 by @zonca

## Instrument properties

See the documentation of the [`202102_design_tool_run`](https://github.com/CMB-S4/s4mapbasedsims/tree/master/202102_design_tool_run)

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

For this simulation with have 3 versions of the Galactic foregrounds which have been recommended [by the Pan Experiment Galactic Science group to be used by all CMB experiments](https://galsci.github.io/blog/2022/common-fiducial-sky/)

The CIB, KSZ and TSZ models are created from the new 0.4 version of the WebSky cosmological simulations, [see the recommended models by the Panexp group](https://galsci.github.io/blog/2022/common-fiducial-extragalactic-cmb)

We needed also to have a CMB solar dipole, so I created a map for the [HFI 2018 solar dipole](https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Map-making#HFI_2018_Solar_dipole) and added it to the unlensed CMB component.

## Available maps

HEALPix maps at high resolution for LAT (nside 4096) and low resolution for SAT (nside 512), these models are deterministic, so we have a set for each resolution for all channels. All maps are full-sky.

Reference frame for the maps is **Equatorial**, pixel ordering is NESTED.
The `ell_max` for the harmonics transform is `2.5*Nside`.
I tried to be exhaustive in saving all metadata in the FITS headers.

**Location at NERSC**:

    /global/cfs/cdirs/cmbs4/dm/mbs/202211_LAT_fg_cmb

The naming convention is:

    {nside}/{content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"

where:

* `content` is `[dust, synchtrotron, freefree, ame, co]` for galactic components and `[ksz, tsz, cib]` for extragalactic components
* `content` for the available CMB is `[cmb, cmb_unlensed_solardipole]`, the unlensed CMB map includes a dipole generated in Equatorial reference frame, but for Websky we assumed a Galactic reference frame, so I removed this dipole when creating the combined maps.
* `num` is `0`
* `telescope` is `LAT`
* `band` is the channel band

The additional components needed for models at different complexity have `_low` or `_high` attached to them, for this release they are:

```
ame_high
co_low
dust_high
dust_low
synchrotron_high
synchrotron_low
```

Only exception is the CMB Solar Dipole map:

    {nside}/cmbs4_cmb_solar_dipole_uKCMB_nside{nside}.fits

If you are not sure what component was used, you can check the `toml` configuration files inside this repository.

## Combined maps

Also created a single set of maps which is the sum of all components for medium, high and low complexity of the Galactic components, while extragalactic and CMB are the same (we are using Unlensed CMB for time domain simulations):

* `combined_foregrounds_cmb_no_radio_fixdip`
* `combined_foregrounds_cmb_no_radio_fixdip_highcomplexity`
* `combined_foregrounds_cmb_no_radio_fixdip_lowcomplexity`

See [`combine_maps.py`](./combine_maps.py) for details.

They are in the same folder and same naming convention, e.g.:

    /global/cfs/cdirs/cmbs4/dm/mbs/202211_LAT_fg_cmb/4096/combined_foregrounds_cmb_no_radio_fixdip_lowcomplexity/0000/cmbs4_combined_foregrounds_cmb_no_radio_fixdip_lowcomplexity_uKCMB_LAT-MFL2_nside4096_0000.fits

## Plots and verification

In progress

### SAT

### LAT

## External analysis


## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `s4mapbasedsims` repo](https://github.com/CMB-S4/s4mapbasedsims/issues)

### Known issues


## Software

* PySM 3: `3.4.0b4`
* `mapsims` version 2.4.0
