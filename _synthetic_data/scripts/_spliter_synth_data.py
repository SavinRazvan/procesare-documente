#!/usr/bin/env python3
"""
Spliter Synthetic Data Generator
===============================

Generates synthetic spliter data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: TIP_SPLITER, NR_SPLITERE
- Uses deterministic generation based on salt for consistency
- Compatible with current spliter processor field structure

Input:
  - _synthetic_data/data/_synth_input/spliter_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/spliter_centralized.geojson

Synthetic Fields Generated:
  - TIP_SPLITER: Realistic splitter types (2, 4, 6, 8, 12)
  - NR_SPLITERE: Random values 1-5
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    stable_choice,
    stable_randint,
    load_geojson,
    save_geojson_single_line,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "spliter_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "spliter_centralized.geojson")


TIP_SPLITER_OPTIONS: List[str] = ["2", "4", "6", "8", "12"]


def main() -> None:
    salt = get_salt()
    
    # Try to load existing spliter data
    try:
        fc = load_geojson(SRC_PATH)
        features_in = fc.get("features", [])
        print(f"📁 Loaded {len(features_in)} features from {os.path.basename(SRC_PATH)}")
    except Exception:
        print(f"❌ Could not load input file {SRC_PATH}")
        return

    if not features_in:
        print("❌ No features found in input file")
        return

    features_out: List[Dict[str, Any]] = []

    for idx, feat in enumerate(features_in, start=1):
        props_in: Dict[str, Any] = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry
        
        seed_base = f"{salt}:{idx}"

        # TIP_SPLITER - ALWAYS generate synthetic
        tip_spliter = stable_choice(seed_base + ":tip_spliter", TIP_SPLITER_OPTIONS)
        print(f"🔧 Generated TIP_SPLITER: {tip_spliter} for feature {idx}")

        # NR_SPLITERE - ALWAYS generate synthetic (1-5 range)
        nr_splitere = str(stable_randint(1, 5, seed_base + ":nr_splitere"))
        print(f"🔧 Generated NR_SPLITERE: {nr_splitere} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["TIP_SPLITER"] = tip_spliter    # Generated synthetic
        props_out["NR_SPLITERE"] = nr_splitere    # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": geometry,  # Preserve original geometry
            }
        )

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Spliter Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} spliter features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 TIP_SPLITER, NR_SPLITERE generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


