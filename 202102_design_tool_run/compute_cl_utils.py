import healpy as hp
import numpy as np

def build_pol_weights(wcov_filename):
    """Build inverse variance weights for polarization from covariance matrices"""
    wcov = hp.ma(hp.read_map(wcov_filename, (3, 4, 5)))
    pol_weights = 2/(wcov[0] + wcov[2] + 2*wcov[1])
    pol_weights = pol_weights.filled(0)
    assert np.all(np.isfinite(pol_weights))
    pixarea = hp.nside2pixarea(hp.npix2nside(wcov.shape[1]))
    noise_cl = np.average(wcov, weights=pol_weights**2, axis=0) * pixarea
    return pol_weights, noise_cl
