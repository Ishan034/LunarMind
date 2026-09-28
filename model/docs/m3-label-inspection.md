# M³ candidate product label inspection

Inspected on 2026-09-28 for `M3G20090203T175131_V01_RFL`.

## Product identity and shape

- PDS3 product in `CH1-ORB-L-M3-4-L2-REFLECTANCE-V1.0`.
- Global Mode, orbit 01054, acquired 2009-02-03 17:51:31–18:27:11 UTC.
- Main reflectance image: `M3G20090203T175131_V01_RFL.IMG`.
- Shape: 21,030 lines × 304 samples × 85 bands.
- `PC_REAL`, 32-bit floating point, line-interleaved (ENVI `bil`), little endian.
- PDS invalid constant: `-999.0`; reflectance is unitless and 1.0 represents 100% reflectance.
- Detached ENVI header lists 85 wavelength centers from 460.99 to 2976.20 nm. Its bad-band list marks bands 1 and 2 invalid; remaining 83 bands are marked valid.
- Band 49 is 1548.92 nm; band 50 is 1578.86 nm. Use the header wavelength vector, not nominal evenly spaced wavelengths.

## Processing and ancillary files

- The Level 2 label and ENVI header indicate I/F conversion, statistical polishing, thermal correction, photometric correction, and band masking were applied.
- Thermal and photometric correction flags are `Y`; ground-truth correction is `N/A` / not applied.
- The image contains reflectance, while the separate 3-band `*_SUP.IMG` contains 1489-nm photometrically corrected albedo, estimated temperature, and Level 1B radiance band 84. Do not treat the supplemental bands as part of the 85-band reflectance cube.
- The label identifies the source Level 1B product and names its radiance, observation-geometry (`*_OBS.IMG`), and pixel-location (`*_LOC.IMG`) files.
- This PDS label does not give the scene's latitude/longitude bounding box or per-pixel quality/geometry values. Confirm study-area coverage and screening masks from the location and observation products before clipping or modeling.

## Reader implications

Read the main cube as 32-bit float with shape `(lines=21030, bands=85, samples=304)` in BIL storage, or the equivalent library-specific ordering. Mask `-999.0` and bands whose ENVI `bbl` value is 0. Preserve the per-pixel quality mask separately from the per-band bad-band list. No reflectance integer scale factor is indicated for this `PC_REAL` image.

## Next inspection

1. Retrieve and inspect the matching Level 1B location and observation products/labels, and determine the exact footprint intersection with the chosen ROI.
2. Record geometry fields, fill values, and any applicable quality flags before defining pixel rejection rules.
3. Fetch the reflectance image only after storage needs and the scene footprint are confirmed; validate binary layout and wavelength alignment on a small sample.

## Source files

- [PDS label](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0004/DATA/20081118_20090214/200902/L2/M3G20090203T175131_V01_L2.LBL)
- [Detached ENVI header](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0004/DATA/20081118_20090214/200902/L2/M3G20090203T175131_V01_RFL.HDR)
- [NASA PDS Level 2 reflectance dataset profile](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=CH1-ORB-L-M3-4-L2-REFLECTANCE-V1.0)
