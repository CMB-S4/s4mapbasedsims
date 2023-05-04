Sky simulations for Data Challenge 0
====================================

## Updates

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
