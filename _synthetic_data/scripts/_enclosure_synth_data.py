#!/usr/bin/env python3
"""
Enclosure Synthetic Data Generator
===================================

Generates synthetic enclosure data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: ENCLOSURE_ID, OBSERVATII
- Sets LOCALITATE to "UNKNOWN" if empty, otherwise preserves original
- Uses deterministic generation based on salt for consistency
- Compatible with current enclosure processor field structure

Input:
  - _synthetic_data/data/_synth_input/enclosure_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/enclosure_centralized.geojson

Synthetic Fields Generated:
  - ENCLOSURE_ID: 1, 2, 3... (per locality counter)
  - OBSERVATII: Professional observation vocabulary
  - LOCALITATE: Set to "UNKNOWN" if empty, otherwise preserved

Requires: Python 3.9+, packages: geojson
"""

import os
from typing import Dict, Any, List

# Local utilities
from utils import (
    get_salt,
    stable_choice,
    load_geojson,
    save_geojson_single_line,
)


# Base directories
# Script is at: _synthetic_data/scripts/_enclosure_synth_data.py
# Inputs live under: _synthetic_data/data/_synth_input
# Outputs should go to: _synthetic_data/data/_synth_output
SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_ENC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "enclosure_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "enclosure_centralized.geojson")


def main() -> None:
    salt = get_salt()
    
    # Try to load existing enclosure data
    try:
        enc = load_geojson(SRC_ENC_PATH)
        features_in = enc.get("features", [])
        print(f"📁 Loaded {len(features_in)} features from {os.path.basename(SRC_ENC_PATH)}")
    except Exception:
        print(f"❌ Could not load input file {SRC_ENC_PATH}")
        return

    if not features_in:
        print("❌ No features found in input file")
        return

    features_out = []
    counters: Dict[str, int] = {}

    # Enhanced observation vocabulary
    obs_vocab = [
        "vizitat",
        "verificat rapid", 
        "in exploatare",
        "fara probleme vizibile",
        "curat, acces ok",
        "inchis corespunzator",
        "semnalizator prezent",
        "echipament functional",
        "necesita mentenanta",
        "temperatura normala",
        "cablu deteriorat",
        "infiltratii posibile",
        "revizie programata",
        "accesibilitate OK",
        "iluminat OK",
        "ventilatie OK"
    ]

    for idx, feat in enumerate(features_in, start=1):
        original_props = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry

        # LOCALITATE - preserve if exists and not empty, otherwise set to UNKNOWN
        localitate_raw = original_props.get("LOCALITATE")
        if localitate_raw and str(localitate_raw).strip():
            localitate = str(localitate_raw).strip()
        else:
            localitate = "UNKNOWN"
            print(f"🔧 Set LOCALITATE to UNKNOWN for feature {idx}")

        # ENCLOSURE_ID - ALWAYS generate synthetic (per-locality starting from 1)
        base = 1
        next_val = counters.get(localitate, base)
        enclosure_id = str(next_val)
        counters[localitate] = next_val + 1
        print(f"🔧 Generated ENCLOSURE_ID: {enclosure_id} for {localitate}")

        # OBSERVATII - ALWAYS generate synthetic
        seed = f"{salt}:{localitate}:{idx}:obs"
        observatii = stable_choice(seed, obs_vocab)
        print(f"🔧 Generated OBSERVATII: {observatii} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out = dict(original_props)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["LOCALITATE"] = localitate  # Set to UNKNOWN if empty
        props_out["ENCLOSURE_ID"] = enclosure_id  # Generated synthetic
        props_out["OBSERVATII"] = observatii       # Generated synthetic

        feature_obj = {
            "type": "Feature",
            "properties": props_out,
            "geometry": geometry,  # Preserve original geometry
        }

        features_out.append(feature_obj)

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Enclosure Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} enclosure features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 ENCLOSURE_ID, OBSERVATII generated for anonymization")
    print(f"📍 Original geometries and all fields preserved (LOCALITATE set to UNKNOWN if empty)")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


