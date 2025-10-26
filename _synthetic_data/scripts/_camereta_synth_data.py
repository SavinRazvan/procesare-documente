#!/usr/bin/env python3
"""
Camereta Synthetic Data Generator
==================================

Generates synthetic camereta data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: ID_TABELA, OBSERVATII_1, OBSERVATII_2, MI_PRINX
- Sets LOCALITATE to "UNKNOWN" if empty, otherwise preserves original
- Uses deterministic generation based on salt for consistency
- Compatible with current camereta processor field structure

Input:
  - _synthetic_data/data/_synth_input/camereta_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/camereta_centralized.geojson

Synthetic Fields Generated:
  - ID_TABELA: TAB100, TAB101, TAB102... (per locality counter)
  - OBSERVATII_1: Professional observation vocabulary
  - OBSERVATII_2: Professional observation vocabulary  
  - MI_PRINX: MI0001, MI0002, MI0003... (per locality counter)
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
# Script is at: _synthetic_data/scripts/_camereta_synth_data.py
# Inputs live under: _synthetic_data/data/_synth_input
# Outputs should go to: _synthetic_data/data/_synth_output
SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_CAM_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "camereta_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "camereta_centralized.geojson")



def main() -> None:
    salt = get_salt()
    
    # Try to load existing camereta data
    try:
        cam = load_geojson(SRC_CAM_PATH)
        features_in = cam.get("features", [])
        print(f"📁 Loaded {len(features_in)} features from {os.path.basename(SRC_CAM_PATH)}")
    except Exception:
        print(f"❌ Could not load input file {SRC_CAM_PATH}")
        return

    if not features_in:
        print("❌ No features found in input file")
        return

    features_out = []
    counters: Dict[str, int] = {}
    mi_prinx_counters: Dict[str, int] = {}

    # Enhanced observation vocabularies
    obs1_vocab = [
        "verificat vizual",
        "functional",
        "neaccesibil temporar",
        "defect minor",
        "revizie programata",
        "echipament OK",
        "necesita mentenanta",
        "temperatura normala",
        "cablu deteriorat",
        "infiltratii posibile"
    ]
    obs2_vocab = [
        "capace OK",
        "incuietoare OK",
        "infiltratii posibile",
        "urme interventie",
        "curatare recomandata",
        "ventilatie OK",
        "sigilare OK",
        "accesibilitate OK",
        "iluminat OK",
        "suprafata curata"
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

        # ID_TABELA - ALWAYS generate synthetic
        base = 100
        next_val = counters.get(localitate, base)
        id_tabela = f"TAB{next_val:03d}"  # Format as TAB100, TAB101, etc.
        counters[localitate] = next_val + 1
        print(f"🔧 Generated ID_TABELA: {id_tabela} for {localitate}")

        # OBSERVATII_1 - ALWAYS generate synthetic
        seed1 = f"{salt}:{localitate}:{idx}:obs1"
        observatii_1 = stable_choice(seed1, obs1_vocab)
        print(f"🔧 Generated OBSERVATII_1: {observatii_1} for feature {idx}")

        # OBSERVATII_2 - ALWAYS generate synthetic
        seed2 = f"{salt}:{localitate}:{idx}:obs2"
        observatii_2 = stable_choice(seed2, obs2_vocab)
        print(f"🔧 Generated OBSERVATII_2: {observatii_2} for feature {idx}")

        # MI_PRINX - ALWAYS generate synthetic
        mi_prinx_val = mi_prinx_counters.get(localitate, 1)
        mi_prinx = f"MI{mi_prinx_val:04d}"  # Format as MI0001, MI0002, etc.
        mi_prinx_counters[localitate] = mi_prinx_val + 1
        print(f"🔧 Generated MI_PRINX: {mi_prinx} for {localitate}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out = dict(original_props)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["LOCALITATE"] = localitate  # Set to UNKNOWN if empty
        props_out["ID_TABELA"] = id_tabela      # Generated synthetic
        props_out["OBSERVATII_1"] = observatii_1 # Generated synthetic
        props_out["OBSERVATII_2"] = observatii_2 # Generated synthetic
        props_out["MI_PRINX"] = mi_prinx         # Generated synthetic

        feature_obj = {
            "type": "Feature",
            "properties": props_out,
            "geometry": geometry,  # Preserve original geometry
        }

        features_out.append(feature_obj)

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Camereta Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} camereta features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 ID_TABELA, OBSERVATII_1, OBSERVATII_2, MI_PRINX generated for anonymization")
    print(f"📍 Original geometries and all fields preserved (LOCALITATE set to UNKNOWN if empty)")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


