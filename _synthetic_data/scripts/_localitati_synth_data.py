#!/usr/bin/env python3
"""
Localitati Synthetic Data Generator
===================================

Generates synthetic localitati data that preserves original NUME and COMUNA fields,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Preserves original NUME and COMUNA (handles both uppercase and lowercase)
- Generates synthetic values for: NR_CASE, ID_CITY_VOICE, MI_PRINX, SIRUTA, OBS, PROIECTANT
- Uses deterministic generation based on salt for consistency
- Compatible with current localitati processor field structure

Input:
  - _synthetic_data/data/_synth_input/localitati_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/localitati_centralized.geojson

Synthetic Fields Generated:
  - NR_CASE: Random values 50-500
  - ID_CITY_VOICE: CV1000-CV9999 format
  - MI_PRINX: MI0001, MI0002... (per locality counter)
  - SIRUTA: Random values 100-1000000
  - OBS: Professional observation vocabulary
  - PROIECTANT: Professional project vocabulary

Preserved Fields:
  - NUME: Original locality name (case-insensitive)
  - COMUNA: Original commune name (case-insensitive)
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    stable_choice,
    stable_randint,
    load_geojson,
    save_geojson_single_line,
    pick_obs,
    pick_proiectant,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "localitati_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "localitati_centralized.geojson")


def main() -> None:
    salt = get_salt()
    
    # Try to load existing localitati data
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

    features_out = []
    mi_prinx_counters: Dict[str, int] = {}

    for idx, feat in enumerate(features_in, start=1):
        original_props = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry

        # nume - preserve original (check both uppercase and lowercase)
        nume = original_props.get("NUME", original_props.get("nume", ""))
        print(f"🔧 Preserved nume: {nume} for feature {idx}")

        # comuna - preserve original (check both uppercase and lowercase)
        comuna = original_props.get("COMUNA", original_props.get("comuna", ""))
        print(f"🔧 Preserved comuna: {comuna} for feature {idx}")

        # NR_CASE - ALWAYS generate synthetic
        seed_nr_case = f"{salt}:{nume}:{idx}:nr_case"
        nr_case = str(stable_randint(50, 500, seed_nr_case))
        print(f"🔧 Generated NR_CASE: {nr_case} for feature {idx}")

        # ID_CITY_VOICE - ALWAYS generate synthetic
        seed_id_cv = f"{salt}:{nume}:{idx}:id_city_voice"
        id_city_voice = f"CV{stable_randint(1000, 9999, seed_id_cv)}"
        print(f"🔧 Generated ID_CITY_VOICE: {id_city_voice} for feature {idx}")

        # MI_PRINX - ALWAYS generate synthetic (per locality counter)
        if nume not in mi_prinx_counters:
            mi_prinx_counters[nume] = 1
        mi_prinx = f"MI{mi_prinx_counters[nume]:04d}"
        mi_prinx_counters[nume] += 1
        print(f"🔧 Generated MI_PRINX: {mi_prinx} for feature {idx}")

        # SIRUTA - ALWAYS generate synthetic
        seed_siruta = f"{salt}:{nume}:{idx}:siruta"
        siruta = str(stable_randint(100, 1000000, seed_siruta))
        print(f"🔧 Generated SIRUTA: {siruta} for feature {idx}")

        # OBS - ALWAYS generate synthetic
        seed_obs = f"{salt}:{nume}:{idx}:obs"
        obs = pick_obs(seed_obs)
        print(f"🔧 Generated OBS: {obs} for feature {idx}")

        # PROIECTANT - ALWAYS generate synthetic
        seed_proj = f"{salt}:{nume}:{idx}:proj"
        proiectant = pick_proiectant(seed_proj)
        print(f"🔧 Generated PROIECTANT: {proiectant} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out = dict(original_props)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["NUME"] = nume          # Preserve original
        props_out["COMUNA"] = comuna      # Preserve original
        props_out["NR_CASE"] = nr_case           # Generated synthetic
        props_out["ID_CITY_VOICE"] = id_city_voice # Generated synthetic
        props_out["MI_PRINX"] = mi_prinx         # Generated synthetic
        props_out["SIRUTA"] = siruta             # Generated synthetic
        props_out["OBS"] = obs                   # Generated synthetic
        props_out["PROIECTANT"] = proiectant      # Generated synthetic

        feature_obj = {
            "type": "Feature",
            "properties": props_out,
            "geometry": geometry,  # Preserve original geometry
        }

        features_out.append(feature_obj)

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Localitati Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} localitati features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 NR_CASE, ID_CITY_VOICE, MI_PRINX, SIRUTA, OBS, PROIECTANT generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


