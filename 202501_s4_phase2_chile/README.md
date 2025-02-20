Sky simulations for CMB-S4 Chile-only simulations Phase 2
=========================================================

## Updates

* 2025-01-22: Ran verification
* 2025-01-17: Exported instrument model, executed maps, made available at NERSC

## Summary

Full sky simulations for SAT only deployed in Chile of Galactic/Extragalactic foregrounds and CMB.
These simulations have the same configuration of the [Phase 1 simulations](https://github.com/CMB-S4/s4mapbasedsims/tree/main/202410_s4_phase1_chile), so please refer to that simulation for LAT maps.
The need for this new round of simulations was triggered by having updated beams and new non-split bands `f090` and `f150`.

The dataset includes Galactic foreground models at 3 different levels of complexity.

The instrument model assumes Gaussian beams and top-hat bandpasses.
Top-hat bandpasses in CMB-S4 are assumed to be **flat in RJ units [uK_RJ]**, which means that they are proportional to $\nu^(-2)$ in the power units used by PySM, see [this post on Confluence (restricted)](https://cmb-s4.atlassian.net/wiki/spaces/XC/pages/1318518785/Bandpass+Convention+-+What+does+flat+mean). Notice that the [DC-0 simulations](https://github.com/CMB-S4/s4mapbasedsims/tree/main/202305_dc0) instead use bandpasses that are flat in power units, similarly to previous Simons Observatory and Litebird simulations.

## Instrument model

The instrument model has been extracted from a TOML instrument model generated by `s4sim`,
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

* `cib1,ksz1,tsz1`
* `c3`: CMB with same Cosmological parameters used in Websky unlensed
* `c4`: Same as `c3` but lensed by Websky
* **TODO**: Radio galaxies are not included yet, the new Catalog-based component still shows some issues, it will be released in the next weeks, the plan is to have 2 components, `rg2` for the sources > 1mJy generated on-the-fly directly at the target beam and resolution and `rg3`, interpolation-based componet for the fainter sources generated at a fiducial beam and differentially smoothed to the target beam.

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

Each of the 16 components is available separately, see the TOML files in this repository for the configuration used to run PySM for each component.

**Location at NERSC**, on project space:

`/global/cfs/cdirs/cmbs4/chile_optimization/simulations/phase2/input_sky`

## Combined maps

Also created a single set of maps to be used as input to the DC-0 simulations, available in the same folder.

* `combined_cmb_unlensed_dipole`: Unlensed CMB with Planck HFI 2018 dipole
* `combined_cmb_lensing_signal`: `cmb` lensed map - `cmb_unlensed` map
* `combined_foregrounds_mediumcomplexity_norg`: all Galactic and Extragalactic foregrounds, including SZ, excluding Radio Galaxies, as requested by the analysis team, due to the some Radio Galaxies in the Websky catalog being too bright and creating un-physical issues in the analysis.

we also have the same foreground maps for the other models, not used in DC-0:

* `combined_foregrounds_lowcomplexity_norg`
* `combined_foregrounds_highcomplexity_norg`

See [`combine_maps.py`](./combine_maps.py) for details.

They are in the same folder and same naming convention.

## Metadata

Most useful metadata is available in the FITS header of the HEALPix maps.

## Model execution

Simulations were run using `mapsims 2.7.0a1` to coordinate the execution of `PySM 3.4.1a1`.
Given that each channel requested a different resolution, we have followed some guidelines, agreed with the Panexperiment Galactic science group:

* We have 2 resolution parameters, the output Nside is the requested resolution of the output map as defined in the instrument model. The modeling Nside instead is the resolution used to run PySM, then the output of PySM is transformed to Alm, beam-smoothed, rotated to Equatorial and anti-transformed to the output Nside. No `ud_grade` operations are ever performed.
* Evaluation of the PySM 3 models is executed at a minimum Nside 2048 or at the higher resolution available in the model. For example PySM 2 native models are executed at Nside 512, the new PySM 3 models are executed at 2048 even if we only want a Nside 128 output. This caused ringing in the CHLAT foreground maps, it was due to [artifacts in `f1`](https://github.com/galsci/pysm/issues/197) so now we execute PySM 2 models, with a max nside of 512, either at 512 or at 4096 with `ud_grade` to avoid ringing.
* Evaluation is executed at 2 times the requested output Nside, unless the requested output Nside is already the maximum available. For example if we request output at Nside 2048, `d10` is executed at 4096, if we request Nside 8192, `d10` is also executed at 8192.
* The maximum Ell is set to 2.5 times the lowest between the modeling and the output Nside, to avoid artifacts in the Spherical Harmonics transforms. Harmonics transforms are executed with [`hp.map2alm_lsq`](https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.map2alm_lsq.html) with 10 maximum iterations and 1e-7 target accuracy.

## Verification

See [the README in the verification folder](verification/README.md)

## Known issues

* [Spikes in Synchrotron at high ell](https://github.com/CMB-S4/s4mapbasedsims/issues/29) if Galaxy is not masked. This should not affect much analysis, the galactic plane is always masked.
* See the notice in the Summary about the meaning of top-hat bandpasses

## Feedback

If anything looks even just suspicious in the simulations, please do not hesitate to [open an issue here](https://github.com/CMB-S4/s4mapbasedsims/issues/new) and attach a Notebook to easily reproduce the problem.
