#!/usr/bin/env python3
"""
Scari Search Synthetic Data Generator
======================================

Processes synthetic scari data to create search-compatible output format.
Extracts only the fields required by the scari_search model from synthetic data.

Features:
- Processes synthetic scari data from _synth_output/scari_centralized.geojson
- Extracts fields matching scari_search model: COD_FTTB, TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, LOCALITATE
- Creates centralized output matching original search processor format
- Preserves original geometries
- Skips features with empty required fields

Input:
  - _synthetic_data/data/_synth_output/scari_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/scari_search.geojson

Extracted Fields:
  - COD_FTTB: FTTB code identifier
  - TIP_ART: Article type (Strada, Bulevard, etc.)
  - DENUMIRE_ART: Article name
  - NR_ART: Article number
  - DENUMIRE_BLOC: Block name
  - NR_SCARA: Stair number
  - LOCALITATE: Locality name

Note: This processor runs after main synthetic processors have generated the data.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import load_geojson, save_geojson_single_line


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_output", "scari_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "scari_search.geojson")


def main() -> None:
    # Try to load existing synthetic scari data
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
        
        # Extract fields matching scari_search model: COD_FTTB, TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, LOCALITATE
        cod_fttb = props_in.get("COD_FTTB", "")
        tip_art = props_in.get("TIP_ART", "")
        denumire_art = props_in.get("DENUMIRE_ART", "")
        nr_art = props_in.get("NR_ART", "")
        denumire_bloc = props_in.get("DENUMIRE_BLOC", "")
        nr_scara = props_in.get("NR_SCARA", "")
        localitate = props_in.get("LOCALITATE", "")
        
        # Skip features with empty required fields
        if not cod_fttb or not tip_art or not denumire_art or not nr_art or not denumire_bloc or not nr_scara or not localitate:
            print(f"⚠️ Skipping feature {idx} with empty required fields")
            continue
        
        # Create search feature with only the required fields
        search_feature = {
            "type": "Feature",
            "properties": {
                "COD_FTTB": cod_fttb,
                "TIP_ART": tip_art,
                "DENUMIRE_ART": denumire_art,
                "NR_ART": nr_art,
                "DENUMIRE_BLOC": denumire_bloc,
                "NR_SCARA": nr_scara,
                "LOCALITATE": localitate
            },
            "geometry": geometry
        }
        
        features_out.append(search_feature)
        print(f"🔧 Processed feature {idx}: {localitate} - {cod_fttb}")

    out_fc = {
        "type": "FeatureCollection",
        "name": "Centralized Scari Search Data",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} scari search features from synthetic data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 Extracted COD_FTTB, TIP_ART, DENUMIRE_ART, NR_ART, DENUMIRE_BLOC, NR_SCARA, LOCALITATE fields for search format")
    print(f"📍 Original geometries preserved")


if __name__ == "__main__":
    main()