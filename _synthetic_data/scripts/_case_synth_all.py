#!/usr/bin/env python3
"""
Case Synthetic Data Generator
=============================

Generates synthetic case data by processing individual CASE_*.geojson files,
preserving all original fields and geometries while anonymizing only ZONA_RETEA.

Features:
- Processes each CASE_*.geojson file individually from _synth_input/case/
- Preserves ALL original fields and geometries from input data
- Generates synthetic values ONLY for ZONA_RETEA field
- Creates corresponding output files with same names in _synth_output/case/
- Generates manifest.json file in output case directory
- Uses deterministic generation based on salt for consistency

Input:
  - _synthetic_data/data/_synth_input/case/CASE_*.geojson (all files)

Output:
  - _synthetic_data/data/_synth_output/case/CASE_*.geojson (same names)
  - _synthetic_data/data/_synth_output/case/manifest.json

Synthetic Fields Generated:
  - ZONA_RETEA: Realistic OLT zone names (olt01.barlad_13_5, olt02.vaslui_8_3, etc.)

Usage:
  python _synthetic_data/scripts/_case_synth_all.py
  python _synthetic_data/scripts/_case_synth_all.py --file "CASE_BARLAD.geojson"
"""

from __future__ import annotations

import argparse
import glob
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from utils import (
    get_salt,
    stable_choice,
    stable_randint,
    load_geojson,
    save_geojson_single_line,
    normalize_tip_art,
    format_fttb_code,
    compute_digi_id,
)


SCRIPT_DIR = os.path.dirname(__file__)
DATA_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
# SRC_DIR removed - now using dynamic path discovery in _discover_files()
OUT_DIR = os.path.abspath(os.path.join(DATA_ROOT, "data", "_synth_output", "case"))


def _title_case(value: Any) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    # Basic title-case; keep parentheses and punctuation
    return s.title()


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _is_numeric_str(value: Any) -> bool:
    s = str(value).strip()
    if not s:
        return False
    return s.isdigit()


def _clamp_int_str(value: Any, min_value: int, max_value: int) -> str:
    s = str(value)
    try:
        # allow float-like strings, then cast to int
        n = int(float(s.replace(",", ".")))
    except Exception:
        return s
    if n < min_value:
        n = min_value
    if n > max_value:
        n = max_value
    return str(n)


def _normalize_empty_to_blank(value: Any) -> str:
    if value is None:
        return ""
    s = str(value)
    if s.strip() == "":
        return ""
    return s


def _deterministic_voice(seed: str) -> str:
    # Small deterministic chance of 1 (e.g., 5%)
    return "1" if stable_randint(1, 100, seed) <= 5 else "0"


def _process_file(path: str, salt: str) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # Try to load existing case data
    try:
        fc = load_geojson(path)
        features: List[Dict[str, Any]] = fc.get("features", []) or []
        print(f"📁 Loaded {len(features)} features from {os.path.basename(path)}")
    except Exception:
        print(f"❌ Could not load input file {path}")
        return

    if not features:
        print("❌ No features found in input file")
        return

    file_basename = os.path.basename(path)
    features_out: List[Dict[str, Any]] = []

    # Synthetic values for specific fields
    zona_retea_values = [
        "olt01.barlad_13_5", "olt01.barlad_16_7", "olt02.vaslui_8_3", "olt03.husi_12_4",
        "olt04.murgeni_15_6", "olt05.negresti_9_2", "olt06.perieni_11_5", "olt07.podu_iloaiei_14_7",
        "olt08.falciu_7_3", "olt09.bunesti_13_6", "olt10.dragomiresti_10_4", "olt11.epureni_16_8",
        "olt12.gherghesti_8_3", "olt13.iana_12_5", "olt14.laza_9_4", "olt15.lipovat_11_6",
        "olt16.lunca_14_7", "olt17.malusteni_7_3", "olt18.manzati_13_6", "olt19.maraseni_10_4"
    ]

    for idx, feat in enumerate(features, start=1):
        props_in: Dict[str, Any] = dict(feat.get("properties", {}))
        geometry = feat.get("geometry")  # Preserve original geometry

        # Extract locality from filename (remove CASE_ prefix and .geojson suffix)
        locality_from_filename = file_basename.replace("CASE_", "").replace(".geojson", "").replace("_", " ").title()

        # LOCALITATE - preserve if exists, otherwise use filename
        loc_raw = props_in.get("LOCALITATE")
        localitate = _title_case(loc_raw) if loc_raw else locality_from_filename

        # TIP_ART - preserve if exists, normalize if needed
        tip_art_raw = props_in.get("TIP_ART")
        if tip_art_raw and str(tip_art_raw).strip():
            tip_art = normalize_tip_art(_as_str(tip_art_raw), seed=f"{salt}:{file_basename}:{idx}:TIP_ART")
        else:
            tip_art = "Strada"  # Default

        # DENUMIRE_ART - preserve if exists
        denumire_art_raw = props_in.get("DENUMIRE_ART")
        if denumire_art_raw and str(denumire_art_raw).strip():
            denumire_art = _title_case(denumire_art_raw)
        else:
            denumire_art = "Sintetica"

        # NR_ART - preserve if exists
        nr_art_raw = props_in.get("NR_ART")
        if nr_art_raw and str(nr_art_raw).strip():
            nr_art = str(nr_art_raw)
        else:
            nr_art = str(idx)

        # STARE_RETEA - preserve if exists
        stare_retea_raw = props_in.get("STARE_RETEA")
        if stare_retea_raw and str(stare_retea_raw).strip():
            stare_retea = str(stare_retea_raw)
        else:
            stare_retea = "4"  # Default

        # ZONA_RETEA - ALWAYS generate synthetic (this is what you want to anonymize)
        zona_retea = stable_choice(f"{salt}:{file_basename}:{idx}:ZONA", zona_retea_values)
        print(f"🔧 Generated ZONA_RETEA: {zona_retea} for feature {idx}")

        # TIP_ECHIPAMENT - preserve if exists
        tip_echipament_raw = props_in.get("TIP_ECHIPAMENT")
        if tip_echipament_raw and str(tip_echipament_raw).strip():
            tip_echipament = str(tip_echipament_raw)
        else:
            tip_echipament = "1"  # Default

        # OBSERVATII - preserve if exists
        obs_raw = props_in.get("OBSERVATII")
        if obs_raw and str(obs_raw).strip():
            observatii = str(obs_raw)
        else:
            observatii = ""  # Default

        # COD_FTTB - preserve original (or generate if you want to anonymize this too)
        cod_fttb_raw = props_in.get("COD_FTTB")
        if cod_fttb_raw and str(cod_fttb_raw).strip():
            cod_fttb = str(cod_fttb_raw)
        else:
            # Generate synthetic COD_FTTB if needed
            cod_fttb = f"VS{localitate[:2].upper()}{idx:04d}"

        # Build properties - preserve all original fields, only modify ZONA_RETEA
        props_out: Dict[str, Any] = dict(props_in)  # Start with all original fields
        
        # Override specific fields
        props_out["COD_FTTB"] = cod_fttb
        props_out["LOCALITATE"] = localitate
        props_out["TIP_ART"] = tip_art
        props_out["DENUMIRE_ART"] = denumire_art
        props_out["NR_ART"] = nr_art
        props_out["STARE_RETEA"] = stare_retea
        props_out["ZONA_RETEA"] = zona_retea  # This is the synthetic field
        props_out["TIP_ECHIPAMENT"] = tip_echipament
        props_out["OBSERVATII"] = observatii

        feature_obj = {
            "type": "Feature",
            "properties": props_out,
            "geometry": geometry,  # Preserve original geometry
        }
        
        features_out.append(feature_obj)

    # Create output file with same name as input
    output_fc = {
        "type": "FeatureCollection",
        "name": f"Synthetic Case Data - {file_basename}",
        "features": features_out,
    }
    
    output_path = os.path.join(OUT_DIR, file_basename)
    save_geojson_single_line(output_fc, output_path)
    
    print(f"✅ Processed {len(features_out)} features from {file_basename}")
    print(f"📁 Created output file: {output_path}")
    print(f"🔧 ZONA_RETEA values generated for anonymization")
    print(f"📍 Original geometries and other fields preserved")


def _discover_files(explicit_files: List[str] | None = None) -> List[str]:
    if explicit_files:
        return [p for p in explicit_files if os.path.isfile(p)]

    # Look for case files in the input directory
    input_dir = os.path.join(os.path.dirname(__file__), "..", "data", "_synth_input", "case")
    if not os.path.isdir(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        return []

    # Find all CASE_*.geojson files
    case_files = []
    for filename in os.listdir(input_dir):
        if filename.startswith("CASE_") and filename.endswith(".geojson"):
            case_files.append(os.path.join(input_dir, filename))

    case_files.sort()  # Sort for consistent processing order
    print(f"📁 Found {len(case_files)} case files in {input_dir}")
    return case_files


def generate_manifest(output_dir: str) -> str:
    """Generate manifest.json file for case files"""
    import json
    from pathlib import Path
    
    output_path = Path(output_dir)
    case_dir = output_path / "case"
    
    if not case_dir.exists():
        print(f"⚠️ Case directory {case_dir} does not exist, cannot generate manifest")
        return None
    
    # Find all GeoJSON files in the case directory
    geojson_files = list(case_dir.glob("*.geojson"))
    
    if not geojson_files:
        print(f"⚠️ No GeoJSON files found in {case_dir}")
        return None
    
    # Priority files (always at the top)
    priority_files = ["CASE_BARLAD.geojson", "CASE_VASLUI.geojson"]
    
    # Create manifest entries
    manifest_entries = []
    
    # Add priority files first
    for priority_file in priority_files:
        priority_path = case_dir / priority_file
        if priority_path.exists():
            stat = priority_path.stat()
            manifest_entries.append({
                "name": priority_file,
                "size": stat.st_size,
                "modified": int(stat.st_mtime),
                "path": f"data/case/{priority_file}"
            })
    
    # Add all other files in alphabetical order
    other_files = [f for f in geojson_files if f.name not in priority_files]
    other_files.sort(key=lambda x: x.name)
    
    for file_path in other_files:
        stat = file_path.stat()
        manifest_entries.append({
            "name": file_path.name,
            "size": stat.st_size,
            "modified": int(stat.st_mtime),
            "path": f"data/case/{file_path.name}"
        })
    
    # Write manifest file
    manifest_file = case_dir / "manifest.json"
    try:
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest_entries, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Generated manifest.json with {len(manifest_entries)} entries")
        return str(manifest_file)
        
    except Exception as e:
        print(f"❌ Failed to generate manifest.json: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Individual synthetic processor for case files - creates same number of output files")
    parser.add_argument(
        "--file",
        dest="files",
        action="append",
        help="Specific input file under _synthetic_data/data/_synth_input/case/ to process. Can be provided multiple times.",
    )
    args = parser.parse_args()

    salt = get_salt()
    files = _discover_files(args.files)
    if not files:
        input_dir = os.path.join(os.path.dirname(__file__), "..", "data", "_synth_input", "case")
        print(f"No input files found in {input_dir}.")
        return

    print(f"🚀 Processing {len(files)} case files individually...")
    print(f"📁 Each input file will create a corresponding output file with same name")
    print(f"🔧 Only ZONA_RETEA field will be generated synthetically")
    print("=" * 80)
    
    processed_count = 0
    for p in files:
        try:
            _process_file(p, salt)
            processed_count += 1
            print("-" * 40)
        except Exception as exc:
            print(f"ERROR processing {p}: {exc}")
    
    print(f"\n🎉 Successfully processed {processed_count}/{len(files)} case files")
    print(f"📁 Output files created in: {OUT_DIR}")
    
    # Generate manifest.json file
    manifest_file = generate_manifest(os.path.dirname(OUT_DIR))
    if manifest_file:
        print(f"📋 Manifest file: {manifest_file}")


if __name__ == "__main__":
    main()


