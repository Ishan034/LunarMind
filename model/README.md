# LunarMind Ilmenite Model

Starter workspace for the first LunarMind resource-intelligence experiment: estimate relative/quantitative ilmenite abundance from Chandrayaan-1 M³ observations in the Mare Serenitatis–Mare Tranquillitatis study area.

## First milestone

Do not train a supervised model until a defensible abundance target and the exact M³ product format are confirmed. First reproduce and inspect the published spectral baseline around the ilmenite absorption near 1.55 µm, understand the M³ labels/quality masks, and make a small reproducible subset with plotted spectra and map coordinates.

The published 2020 study maps this same border region using the 1550 nm band and specifically addresses M³ strip noise. Its outputs are a scientific comparison/reference, not independent ground truth if they are derived from the same M³ observations. Keep those roles explicit in the data manifest.

## Project flow

1. Start from candidate product `M3G20090203T175131_V01_RFL`, which a recent regional M³ study uses for Serenitatis–Tranquillitatis; confirm its footprint and label before using it.
2. Record the precise ROI, M³ product IDs, source URLs, labels, observation geometry, and checksums in `data/manifest.csv`.
3. Inspect PDS labels and product layouts before choosing a reader. Do not assume all products share one file layout.
4. Plot quality-filtered spectra for representative pixels and reproduce an interpretable spectral parameter baseline.
5. Compare the baseline spatially with published ilmenite and TiO₂ products. Treat TiO₂ as a related but different quantity.
6. Only train regression models when target abundance is defined and its provenance is clear. If labels are published M³-derived estimates, describe the task as reproducing those estimates, not independent abundance discovery.
7. Evaluate on held-out contiguous geographic blocks; group overlapping acquisitions/scenes so the same ground footprint cannot leak between train and test. Hold out an acquisition/date as an additional robustness check only where comparable repeat coverage exists.
8. Emit an abundance estimate and a separately validated uncertainty interval/map.

## Technology choices

- **Python** for data inspection and scientific processing.
- **GitHub** as the source of truth for code, issues, and pull requests; keep raw/large planetary datasets out of Git.
- **Cursor/Codex** as coding assistants operating on branches; scientific assumptions and outputs still need teammate review.
- **GitHub Actions** for lightweight code-quality and reproducibility checks.
- **Vercel / Render** are deferred: they are for a later map UI and API/worker, not needed to build or validate the scientific model.

## Environment

Use Python 3.11 and install this package in editable mode with the `dev` extra. The project deliberately starts with a small scientific stack. Add a PDS reader only after confirming the concrete M³ product type and label structure.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

See [`docs/experiment-brief.md`](docs/experiment-brief.md) for target definition, validation, uncertainty, and modality sequencing.

## Data layout

Put downloaded data under `data/raw/` locally. It is ignored by Git. Keep `data/manifest.csv` and processing notes under version control. Never commit raw mission archives or derived rasters unless the team has explicitly chosen a suitable storage/versioning strategy.
