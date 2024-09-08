PySM Foreground and CMB simulations for South Pole Telescope
============================================================

## Updates

* 2024-09-07: Started map execution
* 2023-08-23: Created input instrument model

## Summary

Full sky simulations for all SPT-3G frequency channels of Galactic/Extragalactic foregrounds and CMB. The dataset includes Galactic foreground models at 3 different levels of complexity, the models have been selected by the Panexperiment Galactic Science group for common simulations across all CMB Experiments.

## Instrument model

The instrument model has been created from files provided by the SPT-3G team, full description of the instrument is available in the ["The Design and Integrated Performance of SPT-3G
" paper](https://arxiv.org/abs/2106.11202).
We used measured bandpasses and isotropic but realistic beams, i.e. we start from $`B_\ell`$ instead of a simple FWHM, beams were normalized on the maximum value.


See the [notebook script for more details](utils/create_instrument_parameters.ipynb), the instrument parameters have been extracted to
[text files in IPAC table format](../private/202308_panexp_spt3g/spt_instrument_model.tbl), which supports units for the columns and can be read as `astropy.QTable`.

```python
from astropy import QTable
imo = QTable.read("../private/202308_panexp_spt3g/spt_instrument_model.tbl", format="ascii.ipac" )
imo.add_index("band")
```

Example on how to access all parameters for a band, or a specific one:

```python
imo.loc["150ghz"]
imo.loc["150ghz"]["fwhm"]
```

## Sky model

This release is based on the [3 sets of recommended sky models by the Panexperiment Galactic science group](https://galsci.github.io/blog/2022/common-fiducial-sky/), in summary:

* Low complexity `d9,s4,f1,a1,co1`
* Medium complexity `d10,s5,f1,a1,co3`
* High complexity `d12,s7,f1,a2,co3`

and based on Websky for extragalactic and CMB:

* `cib1,ksz1,tsz1,rg1`, `rg` stands Radio Galaxies.
* `c3`: CMB with same Cosmological parameters used in Websky unlensed
* `c4`: Same as `c3` but lensed by Websky

Documentation reference:

* `d9` `d10` GNILC based models and `d12` MKD 3D layered dust model: https://pysm3.readthedocs.io/en/latest/models.html#dust
* Synchrotron models `s4` and `s5`: https://pysm3.readthedocs.io/en/latest/models.html#synchrotron
* CO: https://pysm3.readthedocs.io/en/latest/models.html#co-line-emission
* All other Galactic models are the same of PySM 2: https://pysm3.readthedocs.io/en/latest/models.html
* For Extragalactic and CMB see [the PySM 3 documentation about Websky](https://pysm3.readthedocs.io/en/latest/websky.html#websky)

## Available maps

Maps are available in HEALPix pixelization. The resolution of the maps is Nside 2048.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the 17 components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

**Location at NERSC**, this is a temporary folder:


## Combined maps

Also created a single set of combined maps:

* `combined_cmb_unlensed_dipole`: Unlensed CMB with Planck HFI 2018 dipole
* `combined_cmb_lensing_signal`: `cmb` lensed map - `cmb_unlensed` map
* `combined_foregrounds_mediumcomplexity`: all Galactic and Extragalactic foregrounds, including SZ
* `combined_foregrounds_lowcomplexity`
* `combined_foregrounds_highcomplexity`

See [`combine_maps.py`](./combine_maps.py) for details.

They are in the same folder and have the same naming convention.

## Metadata

Most useful metadata is available in the FITS header of the HEALPix maps, for example:

```
PIXTYPE = 'HEALPIX '           / HEALPIX pixelisation                           
ORDERING= 'NESTED  '           / Pixel ordering scheme, either RING or NESTED   
COORDSYS= 'C       '           / Ecliptic, Galactic or Celestial (equatorial)   
EXTNAME = 'xtension'           / name of this binary table extension            
NSIDE   =                 4096 / Resolution parameter of HEALPIX                
TELESCOP= 'x'                                                            
BAND    = 'x'                                                          
TAG     = 'dust_d10'                                                            
ELL_MAX = 'x'               
```

## Model execution

Simulations were run using `mapsims 2.6.0` to coordinate the execution of `PySM 3.4.0`.
Given that each channel requested a different resolution, we have followed some guidelines, agreed with the Panexperiment Galactic science group:

* We have 2 resolution parameters, the output Nside is the requested resolution of the output map as defined in the instrument model. The modeling Nside instead is the resolution used to run PySM, then the output of PySM is transformed to Alm, beam-smoothed, rotated to Equatorial and anti-transformed to the output Nside. No `ud_grade` operations are ever performed.
* Evaluation of the PySM 3 models is executed at a minimum Nside 2048 or at the higher resolution available in the model. For example PySM 2 native models are executed at Nside 512, the new PySM 3 models are executed at 2048 even if we only want a Nside 128 output.
* Evaluation is executed at 2 times the requested output Nside, unless the requested output Nside is already the maximum available. For example if we request output at Nside 2048, `d10` is executed at 4096, if we request Nside 8192, `d10` is also executed at 8192.
* The maximum Ell is set to 2.5 times the lowest between the modeling and the output Nside, to avoid artifacts in the Spherical Harmonics transforms. Harmonics transforms are executed with [`hp.map2alm_lsq`](https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.map2alm_lsq.html) with 10 maximum iterations and 1e-7 target accuracy.

See [this comment for a dump from the log files of the Nside and ellMax of each run](TODO), ellmax is also saved in the FITS headers.

## Known issues

* Websky Radio galaxies have a few sources which have fluxes which are much brigther than in Planck maps, this is due to having a statistical realization without a cut. These sources will need masking, we plan to provide a suitable mask as part of the release. See [the relevant issue](https://github.com/CMB-S4/s4mapbasedsims/issues/23)
* Websky Radio galaxies emission is not polarized, this is not realistic, see [the relevant issue in the PySM repository](https://github.com/galsci/pysm/issues/162)
* [Spikes in Synchrotron at high ell](https://github.com/CMB-S4/s4mapbasedsims/issues/29) if Galaxy is not masked. This should not affect much analysis, the galactic plane is always masked.

## Feedback

If anything looks even just suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/CMB-S4/s4mapbasedsims/issues/new) and attach a Notebook to easily reproduce the problem.
