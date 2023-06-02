Sky simulations for Data Challenge 0
====================================

## Updates

* 2023-06-02: Executed maps
* 2023-05-19: Exported instrument model from `s4sim` tag `e20d9ab`

## Summary

Full sky simulations for all CMB-S4 frequency channels for LAT deployed in Chile (CHLAT), SAT deployed at South Pole (SPLAT) and SAT of Galactic/Extragalactic foregrounds and CMB. The dataset includes Galactic foreground models at 3 different levels of complexity.
The instrument model assumes Gaussian beams and top-hat bandpasses.

## Instrument model

The instrument model has been extracted from `s4sim`,
see the [notebook script for more details](utils/create_s4_instrument_parameters.ipynb), the instrument parameters have been extracted to
[text files in IPAC table format](instrument_model/cmbs4_instrument_model.tbl), which supports units for the columns and can be read as `astropy.QTable`.

```python
from astropy import QTable
s4 = QTable.read("instrument_model/cmbs4_instrument_model.tbl", format="ascii.ipac" )
s4.add_index("band")
```

Example on how to access all parameters for a band, or a specific one:

```python
s4.loc["SAT_f030"]
s4.loc["SAT_f030"]["fwhm"]
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

Maps are available in HEALPix pixelization. The resolution of the maps is Nside 4096 for LAT and Nside 512 for SAT.

Maps are in Equatorial Coordinates, `uK_CMB` units, FITS format.
See [`common.toml`](common.toml) for the naming convention.

Each of the 17 components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

**Location at NERSC**, this is a temporary folder:

    /global/cscratch1/sd/zonca/cmbs4/map_based_simulations/202305_dc0

## Metadata

Most useful metadata is available in the FITS header of the HEALPix maps, for example:

```
PIXTYPE = 'HEALPIX '           / HEALPIX pixelisation                           
ORDERING= 'NESTED  '           / Pixel ordering scheme, either RING or NESTED   
COORDSYS= 'C       '           / Ecliptic, Galactic or Celestial (equatorial)   
EXTNAME = 'xtension'           / name of this binary table extension            
NSIDE   =                 4096 / Resolution parameter of HEALPIX                
TELESCOP= 'LAT     '                                                            
BAND    = 'CHLAT_f030'                                                          
TAG     = 'dust_d10'                                                            
ELL_MAX =                10240                                                  
```

## Model execution

Simulations were run using `mapsims 2.6.0` to coordinate the execution of `PySM 3.4.0b8`.
Given that each channel requested a different resolution, we have followed some guidelines, agreed with the Panexperiment Galactic science group:

* We have 2 resolution parameters, the output Nside is the requested resolution of the output map as defined in the instrument model. The modeling Nside instead is the resolution used to run PySM, then the output of PySM is transformed to Alm, beam-smoothed, rotated to Equatorial and anti-transformed to the output Nside. No `ud_grade` operations are ever performed.
* Evaluation of the PySM 3 models is executed at a minimum Nside 2048 or at the higher resolution available in the model. For example PySM 2 native models are executed at Nside 512, the new PySM 3 models are executed at 2048 even if we only want a Nside 128 output.
* Evaluation is executed at 2 times the requested output Nside, unless the requested output Nside is already the maximum available. For example if we request output at Nside 2048, `d10` is executed at 4096, if we request Nside 8192, `d10` is also executed at 8192.
* The maximum Ell is set to 2.5 times the lowest between the modeling and the output Nside, to avoid artifacts in the Spherical Harmonics transforms. Harmonics transforms are executed with [`hp.map2alm_lsq`](https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.map2alm_lsq.html) with 10 maximum iterations and 1e-7 target accuracy.

See [this comment for a dump from the log files of the Nside and ellMax of each run](https://github.com/CMB-S4/s4mapbasedsims/pull/27#issuecomment-1573874629), ellmax is also saved in the FITS headers.

## Verification

See [the README in the verification folder](verification/README.md)

## Known issues

* Websky Radio sources are available only down to 18.7 GHz, the lowest channels have bandpasses to 10 Ghz, so I created a copy of 18.7 GHz and renamed it to 1.0 GHz. This is the border of the band, should not matter much.
* Websky Radio galaxies have a few sources which have fluxes which are much brigther than in Planck maps, this is due to having a statistical realization without a cut. These sources will need masking, we plan to provide a suitable mask as part of the release. See [the relevant issue](https://github.com/CMB-S4/s4mapbasedsims/issues/23)

### Issues under investigation

* [Spikes in Synchrotron at high ell](https://github.com/CMB-S4/s4mapbasedsims/issues/29)
* [Drop at ell=2000 in `d10`](https://github.com/CMB-S4/s4mapbasedsims/issues/28)

## Feedback

If anything looks even just suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/CMB-S4/s4mapbasedsims/issues/new) and attach a Notebook to easily reproduce the problem.
