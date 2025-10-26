#!/usr/bin/env python3
"""
FTTB Search Synthetic Data Generator
====================================

Processes synthetic case and scari data to create FTTB search-compatible output format.
Extracts only the fields required by the fttb_search model from synthetic data.

Features:
- Processes synthetic case files from _synth_output/case/ directory
- Processes synthetic scari data from _synth_output/scari_centralized.geojson
- Extracts fields matching fttb_search model: COD_FTTB, LOCALITATE
- Creates centralized output matching original search processor format
- Preserves original geometries
- Skips features with empty required fields

Input:
  - _synthetic_data/data/_synth_output/case/CASE_*.geojson (all files)
  - _synthetic_data/data/_synth_output/scari_centralized.geojson

Output:
  - _synthetic_data/data/_synth_output/fttb_search.geojson

Extracted Fields:
  - COD_FTTB: FTTB code identifier
  - LOCALITATE: Locality name

Note: This processor runs after main synthetic processors have generated the data.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from utils import load_geojson, save_geojson_single_line


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
CASE_DIR = os.path.join(DATA_ROOT, "data", "_synth_output", "case")
SCARI_PATH = os.path.join(DATA_ROOT, "data", "_synth_output", "scari_centralized.geojson")
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output"))
OUT_PATH = os.path.join(OUT_DIR, "fttb_search.geojson")


def _discover_case_files() -> List[str]:
    """Discover all case files in the case directory"""
    case_files = []
    if os.path.exists(CASE_DIR):
        for file in os.listdir(CASE_DIR):
            if file.endswith('.geojson') and file.startswith('CASE_'):
                case_files.append(os.path.join(CASE_DIR, file))
    return case_files


def main() -> None:
    features_out: List[Dict[str, Any]] = []
    
    # Process case files
    case_files = _discover_case_files()
    print(f"📁 Found {len(case_files)} case files to process")
    
    for case_file in case_files:
        try:
            fc = load_geojson(case_file)
            features_in = fc.get("features", [])
            print(f"📁 Loaded {len(features_in)} features from {os.path.basename(case_file)}")
            
            for idx, feat in enumerate(features_in, start=1):
                props_in: Dict[str, Any] = dict(feat.get("properties", {}))
                geometry = feat.get("geometry")  # Preserve original geometry
                
                # Extract fields matching fttb_search model: COD_FTTB, LOCALITATE
                cod_fttb = props_in.get("COD_FTTB", "")
                localitate = props_in.get("LOCALITATE", "")
                
                # Skip features with empty required fields
                if not cod_fttb or not localitate:
                    print(f"⚠️ Skipping case feature {idx} with empty required fields")
                    continue
                
                # Create search feature with only the required fields
                search_feature = {
                    "type": "Feature",
                    "properties": {
                        "COD_FTTB": cod_fttb,
                        "LOCALITATE": localitate
                    },
                    "geometry": geometry
                }
                
                features_out.append(search_feature)
                print(f"🔧 Processed case feature {idx}: {localitate} - {cod_fttb}")
                
        except Exception as e:
            print(f"❌ Error processing case file {case_file}: {e}")
            continue
    
    # Process scari file
    try:
        fc = load_geojson(SCARI_PATH)
        features_in = fc.get("features", [])
        print(f"📁 Loaded {len(features_in)} features from {os.path.basename(SCARI_PATH)}")
        
        for idx, feat in enumerate(features_in, start=1):
            props_in: Dict[str, Any] = dict(feat.get("properties", {}))
            geometry = feat.get("geometry")  # Preserve original geometry
            
            # Extract fields matching fttb_search model: COD_FTTB, LOCALITATE
            cod_fttb = props_in.get("COD_FTTB", "")
            localitate = props_in.get("LOCALITATE", "")
            
            # Skip features with empty required fields
            if not cod_fttb or not localitate:
                print(f"⚠️ Skipping scari feature {idx} with empty required fields")
                continue
            
            # Create search feature with only the required fields
            search_feature = {
                "type": "Feature",
                "properties": {
                    "COD_FTTB": cod_fttb,
                    "LOCALITATE": localitate
                },
                "geometry": geometry
            }
            
            features_out.append(search_feature)
            print(f"🔧 Processed scari feature {idx}: {localitate} - {cod_fttb}")
            
    except Exception as e:
        print(f"❌ Error processing scari file {SCARI_PATH}: {e}")

    if not features_out:
        print("❌ No features found to process")
        return

    out_fc = {
        "type": "FeatureCollection",
        "name": "Centralized FTTB Search Data",
        "features": features_out,
    }

    save_geojson_single_line(out_fc, OUT_PATH)
    print(f"\n✅ Processed {len(features_out)} FTTB search features from synthetic data")
    print(f"📁 Created output file: {OUT_PATH}")
    print(f"🔧 Extracted COD_FTTB, LOCALITATE fields for search format")
    print(f"📍 Original geometries preserved")


if __name__ == "__main__":
    main()


