# Simulation verification

## CO Lines

[Verify CO Lines notebook](verify_CO.ipynb)

# Visual inspection of maps

Plot of all combined components (Mollview and Gnomview) in histogram-equalized colorscale to identify artifacts like pixelization issues, missing pixels or ringing.

* [`combined_cmb_lensing_signal`](https://nbviewer.org/gist/zonca/0088dfd2738f361d70e1ac6a8d1f7b69)
* [`combined_foregrounds_lowcomplexity_norg`](https://nbviewer.org/gist/zonca/737627175bb1fb60c0ff559e20631326)
* [`combined_cmb_unlensed_dipole`](https://nbviewer.org/gist/zonca/06afa3cf2cb7783306ba14a9a44945ad)
* [`combined_foregrounds_mediumcomplexity_norg`](https://nbviewer.org/gist/zonca/c0e9f919e575a2bc8c0f2c0cbd97d4ee)
* [`combined_foregrounds_highcomplexity_norg`](https://nbviewer.org/gist/zonca/24398799ef878b8653a1ffd1071a3a8c)

## Power spectra

All components except CO and Radio Galaxies,
the B Spectra of the CMB components are affected by high noise due to `ud_grade` performed in the on-the-fly run with PySM inside the notebook.
If the run is properly executed at Nside 4096, no artificial noise is visible anymore.

* [SAT T](https://nbviewer.org/gist/zonca/a6fa37a987ee8d86f54fe3fccb973ada)
* [SAT E](https://nbviewer.org/gist/zonca/88d61cb95b9fe54e9e788170ed2413af)
* [SAT B](https://nbviewer.org/gist/zonca/ee29498ec7ac1941443c29c84159eb27)
