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

## Matching Level 1B location and observation inspection

Inspected the matching source product `M3G20090203T175131_V03_RDN` and its detached location/observation headers. The location and observation files are ancillary to the Level 2 reflectance image and were downloaded locally for footprint/geometry checks; they are in the ignored `data/raw/m3/` directory and are not committed.

- `*_LOC.IMG`: 21,030 × 304 × 3, `PC_REAL` 64-bit, BIL, little endian. Bands are longitude, latitude, and radius. The header describes the frame as `MOON_ME`, longitude/latitude in decimal degrees, radius in metres.
- `*_OBS.IMG`: 21,030 × 304 × 10, `PC_REAL` 32-bit, BIL, little endian. Bands are Sun azimuth/zenith, instrument azimuth/zenith, phase, Sun path offset, instrument path length, facet slope/aspect, and facet cos(i). These are geometry fields, not a per-pixel quality bitmask.
- All 6,393,120 location triplets are finite, with positive radius; longitude spans 24.3986°–83.5400° east and latitude spans −19.3947°–89.0589° north. The file's SHA-256 is `74DB21E2911341C7B7BE3BA092B5669EF37122BF06A07BA2EB98972196E96DA7`.
- All 6,393,120 observation vectors are finite. Across the whole strip, solar zenith is 47.9653°–89.1864°, instrument zenith 0.4799°–12.7876°, phase 36.6883°–97.4062°, and facet cos(i) −0.4985–0.9718. The file's SHA-256 is `41E7D67D92C0FC023E3B281FFC171BCF75CBEF99BF06F6E33B594FD6BC921721`.
- A rough coverage check box (24°–32°E, 15°–30°N; provisional only, not the final ROI polygon) contains 885,622 pixels. Within that box, median solar zenith is 52.1°, instrument zenith 6.316°, phase 52.116°, and facet cos(i) 0.616. A pixel lies 2.74 km from the illustrative point (25°E, 20°N). This supports overlap with part of the broad Serenitatis–Tranquillitatis boundary region, but the team still needs to define an exact ROI.
- Using an approximate Apollo 17 coordinate (30.77°E, 20.19°N), the nearest pixel center is about 115.5 km away. Do not assume this candidate scene covers Apollo 17.
- The L1B label says orbit limb direction `DESCENDING`, while the L2 label says `ASCENDING`. Pixel coordinates run from about 89°N at the first line to −19°N at the last line, consistent with north-to-south coverage. Use the geolocation arrays rather than either orientation label to georeference the scene, and preserve this metadata discrepancy in notes.

No final geometry rejection thresholds have been selected. Use the actual ROI's geometry distributions and literature/reproducibility requirements to choose them; the geolocation/observation cubes contain no standalone binary quality mask. The reflectance cube's `-999.0` fill value and header bad-band list are separate masks.

## Reader implications

Read the main cube as 32-bit float with shape `(lines=21030, bands=85, samples=304)` in BIL storage, or the equivalent library-specific ordering. Mask `-999.0` and bands whose ENVI `bbl` value is 0. Preserve the per-pixel quality mask separately from the per-band bad-band list. No reflectance integer scale factor is indicated for this `PC_REAL` image.

## Next inspection

1. Retrieve and inspect the matching Level 1B location and observation products/labels, and determine the exact footprint intersection with the chosen ROI.
2. Record geometry fields, fill values, and any applicable quality flags before defining pixel rejection rules.
3. Fetch the reflectance image only after storage needs and the scene footprint are confirmed; validate binary layout and wavelength alignment on a small sample.

## Source files

- [PDS label](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0004/DATA/20081118_20090214/200902/L2/M3G20090203T175131_V01_L2.LBL)
- [Detached ENVI header](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0004/DATA/20081118_20090214/200902/L2/M3G20090203T175131_V01_RFL.HDR)
- [Matching L1B label](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0003/DATA/20081118_20090214/200902/L1B/M3G20090203T175131_V03_L1B.LBL)
- [Location ENVI header](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0003/DATA/20081118_20090214/200902/L1B/M3G20090203T175131_V03_LOC.HDR)
- [Observation geometry ENVI header](https://planetarydata.jpl.nasa.gov/img/data/m3/CH1M3_0003/DATA/20081118_20090214/200902/L1B/M3G20090203T175131_V03_OBS.HDR)
- [NASA PDS Level 2 reflectance dataset profile](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=CH1-ORB-L-M3-4-L2-REFLECTANCE-V1.0)
