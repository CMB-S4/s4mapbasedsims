# DC-0 sky signal simulation verification

## Power spectra

All components except CO and Radio Galaxies,
the B Spectra of the CMB components are affected by high noise due to `ud_grade` performed in the on-the-fly run with PySM inside the notebook.
If the run is properly executed at Nside 4096, no artificial noise is visible anymore.

* [SAT T](https://nbviewer.org/gist/zonca/8c56ea1ae49037efd6bb6f265905aef3)
* [SAT E](https://nbviewer.org/gist/zonca/0d91eb04cb37f768fc0f10b7919eebb7)
* [SAT B](https://nbviewer.org/gist/zonca/1ee1a23565987021e2e7cb5638f3b17d)
* [SPLAT T](https://nbviewer.org/gist/zonca/a389465a87bca21446d4a67696b95631)
* [SPLAT E](https://nbviewer.org/gist/zonca/87b026ef38ad63f999e3a4b5da341bdf)
* [SPLAT B](https://nbviewer.org/gist/zonca/269fa7c35a61615a2dbb6b352a0ebe56)
* [CHLAT T](https://nbviewer.org/gist/zonca/53fbb4a46f1683add9d5f67593e309b1)
* [CHLAT E](https://nbviewer.org/gist/zonca/f2a0c878a08b86bc4df985f071c64fd6)
* [CHLAT B](https://nbviewer.org/gist/zonca/b7919148feed4854c25d4aa63a1694f7)

### Obsolete power spectra

First release with missing power at high ell in `dust`

* [SAT T](https://nbviewer.org/gist/zonca/064437a8a988666a52288836e5a40fbb)
* [SAT E](https://nbviewer.org/gist/zonca/5a77d7e3d02de90f28327408034da02f)
* [SAT B](https://nbviewer.org/gist/zonca/5a81e11324d95407a5a34226851c8e3e)
* [CHLAT T](https://nbviewer.org/gist/zonca/2689131a2c458224f595b96a2f90387e)
* [CHLAT E](https://nbviewer.org/gist/zonca/0b86799c564d86fb817911c611a7af32)
* [CHLAT B](https://nbviewer.org/gist/zonca/8321f3315a59ce31148758d06714c544)
* [SPLAT T](https://nbviewer.org/gist/zonca/96f99de0963ae519d5487b16acb7f9f5)
* [SPLAT E](https://nbviewer.org/gist/zonca/cc28f8206efcba55884af518e2d7e0ea)
* [SPLAT B](https://nbviewer.org/gist/zonca/e651e69af46bf11cf049691573e74a1b)

## CO Lines

[Verify CO Lines notebook](verify_CO.ipynb)
