#!/usr/bin/env python3
"""
Fibra Synthetic Data Generator
==============================

Generates synthetic fibra data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: NR_FIRE, LUNGIME_HARTA, LUNGIME_TEREN, AMPLASARE
- Sets LOCALITATE to "UNKNOWN" if empty, otherwise preserves original
- Uses deterministic generation based on salt for consistency
- Compatible with current fibra processor field structure

Input:
  - _synthetic_data/data/_synth_input/fibra_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/fibra_centralized.geojson

Synthetic Fields Generated:
  - NR_FIRE: Realistic fiber counts (4, 12, 24, 48, 96, 144, 288)
  - LUNGIME_HARTA: Original value rounded + random float (1.00-99.99)
  - LUNGIME_TEREN: Original value rounded + random float (1.00-99.99)
  - AMPLASARE: Realistic placement options (subteran, aerian, etc.)
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
# Script is at: _synthetic_data/scripts/_fibra_synth_data.py
# Inputs live under: _synthetic_data/data/_synth_input
# Outputs should go to: _synthetic_data/data/_synth_output
SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_FIBRA_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "fibra_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "fibra_centralized.geojson")


def main() -> None:
    salt = get_salt()
    
    # Try to load existing fibra data
    try:
        fc = load_geojson(SRC_FIBRA_PATH)
        features_in = fc.get("features", [])
        print(f"📁 Loaded {len(features_in)} features from {os.path.basename(SRC_FIBRA_PATH)}")
    except Exception:
        print(f"❌ Could not load input file {SRC_FIBRA_PATH}")
        return

    if not features_in:
        print("❌ No features found in input file")
        return

    features_out = []

    # NR_FIRE options - realistic fiber counts
    nr_fire_options = ["4", "12", "24", "48", "96", "144", "288"]

    # AMPLASARE options - realistic placement values
    amplasare_options = [
        "subteran in canalizatie",
        "subteran direct in sol", 
        "aerian pe stalpi",
        "aerian pe fatada",
        "tubulatura existenta",
        "canalizatie noua",
        "pe stalpi existenti",
        "pe fatada cladirii"
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

        # NR_FIRE - ALWAYS generate synthetic
        seed_nr_fire = f"{salt}:{localitate}:{idx}:nr_fire"
        nr_fire = stable_choice(seed_nr_fire, nr_fire_options)
        print(f"🔧 Generated NR_FIRE: {nr_fire} for feature {idx}")

        # LUNGIME_HARTA - round original value and add random float (1.00-99.99)
        original_lungime = original_props.get("LUNGIME_HARTA", "0")
        try:
            # Convert to float, round to nearest integer
            base_value = round(float(str(original_lungime).replace(",", ".")))
            # Add random float between 1.00 and 99.99
            import random
            random.seed(hash(f"{salt}:{localitate}:{idx}:lungime_harta") % (2**32))
            random_float = round(random.uniform(1.00, 99.99), 2)
            lungime_harta = round(base_value + random_float, 2)
        except (ValueError, TypeError):
            # If conversion fails, use a default value
            import random
            random.seed(hash(f"{salt}:{localitate}:{idx}:lungime_harta") % (2**32))
            lungime_harta = round(random.uniform(100.00, 999.99), 2)
        print(f"🔧 Generated LUNGIME_HARTA: {lungime_harta} for feature {idx}")

        # LUNGIME_TEREN - similar to LUNGIME_HARTA
        original_teren = original_props.get("LUNGIME_TEREN", "0")
        try:
            base_value = round(float(str(original_teren).replace(",", ".")))
            import random
            random.seed(hash(f"{salt}:{localitate}:{idx}:lungime_teren") % (2**32))
            random_float = round(random.uniform(1.00, 99.99), 2)
            lungime_teren = round(base_value + random_float, 2)
        except (ValueError, TypeError):
            import random
            random.seed(hash(f"{salt}:{localitate}:{idx}:lungime_teren") % (2**32))
            lungime_teren = round(random.uniform(50.00, 500.00), 2)
        print(f"🔧 Generated LUNGIME_TEREN: {lungime_teren} for feature {idx}")

        # AMPLASARE - ALWAYS generate synthetic
        seed_amplasare = f"{salt}:{localitate}:{idx}:amplasare"
        amplasare = stable_choice(seed_amplasare, amplasare_options)
        print(f"🔧 Generated AMPLASARE: {amplasare} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out = dict(original_props)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["LOCALITATE"] = localitate  # Set to UNKNOWN if empty
        props_out["NR_FIRE"] = nr_fire           # Generated synthetic
        props_out["LUNGIME_HARTA"] = lungime_harta # Generated synthetic
        props_out["LUNGIME_TEREN"] = lungime_teren # Generated synthetic
        props_out["AMPLASARE"] = amplasare        # Generated synthetic

        feature_obj = {
            "type": "Feature",
            "properties": props_out,
            "geometry": geometry,  # Preserve original geometry
        }

        features_out.append(feature_obj)

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Fibra Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} fibra features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 NR_FIRE, LUNGIME_HARTA, LUNGIME_TEREN, AMPLASARE generated for anonymization")
    print(f"📍 Original geometries and all fields preserved (LOCALITATE set to UNKNOWN if empty)")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


