#!/usr/bin/env python3
"""
Zona Acoperire Hub Synthetic Data Generator
==========================================

Generates synthetic zona acoperire hub data that preserves original NUME field,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Preserves original NUME field
- Generates synthetic values for: NR_CASE, NR_CASE_ACOPERIRE, NR_CASE_ACTIVE, NR_SCARI, NR_APT
- Uses deterministic generation based on salt for consistency
- Compatible with current zona acoperire hub processor field structure

Input:
  - _synthetic_data/data/_synth_input/zona_hub_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/zona_hub_centralized.geojson

Synthetic Fields Generated:
  - NR_CASE: Random values 100-5000
  - NR_CASE_ACOPERIRE: Random values 50-2000
  - NR_CASE_ACTIVE: Random values 50-1500
  - NR_SCARI: Random values 10-500
  - NR_APT: Random values 5-300

Preserved Fields:
  - NUME: Original zone name
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    load_geojson,
    save_geojson_single_line,
    stable_randint,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "zona_hub_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "zona_hub_centralized.geojson")


def _parse_int(value: Any) -> int:
    try:
        return int(float(str(value).replace(",", ".")))
    except Exception:
        return 0


def main() -> None:
    salt = get_salt()
    
    # Try to load existing zona acoperire hub data
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
        
        # NUME - preserve original
        nume = props_in.get("NUME", "")
        print(f"🔧 Preserved NUME: {nume} for feature {idx}")

        seed_base = f"{salt}:{idx}"

        # NR_CASE - ALWAYS generate synthetic (random range 100-5000)
        nr_case = stable_randint(100, 5000, seed_base + ":nr_case")
        print(f"🔧 Generated NR_CASE: {nr_case} for feature {idx}")

        # NR_CASE_ACOPERIRE - ALWAYS generate synthetic (random range 50-2000)
        nr_case_acoperire = stable_randint(50, 2000, seed_base + ":nr_case_acoperire")
        print(f"🔧 Generated NR_CASE_ACOPERIRE: {nr_case_acoperire} for feature {idx}")

        # NR_CASE_ACTIVE - ALWAYS generate synthetic (random range 50-1500)
        nr_case_active = stable_randint(50, 1500, seed_base + ":nr_case_active")
        print(f"🔧 Generated NR_CASE_ACTIVE: {nr_case_active} for feature {idx}")

        # NR_SCARI - ALWAYS generate synthetic (random range 10-500)
        nr_scari = stable_randint(10, 500, seed_base + ":nr_scari")
        print(f"🔧 Generated NR_SCARI: {nr_scari} for feature {idx}")

        # NR_APT - ALWAYS generate synthetic (random range 5-300)
        nr_apt = stable_randint(5, 300, seed_base + ":nr_apt")
        print(f"🔧 Generated NR_APT: {nr_apt} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["NUME"] = nume                    # Preserved original
        props_out["NR_CASE"] = str(nr_case)        # Generated synthetic
        props_out["NR_CASE_ACOPERIRE"] = str(nr_case_acoperire) # Generated synthetic
        props_out["NR_CASE_ACTIVE"] = str(nr_case_active)       # Generated synthetic
        props_out["NR_SCARI"] = str(nr_scari)      # Generated synthetic
        props_out["NR_APT"] = str(nr_apt)          # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": geometry,  # Preserve original geometry
            }
        )

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Zona Acoperire Hub Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} zona acoperire hub features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 NR_CASE, NR_CASE_ACOPERIRE, NR_CASE_ACTIVE, NR_SCARI, NR_APT generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


