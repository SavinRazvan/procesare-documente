#!/usr/bin/env python3
"""
Scari Synthetic Data Generator
==============================

Generates synthetic scari data that preserves all original fields and geometries,
while anonymizing specific sensitive fields with deterministic synthetic values.

Features:
- Preserves ALL original fields and geometries from input data
- Generates synthetic values for: COD_FTTB, ZONA_RETEA, OBSERVATII, ZONA_RETEA_FTTH1000, ZONA_RETEA_FTTH_V2
- Uses deterministic generation based on salt for consistency
- Compatible with current scari processor field structure
- Can generate synthetic data from scratch if no input file exists

Input:
  - _synthetic_data/data/_synth_input/scari_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/scari_centralized.geojson

Synthetic Fields Generated:
  - COD_FTTB: VSX0001, VSX0002... (per locality counter)
  - ZONA_RETEA: Zona A, Zona B, Zona C, Zona D, Zona E
  - OBSERVATII: Professional observation vocabulary
  - ZONA_RETEA_FTTH1000: FTTH1000-A, FTTH1000-B, FTTH1000-C, FTTH1000-D
  - ZONA_RETEA_FTTH_V2: FTTH-V2-A, FTTH-V2-B, FTTH-V2-C, FTTH-V2-D

Note: If input file doesn't exist, generates 250 synthetic features from scratch.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import (
    get_salt,
    stable_choice,
    load_geojson,
    save_geojson_single_line,
    normalize_tip_art,
    digits_to_letters_only,
    stable_randint,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_PATH = os.path.join(DATA_ROOT, "data", "_synth_input", "scari_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "scari_centralized.geojson")


def format_fttb(localitate: str, seq: int) -> str:
    initial = (localitate or "").strip()[:1].upper() or "X"
    return f"VS{initial}{seq:04d}"


def main() -> None:
    salt = get_salt()
    
    # Try to load existing scari data, if not available generate from scratch
    try:
        fc = load_geojson(SRC_PATH)
        features_in = fc.get("features", [])
    except Exception:
        print(f"Input file {SRC_PATH} not found, generating synthetic scari data from scratch")
        features_in = []

    features_out: List[Dict[str, Any]] = []
    fttb_counters: Dict[str, int] = {}

    # Default localities
    default_localities = ["Barlad", "Vaslui", "Husi", "Murgeni", "Negresti", "Perieni", "Podu Iloaiei"]
    
    # Street names and types for synthetic generation
    street_types = ["Strada", "Bulevard", "Aleea", "Calea", "Piata", "Splaiul"]
    street_names = [
        "Independentei", "Unirii", "Eroilor", "Capitalei", "Constructorilor",
        "Viitorului", "Trandafirilor", "Stejarului", "Castanilor", "Lalelelor",
        "Libertatii", "Pacii", "Revolutiei", "Democratiei", "Natiunilor"
    ]
    
    # Building names
    building_names = [
        "Bloc A", "Bloc B", "Bloc C", "Bloc D", "Bloc E", "Bloc F",
        "Complex A", "Complex B", "Complex C", "Complex D",
        "Residence A", "Residence B", "Residence C"
    ]
    
    # Network types and zones
    tip_retea_values = ["FTTH", "FTTB", "FTTC", "HFC", "DSL", "Wireless"]
    zona_retea_values = ["Zona A", "Zona B", "Zona C", "Zona D", "Zona E"]
    zona_retea_ftth1000_values = ["FTTH1000-A", "FTTH1000-B", "FTTH1000-C", "FTTH1000-D"]
    zona_retea_ftth_v2_values = ["FTTH-V2-A", "FTTH-V2-B", "FTTH-V2-C", "FTTH-V2-D"]
    
    # Observation vocabulary
    observatii_vocab = [
        "necesita localizare", "verificat teren", "in analiza", "echipament functional",
        "cablu OK", "accesibilitate OK", "mentenanta programata", "extindere planificata",
        "modernizare necesara", ""
    ]

    # If no input features, generate synthetic ones
    if not features_in:
        print("Generating synthetic scari features from scratch...")
        # Generate 250 synthetic features
        for i in range(250):
            # Generate coordinates (Romania bounds approximately)
            lat = stable_randint(45500000, 48000000, f"{salt}:{i}:lat") / 1000000  # 45.5 to 48.0
            lon = stable_randint(22000000, 30000000, f"{salt}:{i}:lon") / 1000000  # 22.0 to 30.0
            
            geometry = {
                "type": "Point",
                "coordinates": [lon, lat]
            }
            
            features_in.append({
                "type": "Feature",
                "properties": {},
                "geometry": geometry
            })

    for idx, feat in enumerate(features_in, start=1):
        props_in: Dict[str, Any] = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry
        
        # LOCALITATE - preserve original
        localitate = props_in.get("LOCALITATE", "")
        print(f"🔧 Preserved LOCALITATE: {localitate} for feature {idx}")
        
        seed_base = f"{salt}:{localitate}:{idx}"

        # COD_FTTB - ALWAYS generate synthetic
        if localitate not in fttb_counters:
            fttb_counters[localitate] = 1
        cod_fttb = format_fttb(localitate, fttb_counters[localitate])
        fttb_counters[localitate] += 1
        print(f"🔧 Generated COD_FTTB: {cod_fttb} for feature {idx}")

        # ZONA_RETEA - ALWAYS generate synthetic
        zona_retea = stable_choice(seed_base + ":zona_retea", zona_retea_values)
        print(f"🔧 Generated ZONA_RETEA: {zona_retea} for feature {idx}")

        # OBSERVATII - ALWAYS generate synthetic
        observatii = stable_choice(seed_base + ":obs", observatii_vocab)
        print(f"🔧 Generated OBSERVATII: {observatii} for feature {idx}")

        # ZONA_RETEA_FTTH1000 - ALWAYS generate synthetic
        zona_retea_ftth1000 = stable_choice(seed_base + ":ftth1000", zona_retea_ftth1000_values)
        print(f"🔧 Generated ZONA_RETEA_FTTH1000: {zona_retea_ftth1000} for feature {idx}")

        # ZONA_RETEA_FTTH_V2 - ALWAYS generate synthetic
        zona_retea_ftth_v2 = stable_choice(seed_base + ":ftth_v2", zona_retea_ftth_v2_values)
        print(f"🔧 Generated ZONA_RETEA_FTTH_V2: {zona_retea_ftth_v2} for feature {idx}")

        # Build properties - preserve all original fields, only modify specific ones
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields with synthetic data
        props_out["COD_FTTB"] = cod_fttb           # Generated synthetic
        props_out["ZONA_RETEA"] = zona_retea       # Generated synthetic
        props_out["OBSERVATII"] = observatii       # Generated synthetic
        props_out["ZONA_RETEA_FTTH1000"] = zona_retea_ftth1000  # Generated synthetic
        props_out["ZONA_RETEA_FTTH_V2"] = zona_retea_ftth_v2    # Generated synthetic

        features_out.append(
            {
                "type": "Feature",
                "properties": props_out,
                "geometry": feat.get("geometry"),
            }
        )

    out_fc = {
        "type": "FeatureCollection",
        "name": "Synthetic Scari Data V2",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} scari features from real data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 COD_FTTB, ZONA_RETEA, OBSERVATII, ZONA_RETEA_FTTH1000, ZONA_RETEA_FTTH_V2 generated for anonymization")
    print(f"📍 Original geometries and all fields preserved")
    print(f"📋 All original fields preserved with synthetic data for specified fields")


if __name__ == "__main__":
    main()


