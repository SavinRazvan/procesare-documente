#!/usr/bin/env python3
"""
Camereta Search Synthetic Data Generator
========================================

Processes synthetic camereta data to create search-compatible output format.
Extracts only the fields required by the camereta_search model from synthetic data.

Features:
- Processes synthetic camereta data from _synth_output/camereta_centralized.geojson
- Extracts fields matching camereta_search model: LOCALITATE, ID_TABELA
- Creates centralized output matching original search processor format
- Preserves original geometries
- Skips features with empty required fields

Input:
  - _synthetic_data/data/_synth_output/camereta_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/camereta_search.geojson

Extracted Fields:
  - LOCALITATE: Locality name
  - ID_TABELA: Table identifier (TAB100, TAB101, etc.)

Note: This processor runs after main synthetic processors have generated the data.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import load_geojson, save_geojson_single_line


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_output", "camereta_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "camereta_search.geojson")


def main() -> None:
    # Try to load existing synthetic camereta data
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
        
        # Extract fields matching camereta_search model: LOCALITATE, ID_TABELA
        localitate = props_in.get("LOCALITATE", "")
        id_tabela = props_in.get("ID_TABELA", "")
        
        # Skip features with empty required fields
        if not localitate or not id_tabela:
            print(f"⚠️ Skipping feature {idx} with empty LOCALITATE or ID_TABELA")
            continue
        
        # Create search feature with only the required fields
        search_feature = {
            "type": "Feature",
            "properties": {
                "LOCALITATE": localitate,
                "ID_TABELA": id_tabela
            },
            "geometry": geometry
        }
        
        features_out.append(search_feature)
        print(f"🔧 Processed feature {idx}: {localitate} - {id_tabela}")

    out_fc = {
        "type": "FeatureCollection",
        "name": "Centralized Camereta Search Data",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} camereta search features from synthetic data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 Extracted LOCALITATE, ID_TABELA fields for search format")
    print(f"📍 Original geometries preserved")


if __name__ == "__main__":
    main()


