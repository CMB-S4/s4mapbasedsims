Design tool run March 2021
==========================

Release:

* 13 April 2021, `s4_design_sim_tool` 1.1.1, reran all noise and atmosphere maps fixing the observation efficiency factors and the thinning factor impact on atmosphere polarization, see the `s4_design_sim_tool` [CHANGELOG](https://github.com/CMB-S4/s4_design_sim_tool/blob/master/CHANGELOG.md#release-111), first run maps saved at `/global/cscratch1/sd/zonca/cmbs4/map_based_simulations/firstrun_202102_design_tool_run`
* 24 March 2021, `s4_design_sim_tool` 1.1.0, added noise-only and atmosphere-only
* 15 March 2021, released LAT maps and their verification plots
* 10 March 2021, fixed noise+atmosphere SAT maps, added verification plots
* 5 March 2021, SAT maps

The simulation has been performed in 3 stages:

* First we created bandpass-integrated and beam smoothed full sky foreground and CMB maps with PySM 3. This is also available as a separate release at <https://github.com/CMB-S4/s4mapbasedsims/tree/master/202102_design_tool_input>, there you can find information about the foreground models used and the CMB parameters.
* Second we ran short time-domain simulations with TOAST (~10 days) to capture the effect of the observing strategy and filter-and-bin mapmaking, see [the simulation plan on Google doc](https://docs.google.com/document/d/1NGftWuvx6vIpdh_vg60xNUsCizLe-NpXupRKfZO0BZo/edit?usp=sharing) for more details. This consisted in 3 sky maps using the previous simulation as input (scalar CMB, tensor CMB and all other galactic/extra-galactic foregrounds), an atmosphere simulation and an instrumental noise simulation.
* Finally we ran the [CMB-S4 design simulation tool](https://github.com/CMB-S4/s4_design_sim_tool) to scale the TOAST outputs to the full experiment expected performance, 1 realization for the full mission and 7 yearly splits for noise and atmosphere, for a total of 4 different components (scalar CMB, tensor CMB, galactic/extra-galactic foregrounds and atmosphere/instrument noise)

# Instrument model

The instrument model has been extracted from `s4sim` on February, the 25th, 2021,
see the [notebook script for more details](utils/create_s4_instrument_parameters.ipynb), the instrument parameters have been extracted to
[text files in IPAC table format](instrument_model/cmbs4_instrument_model.tbl), which supports units for the columns and can be read as `astropy.QTable`.

```python
s4 = QTable.read("instrument_model/cmbs4_instrument_model.tbl", format="ascii.ipac" )
s4.add_index("band")
```

Example on how to access all parameters for a band, or a specific one:

```python
s4.loc["LFS1"]
s4.loc["LFS1"]["fwhm"]
```

# Instrument design

The design of the instrument (i.e. sites where telescopes are deployed, distribution of tubes in each telescope) follows the "Baseline design".
It is encoded in the [`s4_baseline_design.toml`](s4_baseline_design.toml) file in the repository.

# Verification

* [Mini-plots of all full experiment maps on the same scale](plot_maps/README.md)

## Plots of the maps

* [Comparison input and output foregrounds maps on same scale in gnomview/mollview](plot_gnomview/README.md)

## Noise + Atmosphere

Plots below are generated with a [`C_ell` computation script](compute_cl.py) and a [Plotting notebook](utils/verification_atmo_noise.ipynb). It uses the white noise covariance matrices to inverse-noise-weight the pixels before `anafast`.


* [Plots of spectra of noise + atmosphere, SAT pole](plots/SAT.md)
* [Plots of spectra of noise + atmosphere, 7-way splits, SAT pole](plots/SAT_7.md)
* [Plots of spectra of noise + atmosphere, LAT pole](plots/LAT_pole.md)
* [Plots of spectra of noise + atmosphere, LAT chile](plots/LAT_chile.md)
<!-- 
* [Plots of spectra of noise + atmosphere, SAT chile](plots/SAT_chile.md)
* [Plots of spectra of noise + atmosphere, 7-way splits, SAT chile](plots/SAT_chile_7.md)
* [Plots of hitmaps, SAT chile](plots/hitmap_SAT_chile.md)
-->


## CMB

Plots are interactive, first click on the "Click here to toggle on/off the raw code" buttone, then click on the legend to select channel, double-click on plot to reset, zoom with scrolling.
CMB maps power spectra was computed with the same `compute_cl.py` script, using inverse noise weighting, even if this maps have no noise.

* [SAT TT](https://nbviewer.jupyter.org/gist/zonca/2fabab2f0dddbb7cb1b4c1879d4ce774)
* [SAT EE](https://nbviewer.jupyter.org/gist/zonca/f6f8da5c9810c435d2606ea93ca05dee)
* [SAT BB](https://nbviewer.jupyter.org/gist/zonca/3146421a03ac7eec61c15d9e187e72d2)

For LAT instead, using inverse noise weighting was causing spurious features in the spectra (for example an excess in II for the 2 lowest frequecy channels at Pole in the ell range `300-500`). Therefore I switched to uniform weighting.

* [LAT TT](https://nbviewer.jupyter.org/gist/zonca/5dc1c8f7f2acd16fffb3f326298e9d83)
* [LAT EE](https://nbviewer.jupyter.org/gist/zonca/00a87a2bd6d23fe4e7b9c7ee01932577)
* [LAT BB](https://nbviewer.jupyter.org/gist/zonca/8663ab29235d4894eeee3da12b5d7125)

For reference here the plots with inverse noise weighting:

* [LAT TT](https://nbviewer.jupyter.org/gist/zonca/f933724d5be62daad75caa5e128e8814)
* [LAT EE](https://nbviewer.jupyter.org/gist/zonca/3c74dea8452e2f56fb3ce54d34355b25)
* [LAT BB](https://nbviewer.jupyter.org/gist/zonca/1c53b4ec4d84f9a752900aa7b47748bf)

## Hitmaps

* [Plots of hitmaps, LAT pole](plots/hitmap_LAT_pole.md)
* [Plots of hitmaps, LAT chile](plots/hitmap_LAT_chile.md)
* [Plots of hitmaps, SAT pole](plots/hitmap_SAT.md)


# Available maps

* `N_side` 512 for SAT, 4096 for LAT
* float32 precision
* `K_CMB` unit
* One map per band per site which combines all the telescopes at that band, atmosphere scales down as telescope-years, noise as detector-years
* Compared to the previous release, only base folder names (`s4_reference_design_foregrounds` -> `foregrounds`) and LAT channel labels changed

Metadata are available in the fits headers of extension 1, for example:

```
SOFTWARE= 's4_design_sim_tool'                                                  
SKY_VERS= '1.0     '                                                            
ATM_VERS= '1.0     '                                                            
NOI_VERS= '1.0     '                                                            
SITE    = 'Pole    '                                                            
SPLIT   =                    2                                                  
NSPLITS =                    7                                                  
CHANNEL = 'HFL1    '                                                            
DATE    = '2020-04-23'                                                          
CONFMD5 = '79858f71dbaf1c8bd9bd57a2cbea57ed'   
```

Space used:

```
30G     atmo/
30G     cmb_r0/
30G     cmb_tensor_only_r3e-3/
30G     foregrounds/
31G     noise/
491G    noise_atmo_7splits/
```

## Noise and atmosphere

1 full map based on 7 years of mission and 7 independent splits with equal sky coverage.

The configuration file for the design simulation tool is:

* [`noise_atmo_7splits.toml`](noise_atmo_7splits.toml)

Maps are available at NERSC at:

    /global/cscratch1/sd/zonca/cmbs4/map_based_simulations/202102_design_tool_run

Will be moved to project space later on and the path here updated

File naming convention:

    "{telescope}-{band}_{site}/cmbs4_KCMB_{telescope}-{band}_{site}_nside{nside}_{split}_of_{nsplits}.fits"

Where:
   
* `telescope` LAT or SAT
* `band` e.g. LFL2
* `site` pole or chile
* `split` and `nsplits` the current split (starts from 1) and the number of splits, so `1_of_1` is a full mission map, `3 of 7` is the 3rd year of observation on 7 yearly splits.

For example:

    LAT-LFL2_chile/cmbs4_KCMB_LAT-LFL2_chile_nside4096_1_of_1.fits
    LAT-LFL2_chile/cmbs4_KCMB_LAT-LFL2_chile_nside4096_3_of_7.fits

This dataset also includes hitmaps and white noise covariance matrices properly scaled for full mission and the splits,
for example:

    LAT-HFPL1_pole/cmbs4_hitmap_LAT-HFPL1_pole_nside4096_1_of_1.fits
    LAT-HFPL1_pole/cmbs4_hitmap_LAT-HFPL1_pole_nside4096_1_of_7.fits
    LAT-HFPL1_pole/cmbs4_wcov_LAT-HFPL1_pole_nside4096_1_of_1.fits
    LAT-HFPL1_pole/cmbs4_wcov_LAT-HFPL1_pole_nside4096_1_of_7.fits

The white noise matrices also encode pixels discarded during mapmaking and the effect of variable NET with elevation (also on declination for South Pole),
therefore differ at the 5% level with the white noise levels computed naively from the NET and the hitmaps.

For debugging and comparison purposes I also produces noise-only and atmosphere-only maps, without splits,
they are located in the `noise` and `atmo` subfolders, they have the same weighting and naming of the noise+atmosphere maps,
I haven't run any of the verification on those, please open issue if anything looks suspect.

The noise and atmosphere maps from TOAST used as input are currently located at:

    /global/cscratch1/sd/keskital/s4sim/reference_tool_round_2/out
    
### Observation matrix

Observation matrices for Pole SAT are available in the subfolder:

    noise_atmo_7splits/observation_matrix
    
See the [observation matrix post on the wiki](https://cmb-s4.uchicago.edu/wiki/index.php/Observation_matrix).

## CMB and foregrounds

CMB and foreground maps are generated applying the mapmaking step in map domain to the [full sky, bandpass-integrated and beam-convolved input map based simulations](https://github.com/CMB-S4/s4mapbasedsims/tree/master/202102_design_tool_input#input-components).
See their documentation for details about all the models used.
We have just 1 split, i.e. there is no weighting done for CMB and foregrounds.

We have 1 map per tube for each of 3 components (with link to TOML configuration file):

* [foregrounds (dust, free-free, synchrotron, ame, Websky CIB/tsz/ksz)](foregrounds.toml)
* [CMB scalar (Websky compatible cosmology, scalar modes and lensing with Websky potential)](cmb_r0.toml)
* [CMB tensor only (`r=3e-3`)](cmb_tensor_only_r3e-3.toml)

Maps are available at NERSC at:

    /global/cscratch1/sd/zonca/cmbs4/map_based_simulations/202102_design_tool_run

in the 3 subfolders:

* `foregrounds`
* `cmb_r0`
* `cmb_tensor_only_r3e-3`

File naming convention:

    "{telescope}-{band}_{site}/cmbs4_KCMB_{telescope}-{band}_{site}_nside{nside}_{split}_of_{nsplits}.fits"

Where:
   
* `telescope` LAT or SAT
* `band` e.g. LFL2
* `site` pole or chile
* `split` and `nsplits` the current split and the number of splits, so `1_of_1` is a full mission map

For example:

    foregrounds/LAT-LFL2_chile/cmbs4_KCMB_LAT-LFL2_chile_nside4096_1_of_1.fits

## Issues or feedback

In case of any problem with the maps or the documentation or request more/different runs, [open an issue on the `s4mapbasedsims` repo](https://github.com/CMB-S4/s4mapbasedsims/issues)

### Known issues
