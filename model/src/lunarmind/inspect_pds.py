"""Inspect a PDS label before selecting a reader for a mission product."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path

import pvl


def _walk(label: Mapping, prefix: str = "") -> list[tuple[str, object]]:
    rows: list[tuple[str, object]] = []
    for key, value in label.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, Mapping):
            rows.extend(_walk(value, name))
        elif str(key).upper() in {
            "PDS_VERSION_ID", "RECORD_TYPE", "RECORD_BYTES", "FILE_NAME",
            "^IMAGE", "^QUBE", "^SPECTRAL_QUBE",
            "LINES", "LINE_SAMPLES", "BANDS", "SAMPLE_TYPE", "SAMPLE_BITS",
            "BAND_STORAGE_TYPE", "CORE_ITEMS", "CORE_ITEM_TYPE", "CORE_ITEM_BYTES",
            "CORE_BASE", "CORE_MULTIPLIER", "AXIS_NAME", "CORE_NAME",
            "START_TIME", "STOP_TIME", "PRODUCT_ID", "PRODUCT_TYPE",
        }:
            rows.append((name, value))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize important metadata in a PDS label")
    parser.add_argument("label", type=Path, help="Path to a .lbl file")
    args = parser.parse_args()
    label = pvl.load(args.label)
    print(f"Label: {args.label.resolve()}")
    for key, value in _walk(label):
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
