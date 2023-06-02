Sky simulations for Data Challenge 0
====================================

## Updates

2023-06-02: Executed maps
2023-05-19: Exported instrument model from `s4sim` tag `e20d9ab`

## Summary

Full sky simulations for all CMB-S4 frequency channels for LAT deployed in Chile (CHLAT), SAT deployed at South Pole (SPLAT) and SAT of Galactic and Extragalactic foregrounds and CMB. The dataset includes Galactic foreground models at 3 different levels of complexity.
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
