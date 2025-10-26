#!/usr/bin/env python3
"""
Stalpi Synthetic Data Generator
==============================

Generates synthetic stalpi data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: FOLOSIT_RDS, MATERIAL_CONSTRUCTIV, TIP_STALP
- Sets LOCALITATE to "UNKNOWN" if empty, otherwise preserves original
- Uses deterministic generation based on salt for consistency
- Compatible with current stalpi processor field structure

Input:
  - _synthetic_data/data/_synth_input/stalpi_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/stalpi_centralized.geojson

Synthetic Fields Generated:
  - FOLOSIT_RDS: DA/NU (deterministic choice)
  - MATERIAL_CONSTRUCTIV: Beton (80%), Metal (15%), Lemn (5%) - weighted choice
  - TIP_STALP: retea JT, retea MT, iluminat public, telecomunicatii
  - LOCALITATE: Set to "UNKNOWN" if empty, otherwise preserved
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    load_geojson,
    save_geojson_single_line,
    stable_choice,
    stable_weighted_choice,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "stalpi_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "stalpi_centralized.geojson")


MATERIAL_OPTIONS = [("Beton", 80), ("Metal", 15), ("Lemn", 5)]
TIP_STALP_VALUES = [
    "retea JT",
    "retea MT",
    "iluminat public",
    "telecomunicatii",
]


def main() -> None:
    salt = get_salt()
    
    # Try to load existing stalpi data
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
        
        # LOCALITATE - preserve original if not empty, otherwise set to UNKNOWN
        localitate_raw = props_in.get("LOCALITATE", "")
        if localitate_raw and str(localitate_raw).strip():
            localitate = str(localitate_raw).strip()
            print(f"🔧 Preserved LOCALITATE: {localitate} for feature {idx}")
        else:
            localitate = "UNKNOWN"
            print(f"🔧 Set LOCALITATE to UNKNOWN for feature {idx}")

        seed_base = f"{salt}:{idx}"

        # FOLOSIT_RDS - ALWAYS generate synthetic
        folosit_rds = stable_choice(seed_base + ":rds", ["DA", "NU"])
        print(f"🔧 Generated FOLOSIT_RDS: {folosit_rds} for feature {idx}")

        # MATERIAL_CONSTRUCTIV - ALWAYS generate synthetic
        material = stable_weighted_choice(seed_base + ":mat", MATERIAL_OPTIONS)
        print(f"🔧 Generated MATERIAL_CONSTRUCTIV: {material} for feature {idx}")

        # TIP_STALP - ALWAYS generate synthetic
        tip_stalp = stable_choice(seed_base + ":tip", TIP_STALP_VALUES)
        print(f"🔧 Generated TIP_STALP: {tip_stalp} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["LOCALITATE"] = localitate        # Preserved or set to UNKNOWN
        props_out["FOLOSIT_RDS"] = folosit_rds     # Generated synthetic
        props_out["MATERIAL_CONSTRUCTIV"] = material # Generated synthetic
        props_out["TIP_STALP"] = tip_stalp          # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": geometry,  # Preserve original geometry
            }
        )

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Stalpi Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} stalpi features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 FOLOSIT_RDS, MATERIAL_CONSTRUCTIV, TIP_STALP generated for anonymization")
    print(f"🔧 LOCALITATE set to UNKNOWN if empty, otherwise preserved")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


