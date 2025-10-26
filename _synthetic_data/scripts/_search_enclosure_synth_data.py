#!/usr/bin/env python3
"""
Enclosure Search Synthetic Data Generator
=========================================

Processes synthetic enclosure data to create search-compatible output format.
Extracts only the fields required by the enclosure_search model from synthetic data.

Features:
- Processes synthetic enclosure data from _synth_output/enclosure_centralized.geojson
- Extracts fields matching enclosure_search model: ENCLOSURE_ID, LOCALITATE
- Creates centralized output matching original search processor format
- Preserves original geometries
- Skips features with empty required fields

Input:
  - _synthetic_data/data/_synth_output/enclosure_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/enclosure_search.geojson

Extracted Fields:
  - ENCLOSURE_ID: Enclosure identifier (1, 2, 3, etc.)
  - LOCALITATE: Locality name

Note: This processor runs after main synthetic processors have generated the data.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import load_geojson, save_geojson_single_line


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_output", "enclosure_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "enclosure_search.geojson")


def main() -> None:
    # Try to load existing synthetic enclosure data
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
        
        # Extract fields matching enclosure_search model: ENCLOSURE_ID, LOCALITATE
        enclosure_id = props_in.get("ENCLOSURE_ID", "")
        localitate = props_in.get("LOCALITATE", "")
        
        # Skip features with empty required fields
        if not enclosure_id or not localitate:
            print(f"⚠️ Skipping feature {idx} with empty ENCLOSURE_ID or LOCALITATE")
            continue
        
        # Create search feature with only the required fields
        search_feature = {
            "type": "Feature",
            "properties": {
                "ENCLOSURE_ID": enclosure_id,
                "LOCALITATE": localitate
            },
            "geometry": geometry
        }
        
        features_out.append(search_feature)
        print(f"🔧 Processed feature {idx}: {localitate} - {enclosure_id}")

    out_fc = {
        "type": "FeatureCollection",
        "name": "Centralized Enclosure Search Data",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} enclosure search features from synthetic data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 Extracted ENCLOSURE_ID, LOCALITATE fields for search format")
    print(f"📍 Original geometries preserved")


if __name__ == "__main__":
    main()


