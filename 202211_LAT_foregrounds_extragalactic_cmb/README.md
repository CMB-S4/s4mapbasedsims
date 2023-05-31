Foregrounds and CMB for CMB-S4
==============================

## Updates

* 5 April 2023: discovered bug in solar dipole removal from `cmb_unlensed_solardipole` leaving relativistic quadrupole in the map, this affects all the previously created combined maps, see #22, created a new component named `cmb_unlensed` and used it to created new combined maps. Still using PySM 3.4.0b7.
* 25 February 2023: all `synchrotron` and all combined maps regenerated with PySM 3.4.0b7
* 17 February 2023: `dust_low`, `dust`, all `synchrotron` and all combined maps regenerated with PySM 3.4.0b6
* 3 December 2022: `dust_high`, `radio` and all combined maps regenerated with PySM 3.4.0b5
* 21 November 2022: first release

## Instrument properties

See the documentation of the [`202102_design_tool_run`](https://github.com/CMB-S4/s4mapbasedsims/tree/master/202102_design_tool_run)

## Input components

Each component is saved separately, all maps are in `uK_CMB`, IQU or I, single precision (`float32`)

For this simulation with have 3 versions of the Galactic foregrounds which have been recommended [by the Pan Experiment Galactic Science group to be used by all CMB experiments](https://galsci.github.io/blog/2022/common-fiducial-sky/)

The CMB, CIB, KSZ, TSZ and radio-galaxies models are created from the new 0.4 version of the WebSky cosmological simulations, [see the recommended models by the Panexp group](https://galsci.github.io/blog/2022/common-fiducial-extragalactic-cmb)
For CMB, we both have unlensed and lensed CMB.

We needed also to have a CMB solar dipole, so I created a map for the [HFI 2018 solar dipole](https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Map-making#HFI_2018_Solar_dipole) and added it to the unlensed CMB component.

## Processing

The simulations are executed by the `mapsims` package version 2.5.0 using the TOML configuration files available on Github.
In order to avoid issues in the spectra, no `hp.ud_grade` operations are performed, each model is executed at its native resolution, which is 512 for the PySM 2 based models, like `f1` and 4096 for all the new models and for the extragalactic and CMB component, then the maps are rotated to Equatorial coordinates in Spherical Harmonics domain and transformed back to the target resolution.

## Processing

The simulations are executed by the `mapsims` package version 2.5.0 using the TOML configuration files available on Github.
In order to avoid issues in the spectra, no `hp.ud_grade` operations are performed, each model is executed at its native resolution (referred as "modeling nside" in the code), which is 512 for the PySM 2 based models, like `f1` and 4096 for all the new models and for the extragalactic and CMB component, then the maps are rotated to Equatorial coordinates and beam-smoothed in Spherical Harmonics domain (using `map2alm_lsq` with 10 iterations max) and transformed back to the target resolution. The ell max of the transforms is 2.5 times the modeling Nside and it is saved in the metadata of the output FITS maps.

## Available maps

HEALPix maps at high resolution for LAT (nside 4096) and low resolution for SAT (nside 512), these models are deterministic, so we have a set for each resolution for all channels. All maps are full-sky.

Reference frame for the maps is **Equatorial**, pixel ordering is NESTED.
The `ell_max` for the harmonics transform is `2.5*Nside`.
I tried to be exhaustive in saving all metadata in the FITS headers.

**Location at NERSC**, notice they are now in the `raw/` subfolder:

    /global/cfs/cdirs/cmbs4/dc/dc0/sky/4096/raw/

The naming convention is:

    {content}/{num:04d}/cmbs4_{content}_uKCMB_{telescope}-{band}_nside{nside}_{num:04d}.fits"

where:

* `content` is `[dust, synchtrotron, freefree, ame, co]` for galactic components and `[ksz, tsz, cib, radio]` for extragalactic components
* `content` for the available CMB is `[cmb, cmb_unlensed]`, the CMB maps have no solar dipole
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

    cmbs4_cmb_solar_dipole_uKCMB_nside{nside}.fits

If you are not sure what component was used, you can check the `toml` configuration files inside this repository.

## Combined maps

Also created a single set of maps to be used as input to the DC-0 simulations, available at:

    /global/cfs/cdirs/cmbs4/dc/dc0/sky/

* `combined_cmb_unlensed_dipole`: Unlensed CMB with Planck HFI 2018 dipole
* `combined_cmb_lensing_signal`: `cmb` lensed map - `cmb_unlensed` map
* `combined_foregrounds_mediumcomplexity`: all Galactic and Extragalactic foregrounds, including SZ

we also have the same foreground maps for the other models, not used in DC-0:

* `combined_foregrounds_lowcomplexity`
* `combined_foregrounds_highcomplexity`

See [`combine_maps.py`](./combine_maps.py) for details.

They are in the same folder and same naming convention, e.g.:

    /global/cfs/cdirs/cmbs4/dc/dc0/sky/4096/combined_foregrounds_lowcomplexity/0000/cmbs4_combined_foregrounds_lowcomplexity_uKCMB_LAT-MFL2_nside4096_0000.fits

## Plots and verification

In progress

### SAT

### LAT

## External analysis

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `s4mapbasedsims` repo](https://github.com/CMB-S4/s4mapbasedsims/issues)

### Known issues

* The first release of this simulation used PySM `3.4.0b4` which was missing color correction in the `d12` maps, so affecting only the high-complexity model. It also had no radio galaxies, which were not validated yet. The maps produced in that first run are available in the `obsolete/` subfolder.
