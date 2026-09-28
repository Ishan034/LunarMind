# Experiment brief: M³ ilmenite abundance

## Research question

For a fixed area on the Mare Serenitatis–Mare Tranquillitatis boundary, how well can quality-screened Chandrayaan-1 M³ spectra reproduce a defensible ilmenite abundance estimate, and does a carefully chosen contextual layer improve performance on geographically unseen terrain?

## Prediction target

The desired scientific output is ilmenite abundance (with units and scale copied from the reference product/method) plus a calibrated uncertainty interval. “Titanium detected” and “ilmenite abundance” are not interchangeable: Ti also occurs in other phases. Do not turn a TiO₂ map into ilmenite labels.

### Target decision gate

Before supervised learning, document exactly what y means:

- **Direct/independent reference:** measurements or a reference map whose provenance is independent of the M³ input used for prediction.
- **Published algorithm estimate:** valuable for reproducing/comparing a method, but not independent truth if it uses the same or overlapping M³ observations.
- **Pseudo-label:** may train a model to imitate an algorithm; report it as emulation, and do not claim validation against the pseudo-label proves physical accuracy.

The Surkov et al. (2020) study is the primary first baseline because it maps the same regional boundary using the M³ 1550 nm feature and discusses strip-noise suppression. Reproduce its preprocessing/parameterization from the paper before choosing an ML target.

## First experiment: M³ only

1. Start with candidate Level 2 global-mode product **M3G20090203T175131_V01_RFL**, cited by a 2026 regional M³ study of Mare Serenitatis–Mare Tranquillitatis. It is listed as a 140 m/pixel, 85-band scene. Confirm that its footprint fully covers the exact ROI and inspect the PDS label before processing; do not infer coverage from a filename alone.
2. Read its PDS label and confirm dimensions, band/wavelength table, units, scaling, projection/geolocation, quality flags, and missing-value conventions.
3. Screen low-quality/no-data pixels using product flags and geometry. Preserve the masks and rejection counts.
4. Plot spectra from 10–20 spatially distributed pixels and inspect the 1.3–1.7 µm region, overall albedo/slope, and artifacts. Check for strip patterns before smoothing; never smooth across masked gaps.
5. Implement and document the published spectral baseline. Compare outputs with the study’s regional map and related TiO₂ context layer without treating either as automatic ground truth.
6. Decide whether there is a scientifically defensible y for supervised regression. If not, report the reproduced physical/spectral mapping baseline and keep ML as a later phase.

## Model ladder, only after target approval

Use a transparent linear/ridge regression baseline, then Random Forest, then XGBoost if it adds value. Fit all scaling, feature selection, and calibration on training geography only. Keep a simple physical/spectral baseline in every comparison. A neural network is not justified for the first small regional experiment.

Potential M³ features should be chosen from the literature and instrument characteristics: calibrated reflectance bands; continuum-removed feature depth/shape near the ilmenite band; visible/NIR slope and albedo; relevant pyroxene band parameters; and quality/geometry covariates for screening or diagnostics. Do not blindly include all bands or observation metadata as predictors if that creates scene/date shortcuts.

## Spatial validation

Do not randomly split neighboring pixels. Define contiguous geographic blocks before fitting. Hold out one or more full blocks for evaluation; group overlapping strips/repeated observations of the same footprint together. Report the held-out block map and metrics per block. If there are comparable repeat observations, add a separate acquisition/date holdout as a robustness check; it does not replace geographic holdout. The transcript’s “three parts train, fourth unseen” is directionally sound, but block boundaries should follow coverage/geology and avoid leakage, not arbitrary pixel quadrants.

Report MAE, RMSE, bias, and R² only where the target scale supports them. Also inspect spatial residual maps, errors by block and data-quality regime, and baseline-versus-model differences.

## Uncertainty

Return prediction and uncertainty together. Separate measurement/quality uncertainty, model uncertainty, and reference-label uncertainty where possible. Start with spatially held-out residuals and a calibrated interval method (for example, block-aware conformal calibration); do not label raw Random Forest tree spread or generic confidence as a validated “uncertainty percentage.” Evaluate interval coverage and width on held-out spatial blocks.

## Modalities as controlled additions

1. M³ spectra only.
2. M³ plus a co-registered TiO₂ context layer as a distinct predictor (with clear provenance; guard against target leakage if the reference uses it).
3. M³ plus LOLA elevation-derived slope/roughness at a defensible common scale.
4. Add LROC only after selecting calibrated/georeferenced regional products; the linked LROC EDR entry is raw, uncalibrated NAC/WAC data and is not a ready-to-use morphology layer.
5. Add Diviner last. It measures thermal behavior, which is a weakly motivated predictor of composition for this first task; justify a physical hypothesis and handle documented product gaps before using it.

For each step, use identical spatial folds, evaluate whether held-out performance and uncertainty improve, and retain the simpler model if additional layers do not help. Keep resource accessibility/prospectivity as a later product built on validated abundance, terrain, and uncertainty—not the first model target.

## Team / delivery workflow

- GitHub: issues for the experiment gates, branches and pull requests for changes, data manifests and documentation committed, large raw data ignored.
- Cursor/Codex: assist with code and documentation on a branch; teammate reviews science and code.
- GitHub Actions: lightweight Ruff/lint and packaging checks on pull requests; add data-dependent workflows only when small and reproducible.
- Vercel and Render: no role in scientific training at this stage. Consider later for a map front end and an API/worker after there is a validated artifact to serve.

## Open decisions for the two-person team

- Exact ROI coordinates / M³ product(s) and projection.
- Whether the target is absolute abundance, a published map estimate, or a relative spectral index.
- Whether an independent reference raster/sample data can be obtained and aligned.
- Block definition and acceptable generalization claim.
- Which published procedure to reproduce, including filter/preprocessing parameters.
