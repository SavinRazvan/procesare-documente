#!/usr/bin/env python3
"""
Case Individual Processor
=========================

Professional GeoJSON processor for case files with comprehensive data validation, duplicate detection, and centralized output generation.

Features:
- FTTB code validation and duplicate detection
- Empty field filtering based on required fields
- Individual file processing with compact JSON formatting
- Centralized output with manifest generation
- Professional error handling and logging

Author: Savin Ionut Razvan
Version: 2025.10.05
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

# Add src to path for imports
if str(Path(__file__).parent / "src") not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.engine import GeoJSONProcessor, ProcessingResult
from src.utils.exceptions import FileProcessingError
from src.utils.logger import get_logger, get_performance_logger

@dataclass
class CaseFeature:
    """Represents a processed case feature"""
    feature: Dict[str, Any]
    source_file: str
    processing_timestamp: str

class CaseProcessor:
    """
    Individual processor for case files with standardized headers
    """
    
    def __init__(self, enable_duplicate_detection: bool = True):
        """Initialize the case processor"""
        self.processor = GeoJSONProcessor()
        self.enable_duplicate_detection = enable_duplicate_detection
        self.centralized_data = []  # List of CaseFeature
        self.duplicate_tracking = set()
        self.fttb_code_tracking = set()  # Track FTTB codes specifically
        self.duplicate_stats = {
            "total_duplicates_skipped": 0,
            "duplicates_by_file": {},
            "fttb_code_duplicates": 0
        }
        self.logger = get_logger(__name__)
        self.performance_logger = get_performance_logger()
        
    def _generate_feature_hash(self, feature: Dict[str, Any]) -> str:
        """Generate a unique hash for a feature based on FTTB code and location"""
        import hashlib
        
        # For Case, the primary uniqueness is based on COD_FTTB + DENUMIRE_ART + NR_ART
        # This ensures we don't have duplicate FTTB codes in the same building/art
        key_fields = ["COD_FTTB", "DENUMIRE_ART", "NR_ART"]
        
        # Extract key values - ensure uppercase field names for consistency
        properties = feature.get("properties", {})
        key_values = []
        for field in key_fields:
            field_upper = field.upper()
            if field_upper in properties:
                key_values.append(f"{field_upper}:{properties[field_upper]}")
            elif field in properties:
                key_values.append(f"{field}:{properties[field]}")
        
        # Combine key values for Case uniqueness
        combined = "|".join(sorted(key_values))
        
        # Generate hash
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def _is_duplicate_feature(self, feature: Dict[str, Any]) -> bool:
        """Check if a feature is a duplicate or has invalid data"""
        # First check if feature has valid FTTB data
        properties = feature.get('properties', {})
        cod_fttb = properties.get('COD_FTTB', '').strip()
        denumire_art = properties.get('DENUMIRE_ART', '').strip()
        nr_art = properties.get('NR_ART', '').strip()
        
        # Skip features with empty or invalid FTTB codes
        if not cod_fttb or cod_fttb == '':
            self.logger.debug(f"Skipping feature with empty COD_FTTB: {properties}")
            return True
            
        # Skip features with FTTB codes that are not exactly 7 characters
        if len(cod_fttb) != 7:
            self.logger.debug(f"Skipping feature with invalid COD_FTTB length ({len(cod_fttb)} chars): {cod_fttb}")
            return True
            
        if not denumire_art or denumire_art == '':
            self.logger.debug(f"Skipping feature with empty DENUMIRE_ART: {properties}")
            return True
            
        if not nr_art or nr_art == '':
            self.logger.debug(f"Skipping feature with empty NR_ART: {properties}")
            return True
        
        # Check for FTTB code duplicates specifically
        fttb_key = f"{cod_fttb}|{denumire_art}|{nr_art}"
        if fttb_key in self.fttb_code_tracking:
            self.logger.debug(f"Skipping duplicate FTTB code: {cod_fttb} in {denumire_art} {nr_art}")
            self.duplicate_stats["fttb_code_duplicates"] += 1
            self.duplicate_stats["total_duplicates_skipped"] += 1
            return True
        
        # Add to FTTB code tracking
        self.fttb_code_tracking.add(fttb_key)
        
        # Then check for general duplicates
        if not self.enable_duplicate_detection:
            return False
            
        feature_hash = self._generate_feature_hash(feature)
        
        if feature_hash in self.duplicate_tracking:
            self.duplicate_stats["total_duplicates_skipped"] += 1
            return True
            
        # Add to tracking set
        self.duplicate_tracking.add(feature_hash)
        return False
    
    
    def _process_loaded_data(self, data: Dict[str, Any], file_path: str) -> ProcessingResult:
        """Process already loaded data with case model"""
        import time
        start_time = time.time()
        
        try:
            features = data.get('features', [])
            if not features:
                return ProcessingResult(
                    success=True,
                    model_detected="case",
                    features_processed=0,
                    features_extracted=0,
                    errors=[],
                    warnings=["No features found"],
                    processing_time=time.time() - start_time,
                    metadata={'input_file': str(file_path)}
                )
            
            # Process with case model
            processed_features = []
            errors = []
            warnings = []
            
            for feature in features:
                try:
                    # Extract fields according to case model
                    properties = feature.get('properties', {})
                    extracted_data = self.processor.model_manager.extract_fields("case", properties)
                    
                    # Create processed feature
                    processed_feature = {
                        'type': feature.get('type'),
                        'properties': extracted_data,
                        'geometry': feature.get('geometry')
                    }
                    processed_features.append(processed_feature)
                    
                except Exception as e:
                    errors.append(f"Feature processing error: {str(e)}")
                    continue
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                success=True,
                model_detected="case",
                features_processed=len(features),
                features_extracted=len(processed_features),
                errors=errors,
                warnings=warnings,
                processing_time=processing_time,
                metadata={
                    'input_file': str(file_path),
                    'output_data': {'features': processed_features},
                    'processing_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                model_detected="case",
                features_processed=0,
                features_extracted=0,
                errors=[str(e)],
                warnings=[],
                processing_time=time.time() - start_time,
                metadata={'input_file': str(file_path), 'error': str(e)}
            )

    def process_file(self, file_path: str, output_dir: str) -> ProcessingResult:
        """Process a single case file"""
        self.logger.info(f"Processing case file: {file_path}")
        
        try:
            # Check if file has CASE_ in the name
            file_name = Path(file_path).name
            if "CASE_" not in file_name.upper():
                self.logger.warning(f"File {file_path} does not contain 'CASE_' in name, skipping")
                return ProcessingResult(
                    success=False,
                    model_detected="case",
                    features_processed=0,
                    features_extracted=0,
                    errors=["File does not contain 'CASE_' in name"],
                    warnings=[],
                    processing_time=0.0,
                    metadata={"error_message": "File does not contain 'CASE_' in name"}
                )
            
            # Try different encodings to handle various file formats
            encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252', 'cp1252']
            data = None
            
            for encoding in encodings_to_try:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        data = json.load(f)
                    self.logger.debug(f"Successfully read {file_path} with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
                except json.JSONDecodeError:
                    continue
            
            if data is None:
                raise FileProcessingError(f"Could not read {file_path} with any supported encoding")
            
            # Process the loaded data
            result = self._process_loaded_data(data, file_path)
            
            if not result.success:
                self.logger.error(f"Failed to process {file_path}: {result.errors}")
                return result
            
            # Check if it's a case file
            if result.model_detected != "case":
                self.logger.warning(f"File {file_path} is not a case file (detected: {result.model_detected})")
                return result
            
            # Get processed features from metadata
            output_data = result.metadata.get('output_data', {})
            features = output_data.get('features', [])
            
            # Filter out duplicates and empty properties
            filtered_features = []
            empty_features_skipped = 0
            
            for feature in features:
                # Skip features with empty properties
                properties = feature.get('properties', {})
                if not properties or len(properties) == 0:
                    self.logger.debug(f"Skipping feature with empty properties: {feature}")
                    empty_features_skipped += 1
                    continue
                
                # Check if required fields for case are empty
                has_required_values = False
                empty_required_fields = []
                for field in ["COD_FTTB", "DENUMIRE_ART", "NR_ART", "STARE_RETEA", "ZONA_RETEA", "TIP_ECHIPAMENT"]:
                    value = properties.get(field, '')
                    if value is not None and value != "" and value != [] and value != {}:
                        has_required_values = True
                        break
                    else:
                        empty_required_fields.append(f"{field}='{value}'")
                
                if not has_required_values:
                    self.logger.debug(f"Skipping feature with empty required fields for case: {', '.join(empty_required_fields)}")
                    empty_features_skipped += 1
                    continue
                
                if not self._is_duplicate_feature(feature):
                    filtered_features.append(feature)
                else:
                    # Track duplicates by file
                    file_name = Path(file_path).name
                    if file_name not in self.duplicate_stats["duplicates_by_file"]:
                        self.duplicate_stats["duplicates_by_file"][file_name] = 0
                    self.duplicate_stats["duplicates_by_file"][file_name] += 1
            
            # Create case folder in output directory
            case_output_dir = Path(output_dir) / "case"
            case_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create output file (keep original name for case files)
            output_file = case_output_dir / f"{Path(file_path).stem}.geojson"
            
            # Save individual file with compact formatting (same as scari)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('{\n')
                f.write('"type": "FeatureCollection",\n')
                f.write(f'"name": "Processed Case - {Path(file_path).stem}",\n')
                f.write('"features": [\n')
                
                # Write features in compact format
                for i, feature in enumerate(filtered_features):
                    try:
                        # Create compact feature string with proper JSON escaping
                        properties = feature.get("properties", {})
                        
                        # Ensure all property keys are uppercase
                        uppercase_properties = {}
                        for key, value in properties.items():
                            uppercase_properties[key.upper()] = value
                        
                        # Create compact feature
                        feature_str = '{ "type": "Feature", "properties": '
                        feature_str += json.dumps(uppercase_properties, separators=(',', ':'), ensure_ascii=False)
                        feature_str += ', "geometry": '
                        
                        # Add geometry
                        geometry = feature.get("geometry", {})
                        if geometry:
                            geometry_str = json.dumps(geometry, separators=(',', ':'), ensure_ascii=False)
                        else:
                            geometry_str = '{"type": "Point", "coordinates": [0, 0]}'
                        
                        feature_str += geometry_str + ' }'
                        
                        # Add comma if not last feature
                        if i < len(filtered_features) - 1:
                            feature_str += ','
                        
                        f.write(feature_str + '\n')
                        
                    except Exception as e:
                        self.logger.warning(f"Failed to process case feature: {e}")
                        continue
                
                f.write(']\n')
                f.write('}\n')
            
            # Add to centralized data
            for feature in filtered_features:
                centralized_feature = CaseFeature(
                    feature=feature,
                    source_file=Path(file_path).name,
                    processing_timestamp=result.metadata.get('processing_timestamp', '')
                )
                self.centralized_data.append(centralized_feature)
            
            self.logger.info(f"Processed {file_path}: {len(filtered_features)} features, {len(features) - len(filtered_features)} duplicates skipped, {empty_features_skipped} empty features skipped")
            
            return ProcessingResult(
                success=True,
                model_detected="case",
                features_processed=len(features),
                features_extracted=len(filtered_features),
                errors=[],
                warnings=[],
                processing_time=result.processing_time,
                metadata={
                    "source_file": file_path,
                    "output_file": str(output_file),
                    "total_features": len(features),
                    "filtered_features": len(filtered_features),
                    "duplicates_skipped": len(features) - len(filtered_features),
                    "empty_features_skipped": empty_features_skipped,
                    "processing_timestamp": result.metadata.get('processing_timestamp', '')
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            return ProcessingResult(
                success=False,
                model_detected="case",
                features_processed=0,
                features_extracted=0,
                errors=[str(e)],
                warnings=[],
                processing_time=0.0,
                metadata={"error_message": str(e)}
            )
    
    def save_centralized_file(self, output_dir: str) -> str:
        """Save centralized case file in compact format"""
        if not self.centralized_data:
            self.logger.warning("No centralized data to save")
            return ""
        
        # Create case folder in output directory
        case_output_dir = Path(output_dir) / "case"
        case_output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = case_output_dir / "case_centralized.geojson"
        
        # Create centralized GeoJSON in compact format
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('{\n')
            f.write('"type": "FeatureCollection",\n')
            f.write('"name": "Centralized Case Data",\n')
            f.write('"features": [\n')
            
            # Sort entries alphabetically by LOCALITATE
            sorted_entries = sorted(self.centralized_data, key=lambda entry: entry.feature.get("properties", {}).get("LOCALITATE", "").lower())
            
            # Write features in compact format
            for i, entry in enumerate(sorted_entries):
                try:
                    # Create compact feature string with proper JSON escaping
                    properties = entry.feature.get("properties", {})
                    
                    # Ensure all property keys are uppercase
                    uppercase_properties = {}
                    for key, value in properties.items():
                        uppercase_properties[key.upper()] = value
                    
                    # Create compact feature
                    feature_str = '{ "type": "Feature", "properties": '
                    feature_str += json.dumps(uppercase_properties, separators=(',', ':'), ensure_ascii=False)
                    feature_str += ', "geometry": '
                    
                    # Add geometry
                    geometry = entry.feature.get("geometry", {})
                    if geometry:
                        geometry_str = json.dumps(geometry, separators=(',', ':'), ensure_ascii=False)
                    else:
                        geometry_str = '{"type": "Point", "coordinates": [0, 0]}'
                    
                    feature_str += geometry_str + ' }'
                    
                    # Add comma if not last feature
                    if i < len(sorted_entries) - 1:
                        feature_str += ','
                    
                    f.write(feature_str + '\n')
                    
                except Exception as e:
                    self.logger.warning(f"Failed to process case entry: {e}")
                    continue
            
            f.write(']\n')
            f.write('}\n')
        
        self.logger.info(f"Saved centralized case file: {output_file} ({len(self.centralized_data)} features)")
        return str(output_file)
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get processing summary"""
        return {
            "model_type": "case",
            "total_features": len(self.centralized_data),
            "duplicate_stats": self.duplicate_stats,
            "files_processed": len(set(cf.source_file for cf in self.centralized_data)),
            "unique_fttb_codes": len(self.fttb_code_tracking)
        }
    
    def generate_manifest(self, output_dir: str) -> str:
        """Generate manifest.json file for case files"""
        
        output_path = Path(output_dir)
        case_dir = output_path / "case"
        
        if not case_dir.exists():
            self.logger.warning(f"Case directory {case_dir} does not exist, cannot generate manifest")
            return None
        
        # Find all GeoJSON files in the case directory
        geojson_files = list(case_dir.glob("*.geojson"))
        
        if not geojson_files:
            self.logger.warning(f"No GeoJSON files found in {case_dir}")
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
            
            self.logger.info(f"Generated manifest.json with {len(manifest_entries)} entries")
            return str(manifest_file)
            
        except Exception as e:
            self.logger.error(f"Failed to generate manifest.json: {e}")
            return None

def main():
    """Main function for case processing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process case files individually and create centralized output")
    parser.add_argument("input_dir", help="Input directory containing case files")
    parser.add_argument("output_dir", help="Output directory for processed files")
    parser.add_argument("--no-duplicates", action="store_true", help="Disable duplicate detection")
    
    args = parser.parse_args()
    
    processor = CaseProcessor(enable_duplicate_detection=not args.no_duplicates)
    
    # Process all case files
    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"Error: Input directory {input_path} does not exist")
        sys.exit(1)
    
    # Find all GeoJSON files
    geojson_files = list(input_path.rglob("*.geojson"))
    
    if not geojson_files:
        print(f"No GeoJSON files found in {input_path}")
        sys.exit(1)
    
    print(f"Found {len(geojson_files)} GeoJSON files to process")
    
    # Process each file
    processed_count = 0
    for file_path in geojson_files:
        result = processor.process_file(str(file_path), args.output_dir)
        if result.success:
            processed_count += 1
    
    # Save centralized file - DISABLED
    # centralized_file = processor.save_centralized_file(args.output_dir)
    
    # Generate manifest.json
    manifest_file = processor.generate_manifest(args.output_dir)
    
    # Print summary
    summary = processor.get_processing_summary()
    print("\n🎉 Case Processing Complete!")
    print(f"📊 Processed: {processed_count}/{len(geojson_files)} files")
    print(f"🔢 Total features: {summary['total_features']}")
    print(f"🔄 Duplicates skipped: {summary['duplicate_stats']['total_duplicates_skipped']}")
    print(f"🔑 FTTB code duplicates: {summary['duplicate_stats']['fttb_code_duplicates']}")
    print(f"✅ Unique FTTB codes: {summary['unique_fttb_codes']}")
    # if centralized_file:
    #     print(f"📁 Centralized file: {centralized_file}")
    if manifest_file:
        print(f"📋 Manifest file: {manifest_file}")

if __name__ == "__main__":
    main()
