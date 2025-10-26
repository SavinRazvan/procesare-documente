#!/usr/bin/env python3
"""
Zone Interventie Synthetic Data Generator
=========================================

Generates synthetic zone interventie data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: ECHIPA, TIP_ECHIPA
- Uses deterministic generation based on salt for consistency
- Compatible with current zone interventie processor field structure
- Professional team naming and categorization

Input:
  - _synthetic_data/data/_synth_input/zone_interventie_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/zone_interventie_centralized.geojson

Synthetic Fields Generated:
  - TIP_ECHIPA: BLOCURI (45%), CASE (45%), MENTENANTA (10%) - weighted choice
  - ECHIPA: Professional team names (e.g., "Barlad Blocuri 01", "Vaslui Case 02")
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    load_geojson,
    save_geojson_single_line,
    stable_weighted_choice,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "zone_interventie_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "zone_interventie_centralized.geojson")


def pick_tip_echipa(seed: str) -> str:
    """Generate professional team types with realistic distribution"""
    return stable_weighted_choice(seed, [
        ("BLOCURI", 45), 
        ("CASE", 45), 
        ("MENTENANTA", 10)
    ])


def build_echipa_name(localitate: str | None, tip_echipa: str, per_loc_type_index: int) -> str:
    """Build professional team names based on locality and team type"""
    loc = (localitate or "").strip()
    if not loc:
        loc = "UNKNOWN"
    
    # Professional team type labels
    label_map = {
        "BLOCURI": "Blocuri",
        "CASE": "Case", 
        "MENTENANTA": "Mentenanta",
    }
    
    label = label_map.get(tip_echipa, "Echipa")
    return f"{loc} {label} {per_loc_type_index:02d}".strip()


def main() -> None:
    salt = get_salt()
    
    # Try to load existing zone interventie data
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

    # Counters per (localitate, tip) for ECHIPA numbering
    echipa_idx_per_loc_type: Dict[str, int] = {}

    for idx, feat in enumerate(features_in, start=1):
        props_in: Dict[str, Any] = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry
        
        # Preserve original fields
        localitate = props_in.get("LOCALITATE", "")
        
        # TIP_ECHIPA - ALWAYS generate synthetic (professional team types)
        tip_echipa = pick_tip_echipa(f"{salt}:{idx}:tip")
        print(f"🔧 Generated TIP_ECHIPA: {tip_echipa} for feature {idx}")

        # ECHIPA - ALWAYS generate synthetic (professional team names)
        loc_type_key = f"{localitate}:{tip_echipa}"
        echipa_idx = echipa_idx_per_loc_type.get(loc_type_key, 1)
        echipa_idx_per_loc_type[loc_type_key] = echipa_idx + 1
        
        echipa = build_echipa_name(localitate, tip_echipa, echipa_idx)
        print(f"🔧 Generated ECHIPA: {echipa} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["ECHIPA"] = echipa        # Generated synthetic
        props_out["TIP_ECHIPA"] = tip_echipa  # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": geometry,  # Preserve original geometry
            }
        )

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Zone Interventie Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} zone interventie features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 ECHIPA, TIP_ECHIPA generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


