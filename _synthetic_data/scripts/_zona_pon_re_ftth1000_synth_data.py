#!/usr/bin/env python3
"""
Zona PON RE FTTH1000 Synthetic Data Generator
=============================================

Generates synthetic zona PON RE FTTH1000 data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: PON, OLT
- Uses deterministic generation based on salt for consistency
- Compatible with current zona PON RE FTTH1000 processor field structure

Input:
  - _synthetic_data/data/_synth_input/zona_pon_re_ftth1000_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/zona_pon_re_ftth1000_centralized.geojson

Synthetic Fields Generated:
  - PON: PON-0001, PON-0002, PON-0003... (sequential counter)
  - OLT: OLT-LOC-001, OLT-LOC-002... (extracts locality from original OLT if available)
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    load_geojson,
    save_geojson_single_line,
    extract_locality_from_olt,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "zona_pon_re_ftth1000_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "zona_pon_re_ftth1000_centralized.geojson")


def format_pon(seq: int) -> str:
    return f"PON-{seq:04d}"


def format_olt(locality: str, seq: int) -> str:
    return f"OLT-{locality}-{seq:03d}"


def main() -> None:
    salt = get_salt()
    
    # Try to load existing zona PON RE FTTH1000 data
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
    seq = 1

    for idx, feat in enumerate(features_in, start=1):
        props_in: Dict[str, Any] = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry
        
        seed_base = f"{salt}:{idx}"

        # PON - ALWAYS generate synthetic (PON-0001, PON-0002, etc.)
        pon = format_pon(seq)
        print(f"🔧 Generated PON: {pon} for feature {idx}")

        # OLT - ALWAYS generate synthetic (OLT-LOC-001, OLT-LOC-002, etc.)
        # Extract locality from original OLT if available, otherwise use generic
        original_olt = props_in.get("OLT", "")
        if original_olt:
            loc = extract_locality_from_olt(original_olt)
        else:
            loc = "UNKNOWN"
        
        olt = format_olt(loc, seq)
        print(f"🔧 Generated OLT: {olt} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["PON"] = pon      # Generated synthetic
        props_out["OLT"] = olt      # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": geometry,  # Preserve original geometry
            }
        )

        seq += 1

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Zona PON RE FTTH1000 Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} zona PON RE FTTH1000 features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 PON, OLT generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


