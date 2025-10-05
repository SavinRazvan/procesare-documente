#!/usr/bin/env python3
"""
Zone Interventie Individual Processor
=====================================

Professional GeoJSON processor for zone interventie files with comprehensive data validation, duplicate detection, and centralized output generation.

Features:
- Zone Interventie ID validation and duplicate detection
- Empty field filtering based on required fields
- Individual file processing with compact JSON formatting
- Centralized output with professional formatting
- Advanced error handling and performance logging

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
class ZoneInterventieFeature:
    """Represents a processed zone_interventie feature"""
    feature: Dict[str, Any]
    source_file: str
    processing_timestamp: str

class ZoneInterventieProcessor:
    """
    Individual processor for zone_interventie files with standardized headers
    """
    
    def __init__(self, enable_duplicate_detection: bool = True):
        """Initialize the zone_interventie processor"""
        self.processor = GeoJSONProcessor()
        self.enable_duplicate_detection = enable_duplicate_detection
        self.centralized_data = []  # List of ZoneInterventieFeature
        self.duplicate_tracking = set()
        self.duplicate_stats = {
            "total_duplicates_skipped": 0,
            "duplicates_by_file": {}
        }
        self.logger = get_logger(__name__)
        self.performance_logger = get_performance_logger()
        
    def _generate_feature_hash(self, feature: Dict[str, Any]) -> str:
        """Generate a unique hash for a feature based on key values and geometry"""
        import hashlib
        
        # Get key fields for zone_interventie
        key_fields = ["ZONA_INTERVENTIE_ID", "LOCALITATE"]
        
        # Extract key values - ensure uppercase field names for consistency
        properties = feature.get("properties", {})
        key_values = []
        for field in key_fields:
            field_upper = field.upper()
            if field_upper in properties:
                key_values.append(f"{field_upper}:{properties[field_upper]}")
            elif field in properties:
                key_values.append(f"{field}:{properties[field]}")
        
        # Add geometry hash
        geometry = feature.get("geometry", {})
        geometry_str = json.dumps(geometry, sort_keys=True)
        
        # Combine key values and geometry
        combined = "|".join(sorted(key_values)) + "|" + geometry_str
        
        # Generate hash
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def _is_duplicate_feature(self, feature: Dict[str, Any]) -> bool:
        """Check if a feature is a duplicate"""
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
        """Process already loaded data with zone_interventie model"""
        import time
        start_time = time.time()
        
        try:
            features = data.get('features', [])
            if not features:
                return ProcessingResult(
                    success=True,
                    model_detected="zone_interventie",
                    features_processed=0,
                    features_extracted=0,
                    errors=[],
                    warnings=["No features found"],
                    processing_time=time.time() - start_time,
                    metadata={'input_file': str(file_path)}
                )
            
            # Process with zone_interventie model
            processed_features = []
            errors = []
            warnings = []
            
            for feature in features:
                try:
                    # Extract fields according to zone_interventie model
                    properties = feature.get('properties', {})
                    extracted_data = self.processor.model_manager.extract_fields("zone_interventie", properties)
                    
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
                model_detected="zone_interventie",
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
                model_detected="zone_interventie",
                features_processed=0,
                features_extracted=0,
                errors=[str(e)],
                warnings=[],
                processing_time=time.time() - start_time,
                metadata={'input_file': str(file_path), 'error': str(e)}
            )

    def process_file(self, file_path: str, output_dir: str) -> ProcessingResult:
        """Process a single zone_interventie file"""
        self.logger.info(f"Processing zone_interventie file: {file_path}")
        
        try:
            # Check if file has ZONA_ or ZONE_ in the name
            file_name = Path(file_path).name
            if "ZONA_" not in file_name.upper() and "ZONE_" not in file_name.upper():
                self.logger.warning(f"File {file_path} does not contain 'ZONA_' or 'ZONE_' in name, skipping")
                return ProcessingResult(
                    success=False,
                    model_detected="zone_interventie",
                    features_processed=0,
                    features_extracted=0,
                    errors=["File does not contain 'ZONA_' or 'ZONE_' in name"],
                    warnings=[],
                    processing_time=0.0,
                    metadata={"error_message": "File does not contain 'ZONA_' or 'ZONE_' in name"}
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
            
            # Check if it's a zone_interventie file
            if result.model_detected != "zone_interventie":
                self.logger.warning(f"File {file_path} is not a zone_interventie file (detected: {result.model_detected})")
                return result
            
            # Get processed features from metadata
            output_data = result.metadata.get('output_data', {})
            features = output_data.get('features', [])
            
            # Additional validation: Check if features have the required zone interventie fields
            valid_features = []
            for feature in features:
                properties = feature.get('properties', {})
                # Check if feature has the core zone interventie fields
                if (properties.get('ZONA') and properties.get('ECHIPA') and 
                    properties.get('TIP_ECHIPA') and properties.get('LOCALITATE')):
                    valid_features.append(feature)
                else:
                    self.logger.debug(f"Skipping feature without required zone interventie fields: {properties}")
            
            if not valid_features:
                self.logger.warning(f"No valid zone interventie features found in {file_path}")
                return ProcessingResult(
                    success=False,
                    model_detected="zone_interventie",
                    features_processed=len(features),
                    features_extracted=0,
                    errors=["No valid zone interventie features found"],
                    warnings=[],
                    processing_time=result.processing_time,
                    metadata={"error_message": "No valid zone interventie features found"}
                )
            
            # Use only valid features
            features = valid_features
            
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
                
                # Check if required fields for zone_interventie are empty
                has_required_values = False
                empty_required_fields = []
                for field in ["JUDET", "LOCALITATE", "ZONA", "ECHIPA", "TIP_ECHIPA", "MI_PRINX", "DIGI_ID"]:
                    value = properties.get(field, '')
                    if value is not None and value != "" and value != [] and value != {}:
                        has_required_values = True
                        break
                    else:
                        empty_required_fields.append(f"{field}='{value}'")
                
                if not has_required_values:
                    self.logger.debug(f"Skipping feature with empty required fields for zone_interventie: {', '.join(empty_required_fields)}")
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
            
            # No individual file creation - only centralized data collection
            
            # Add to centralized data
            for feature in filtered_features:
                centralized_feature = ZoneInterventieFeature(
                    feature=feature,
                    source_file=Path(file_path).name,
                    processing_timestamp=result.metadata.get('processing_timestamp', '')
                )
                self.centralized_data.append(centralized_feature)
            
            self.logger.info(f"Processed {file_path}: {len(filtered_features)} features, {len(features) - len(filtered_features)} duplicates skipped, {empty_features_skipped} empty features skipped")
            
            return ProcessingResult(
                success=True,
                model_detected="zone_interventie",
                features_processed=len(features),
                features_extracted=len(filtered_features),
                errors=[],
                warnings=[],
                processing_time=result.processing_time,
                metadata={
                    "source_file": file_path,
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
                model_detected="zone_interventie",
                features_processed=0,
                features_extracted=0,
                errors=[str(e)],
                warnings=[],
                processing_time=0.0,
                metadata={"error_message": str(e)}
            )
    
    def save_centralized_file(self, output_dir: str) -> str:
        """Save centralized zone_interventie file in compact format"""
        if not self.centralized_data:
            self.logger.warning("No centralized data to save")
            return ""
        
        output_file = Path(output_dir) / "zone_interventie_centralized.geojson"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create centralized GeoJSON in compact format
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('{\n')
            f.write('"type": "FeatureCollection",\n')
            f.write('"name": "Centralized Zone Interventie Data",\n')
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
                    self.logger.warning(f"Failed to process zone_interventie entry: {e}")
                    continue
            
            f.write(']\n')
            f.write('}\n')
        
        self.logger.info(f"Saved centralized zone_interventie file: {output_file} ({len(self.centralized_data)} features)")
        return str(output_file)
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get processing summary"""
        return {
            "model_type": "zone_interventie",
            "total_features": len(self.centralized_data),
            "duplicate_stats": self.duplicate_stats,
            "files_processed": len(set(cf.source_file for cf in self.centralized_data))
        }

def main():
    """Main function for zone_interventie processing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process zone_interventie files and create centralized output only")
    parser.add_argument("input_dir", help="Input directory containing zone_interventie files")
    parser.add_argument("output_dir", help="Output directory for processed files")
    parser.add_argument("--no-duplicates", action="store_true", help="Disable duplicate detection")
    
    args = parser.parse_args()
    
    processor = ZoneInterventieProcessor(enable_duplicate_detection=not args.no_duplicates)
    
    # Process all zone_interventie files
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
    
    # Save centralized file
    centralized_file = processor.save_centralized_file(args.output_dir)
    
    # Print summary
    summary = processor.get_processing_summary()
    print("\n🎉 Zone Interventie Processing Complete!")
    print(f"📊 Processed: {processed_count}/{len(geojson_files)} files")
    print(f"🔢 Total features: {summary['total_features']}")
    print(f"🔄 Duplicates skipped: {summary['duplicate_stats']['total_duplicates_skipped']}")
    if centralized_file:
        print(f"📁 Centralized file: {centralized_file}")

if __name__ == "__main__":
    main()
