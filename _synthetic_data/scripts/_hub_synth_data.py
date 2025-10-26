#!/usr/bin/env python3
"""
Hub Synthetic Data Generator
===========================

Generates synthetic hub data that preserves original fields and geometries,
while generating synthetic values only for empty COD_FTTB and AC fields.

Features:
- Preserves original COD_FTTB and AC if they exist and are not empty
- Generates synthetic COD_FTTB (HUB0001, HUB0002...) if original is empty
- Generates synthetic AC (1-24) if original is empty
- Uses deterministic generation based on salt for consistency
- Compatible with current hub processor field structure

Input:
  - _synthetic_data/data/_synth_input/hub_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/hub_centralized.geojson

Synthetic Fields Generated (only if original is empty):
  - COD_FTTB: HUB0001, HUB0002, HUB0003... (sequential counter)
  - AC: Realistic AC values (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24)

Note: Only generates synthetic values for fields that are empty in the input data.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

# Local utilities
from utils import (
    get_salt,
    stable_choice,
    load_geojson,
    save_geojson_single_line,
)


# Base directories
SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_HUB_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "hub_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "hub_centralized.geojson")


MOTIVE_VALUES = [
    "",
    "alimentare electrica indisponibila",
    "defect sursa 48V",
    "cablu deteriorat in camera tehnica",
    "temperatura peste limita in rack",
    "mentenanta programata",
]


def format_hub_id(seq: int) -> str:
    return f"HUB{seq:04d}"


def main() -> None:
    salt = get_salt()
    
    # Try to load existing hub data
    try:
        fc = load_geojson(SRC_HUB_PATH)
        features_in = fc.get("features", [])
        print(f"📁 Loaded {len(features_in)} features from {os.path.basename(SRC_HUB_PATH)}")
    except Exception:
        print(f"❌ Could not load input file {SRC_HUB_PATH}")
        return

    if not features_in:
        print("❌ No features found in input file")
        return

    features_out = []
    hub_seq = 1

    # AC options - realistic values
    ac_options = ["1", "2", "3", "4", "5", "6", "8", "10", "12", "16", "20", "24"]

    for idx, feat in enumerate(features_in, start=1):
        original_props = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry

        # COD_FTTB - preserve original if exists, otherwise generate synthetic
        cod_fttb_raw = original_props.get("COD_FTTB", "")
        if cod_fttb_raw and str(cod_fttb_raw).strip():
            cod_fttb = str(cod_fttb_raw).strip()
            print(f"🔧 Preserved COD_FTTB: {cod_fttb} for feature {idx}")
        else:
            cod_fttb = format_hub_id(hub_seq)
            hub_seq += 1
            print(f"🔧 Generated COD_FTTB: {cod_fttb} for feature {idx}")

        # AC - preserve original if exists, otherwise generate synthetic
        ac_raw = original_props.get("AC", "")
        if ac_raw and str(ac_raw).strip():
            ac = str(ac_raw).strip()
            print(f"🔧 Preserved AC: {ac} for feature {idx}")
        else:
            seed_ac = f"{salt}:{idx}:ac"
            ac = stable_choice(seed_ac, ac_options)
            print(f"🔧 Generated AC: {ac} for feature {idx}")

        # Build properties - preserve all original fields, only modify if empty
        props_out = {
            "COD_FTTB": cod_fttb,
            "AC": ac,
        }

        feature_obj = {
            "type": "Feature",
            "properties": props_out,
            "geometry": geometry,  # Preserve original geometry
        }

        features_out.append(feature_obj)

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Hub Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} hub features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 COD_FTTB, AC generated for anonymization (if original was empty)")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 Fields: {', '.join(['COD_FTTB', 'AC'])}")


if __name__ == "__main__":
    main()


