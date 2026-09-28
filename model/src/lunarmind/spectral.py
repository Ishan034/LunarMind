"""Small, transparent spectral utilities for exploratory M³ analysis.

Inputs use wavelengths in micrometres and reflectance on the product's documented scale.
These helpers do not replace the published Surkov et al. processing procedure.
"""

from __future__ import annotations

import numpy as np


def continuum_removed_depth(
    wavelength_um: np.ndarray,
    reflectance: np.ndarray,
    *,
    band_um: tuple[float, float] = (1.50, 1.62),
    shoulder_um: tuple[float, float] = (1.42, 1.72),
) -> float:
    """Return a simple minimum continuum-removed depth in the specified band.

    A straight line joins median reflectance in the two shoulder windows. The result is
    (continuum - reflectance) / continuum at the minimum within ``band_um``. This is a
    diagnostic feature only; validate windows and preprocessing for the selected product.
    """
    wavelength = np.asarray(wavelength_um, dtype=float)
    spectrum = np.asarray(reflectance, dtype=float)
    if wavelength.ndim != 1 or spectrum.ndim != 1 or wavelength.size != spectrum.size:
        raise ValueError("wavelength_um and reflectance must be matching one-dimensional arrays")
    if not np.all(np.diff(wavelength) > 0):
        raise ValueError("wavelength_um must be strictly increasing")

    left = (wavelength >= shoulder_um[0]) & (wavelength < band_um[0]) & np.isfinite(spectrum)
    right = (wavelength > band_um[1]) & (wavelength <= shoulder_um[1]) & np.isfinite(spectrum)
    band = (wavelength >= band_um[0]) & (wavelength <= band_um[1]) & np.isfinite(spectrum)
    if not left.any() or not right.any() or not band.any():
        return float("nan")

    left_wave, right_wave = np.median(wavelength[left]), np.median(wavelength[right])
    left_ref, right_ref = np.median(spectrum[left]), np.median(spectrum[right])
    if left_ref <= 0 or right_ref <= 0:
        return float("nan")

    continuum = left_ref + (right_ref - left_ref) * (
        (wavelength[band] - left_wave) / (right_wave - left_wave)
    )
    valid = continuum > 0
    if not valid.any():
        return float("nan")
    depths = 1.0 - spectrum[band][valid] / continuum[valid]
    return float(np.max(depths))


def spectral_slope(
    wavelength_um: np.ndarray,
    reflectance: np.ndarray,
    *,
    interval_um: tuple[float, float] = (1.0, 2.0),
) -> float:
    """Return a least-squares reflectance slope over a wavelength interval."""
    wavelength = np.asarray(wavelength_um, dtype=float)
    spectrum = np.asarray(reflectance, dtype=float)
    mask = (
        (wavelength >= interval_um[0])
        & (wavelength <= interval_um[1])
        & np.isfinite(wavelength)
        & np.isfinite(spectrum)
    )
    if mask.sum() < 2:
        return float("nan")
    return float(np.polyfit(wavelength[mask], spectrum[mask], deg=1)[0])
