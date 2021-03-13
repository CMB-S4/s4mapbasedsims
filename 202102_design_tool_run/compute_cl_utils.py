import healpy as hp
import numpy as np


def build_inverse_cov_weights(wcov_filename):
    """Build inverse variance weights for polarization from covariance matrices"""
    wcov = hp.read_map(wcov_filename, (0, 3, 4, 5))
    wcov[wcov == hp.UNSEEN] = np.nan
    pol_weights = 2 / (wcov[1] + wcov[3] + 2 * wcov[2])
    temp_weights = (1 / wcov[0])
    pol_weights[np.isnan(pol_weights)] = 0
    temp_weights[np.isnan(temp_weights)] = 0
    pol_weights[np.isinf(pol_weights)] = 0
    temp_weights[np.isinf(temp_weights)] = 0
    assert np.all(np.isfinite(pol_weights))
    assert np.all(np.isfinite(temp_weights))
    wcov[np.isnan(wcov)] = 0
    pixarea = hp.nside2pixarea(hp.npix2nside(wcov.shape[1]))
    noise_cl = np.average(wcov, weights=pol_weights ** 2, axis=1) * pixarea
    noise_cl[0] = np.average(wcov[0], weights=temp_weights ** 2) * pixarea
    return temp_weights, pol_weights, noise_cl
