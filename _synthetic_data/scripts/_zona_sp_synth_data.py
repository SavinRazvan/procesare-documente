#!/usr/bin/env python3
"""
Zona SP Synthetic Data Generator
===============================

Generates synthetic zona SP data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: ID_ZONA
- Uses deterministic generation based on salt for consistency
- Compatible with current zona SP processor field structure

Input:
  - _synthetic_data/data/_synth_input/zona_spliter_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/zona_spliter_centralized.geojson

Synthetic Fields Generated:
  - ID_ZONA: Deterministic UUIDv5 generated from salt + geometry
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    load_geojson,
    save_geojson_single_line,
    deterministic_uuid5,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "zona_spliter_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "zona_spliter_centralized.geojson")


def format_pon(seq: int) -> str:
    return f"PON-SP-{seq:04d}"


def main() -> None:
    salt = get_salt()
    
    # Try to load existing zona SP data
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
        
        # ID_ZONA - ALWAYS generate synthetic (deterministic UUIDv5 from salt+geometry)
        id_seed = f"{salt}:{idx}:{geometry}"
        id_zona = deterministic_uuid5(id_seed)
        print(f"🔧 Generated ID_ZONA: {id_zona} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["ID_ZONA"] = id_zona  # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": geometry,  # Preserve original geometry
            }
        )

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Zona SP Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} zona SP features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 ID_ZONA generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


