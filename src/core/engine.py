"""
Core Processing Engine
======================

Professional GeoJSON processing engine with comprehensive error handling,
performance monitoring, and extensible architecture.

Features:
- Dynamic model detection and field extraction
- Professional error handling with detailed logging
- Performance monitoring and statistics
- Batch processing capabilities
- Compact GeoJSON output formatting
- Extensible plugin architecture

Author: Savin Ionut Razvan
Version: 2.1 - 26.10.2025
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from ..utils.exceptions import (
        FileProcessingError, ModelDetectionError
    )
    from ..utils.logger import get_logger, get_performance_logger
    from ..utils.data_integrity import DataValidator
    from .model_manager import ModelManager
except ImportError:
    # Handle direct imports when running from main.py
    from utils.exceptions import (
        FileProcessingError, ModelDetectionError
    )
    from utils.logger import get_logger, get_performance_logger
    from utils.data_integrity import DataValidator
    from core.model_manager import ModelManager


@dataclass
class ProcessingResult:
    """Processing result data class"""
    success: bool
    model_detected: Optional[str]
    features_processed: int
    features_extracted: int
    errors: List[str]
    warnings: List[str]
    processing_time: float
    metadata: Dict[str, Any]


@dataclass
class ProcessingStats:
    """Processing statistics data class"""
    total_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    total_features: int = 0
    total_processing_time: float = 0.0
    models_detected: Dict[str, int] = None
    
    def __post_init__(self):
        if self.models_detected is None:
            self.models_detected = {}


class GeoJSONProcessor:
    """
    Core GeoJSON processing engine with professional features.
    """
    
    def __init__(self, config_path: str = "config/models.json", settings_path: str = "config/settings.json"):
        self.config_path = config_path
        self.settings_path = settings_path
        self.logger = get_logger(__name__)
        self.performance_logger = get_performance_logger()
        
        # Initialize components
        self.model_manager = ModelManager(config_path)
        self.validator = DataValidator()
        self.stats = ProcessingStats()
        
        # Load settings
        self._load_settings()
        
        self.logger.info("GeoJSON Processor V2 initialized successfully")
    
    def _load_settings(self):
        """Load processing settings"""
        try:
            settings_path = Path(self.settings_path)
            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self._get_default_settings()
            
            self.logger.info("Settings loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load settings: {str(e)}")
            self.settings = self._get_default_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings"""
        return {
            'processing': {
                'enable_duplicate_detection': True,
                'enable_validation': True,
                'enable_statistics': True,
                'batch_size': 1000,
                'max_workers': 4,
                'timeout_seconds': 300
            },
            'validation': {
                'strict_mode': False,
                'skip_invalid_files': True,
                'log_validation_errors': True
            },
            'output': {
                'preserve_structure': True,
                'create_centralized': False,
                'include_metadata': True,
                'include_statistics': True
            }
        }
    
    def process_file(self, file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> ProcessingResult:
        """
        Process a single GeoJSON file.
        
        Args:
            file_path: Path to input GeoJSON file
            output_path: Path for output file (optional)
            
        Returns:
            ProcessingResult with processing details
        """
        start_time = time.time()
        file_path = Path(file_path)
        
        try:
            self.logger.info(f"Processing file: {file_path}")
            
            # Load GeoJSON data
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict) or 'features' not in data:
                raise FileProcessingError("Invalid GeoJSON format: missing features", str(file_path))
            
            features = data['features']
            if not isinstance(features, list):
                raise FileProcessingError("Invalid GeoJSON format: features must be a list", str(file_path))
            
            # Detect model
            model_detected = self._detect_model_from_features(features)
            if not model_detected:
                raise ModelDetectionError(
                    "No matching model found for file fields",
                    str(file_path),
                    self._get_available_fields(features)
                )
            
            # Process features
            processed_features, errors, warnings = self._process_features(features, model_detected)
            
            # Create output
            output_data = self._create_output_data(data, processed_features, model_detected)
            
            # Save output if path provided
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    self._write_compact_geojson(output_data, f)
                
                self.logger.info(f"Output saved to: {output_path}")
            
            # Update statistics
            processing_time = time.time() - start_time
            self._update_stats(True, len(features), len(processed_features), processing_time, model_detected)
            
            result = ProcessingResult(
                success=True,
                model_detected=model_detected,
                features_processed=len(features),
                features_extracted=len(processed_features),
                errors=errors,
                warnings=warnings,
                processing_time=processing_time,
                metadata={
                    'input_file': str(file_path),
                    'output_file': str(output_path) if output_path else None,
                    'model_info': asdict(self.model_manager.get_model(model_detected)),
                    'output_data': output_data
                }
            )
            
            self.performance_logger.log_performance(
                f"process_file_{file_path.name}",
                processing_time,
                {'features_processed': len(features), 'model': model_detected}
            )
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._update_stats(False, 0, 0, processing_time)
            
            self.logger.error(f"Failed to process file {file_path}: {str(e)}")
            
            return ProcessingResult(
                success=False,
                model_detected=None,
                features_processed=0,
                features_extracted=0,
                errors=[str(e)],
                warnings=[],
                processing_time=processing_time,
                metadata={'input_file': str(file_path), 'error': str(e)}
            )
    
    def _detect_model_from_features(self, features: List[Dict[str, Any]]) -> Optional[str]:
        """Detect model from feature properties"""
        if not features:
            return None
        
        # Get fields from first feature
        first_feature = features[0]
        properties = first_feature.get('properties', {})
        field_names = list(properties.keys())
        
        return self.model_manager.detect_model(field_names)
    
    def _detect_all_matching_models_from_features(self, features: List[Dict[str, Any]]) -> List[str]:
        """Detect ALL matching models from feature properties"""
        if not features:
            return []
        
        # Get fields from first feature
        first_feature = features[0]
        properties = first_feature.get('properties', {})
        field_names = list(properties.keys())
        
        return self.model_manager.detect_all_matching_models(field_names)
    
    def process_file_with_models(self, file_path: str, target_models: List[str]) -> Dict[str, ProcessingResult]:
        """
        Process a file with specific target models.
        Useful for search processors that need to process files with multiple models.
        
        Args:
            file_path: Path to the GeoJSON file
            target_models: List of model IDs to process with
            
        Returns:
            Dictionary mapping model_id to ProcessingResult
        """
        results = {}
        
        for model_id in target_models:
            try:
                result = self.process_file_with_model(file_path, model_id)
                results[model_id] = result
            except Exception as e:
                self.logger.error(f"Error processing {file_path} with model {model_id}: {str(e)}")
                results[model_id] = ProcessingResult(
                    success=False,
                    model_detected=model_id,
                    features_processed=0,
                    features_extracted=0,
                    errors=[str(e)],
                    warnings=[],
                    processing_time=0.0,
                    metadata={'input_file': str(file_path), 'error': str(e)}
                )
        
        return results
    
    def process_file_with_model(self, file_path: str, model_id: str) -> ProcessingResult:
        """
        Process a file with a specific model.
        
        Args:
            file_path: Path to the GeoJSON file
            model_id: Specific model ID to use
            
        Returns:
            ProcessingResult
        """
        start_time = time.time()
        
        try:
            # Load and validate file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data.get('type') != 'FeatureCollection':
                raise FileProcessingError("Invalid GeoJSON: must be FeatureCollection")
            
            features = data.get('features', [])
            if not features:
                return ProcessingResult(
                    success=True,
                    model_detected=model_id,
                    features_processed=0,
                    features_extracted=0,
                    errors=[],
                    warnings=["No features found"],
                    processing_time=time.time() - start_time,
                    metadata={'input_file': str(file_path)}
                )
            
            # Process with specific model
            processed_features = []
            errors = []
            warnings = []
            
            for feature in features:
                try:
                    # Extract fields according to model
                    properties = feature.get('properties', {})
                    extracted_data = self.model_manager.extract_fields(model_id, properties)
                    
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
                model_detected=model_id,
                features_processed=len(features),
                features_extracted=len(processed_features),
                errors=errors,
                warnings=warnings,
                processing_time=processing_time,
                metadata={
                    'input_file': str(file_path),
                    'output_data': {'features': processed_features},
                    'processing_timestamp': datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                model_detected=model_id,
                features_processed=0,
                features_extracted=0,
                errors=[str(e)],
                warnings=[],
                processing_time=time.time() - start_time,
                metadata={'input_file': str(file_path), 'error': str(e)}
            )
    
    def _get_available_fields(self, features: List[Dict[str, Any]]) -> List[str]:
        """Get available fields from features"""
        if not features:
            return []
        
        all_fields = set()
        for feature in features:
            properties = feature.get('properties', {})
            all_fields.update(properties.keys())
        
        return list(all_fields)
    
    def _process_features(self, features: List[Dict[str, Any]], model_id: str) -> tuple:
        """Process features according to model configuration"""
        processed_features = []
        errors = []
        warnings = []
        
        model_info = self.model_manager.get_model(model_id)
        if not model_info:
            errors.append(f"Model not found: {model_id}")
            return processed_features, errors, warnings
        
        for i, feature in enumerate(features):
            try:
                properties = feature.get('properties', {})
                
                # Validate data if enabled
                if self.settings.get('validation', {}).get('enable_validation', True):
                    validation_result = self.validator.validate_model_data(properties, {
                        'required_fields': model_info.required_fields,
                        'field_mappings': model_info.field_mappings
                    })
                    
                    if not validation_result.is_valid:
                        if self.settings.get('validation', {}).get('strict_mode', False):
                            errors.append(f"Feature {i}: Validation failed - {', '.join(validation_result.errors)}")
                            continue
                        else:
                            warnings.append(f"Feature {i}: Validation warnings - {', '.join(validation_result.warnings)}")
                
                # Extract fields
                extracted_properties = self.model_manager.extract_fields(model_id, properties)
                
                # Create processed feature (match original format: properties first, then geometry)
                processed_feature = {
                    'type': feature.get('type', 'Feature'),
                    'properties': extracted_properties,
                    'geometry': feature.get('geometry')
                }
                
                processed_features.append(processed_feature)
                
            except Exception as e:
                error_msg = f"Feature {i}: {str(e)}"
                errors.append(error_msg)
                self.logger.warning(error_msg)
        
        return processed_features, errors, warnings
    
    def _create_output_data(self, original_data: Dict[str, Any], processed_features: List[Dict[str, Any]], model_id: str) -> Dict[str, Any]:
        """Create output GeoJSON data"""
        output_data = {
            'type': original_data.get('type', 'FeatureCollection'),
            'features': processed_features
        }
        
        # Add metadata if enabled
        if self.settings.get('output', {}).get('include_metadata', True):
            output_data['metadata'] = {
                'processed_at': datetime.now().isoformat(),
                'model_detected': model_id,
                'features_count': len(processed_features),
                'processor_version': '2.0'
            }
        
        # Add statistics if enabled
        if self.settings.get('output', {}).get('include_statistics', True):
            output_data['statistics'] = asdict(self.stats)
        
        return output_data
    
    def _update_stats(self, success: bool, features_processed: int, features_extracted: int, processing_time: float, model_detected: Optional[str] = None):
        """Update processing statistics"""
        self.stats.total_files += 1
        
        if success:
            self.stats.successful_files += 1
        else:
            self.stats.failed_files += 1
        
        self.stats.total_features += features_processed
        self.stats.total_processing_time += processing_time
        
        if model_detected:
            self.stats.models_detected[model_detected] = self.stats.models_detected.get(model_detected, 0) + 1
    
    def process_batch(self, input_dir: Union[str, Path], output_dir: Union[str, Path]) -> Dict[str, Any]:
        """
        Process multiple GeoJSON files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            
        Returns:
            Batch processing results
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            raise FileProcessingError(f"Input directory not found: {input_dir}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all GeoJSON files
        geojson_files = list(input_dir.rglob("*.geojson"))
        
        if not geojson_files:
            self.logger.warning(f"No GeoJSON files found in {input_dir}")
            return {'message': 'No files to process', 'processed_files': 0}
        
        self.logger.info(f"Found {len(geojson_files)} GeoJSON files to process")
        
        results = []
        successful = 0
        failed = 0
        
        for file_path in geojson_files:
            try:
                # Create output path preserving directory structure
                relative_path = file_path.relative_to(input_dir)
                output_path = output_dir / relative_path
                
                result = self.process_file(file_path, output_path)
                results.append(result)
                
                if result.success:
                    successful += 1
                else:
                    failed += 1
                
            except Exception as e:
                self.logger.error(f"Failed to process {file_path}: {str(e)}")
                failed += 1
        
        batch_result = {
            'total_files': len(geojson_files),
            'successful_files': successful,
            'failed_files': failed,
            'results': results,
            'statistics': asdict(self.stats)
        }
        
        self.logger.info(f"Batch processing completed: {successful} successful, {failed} failed")
        
        return batch_result
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return asdict(self.stats)
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.stats = ProcessingStats()
        self.logger.info("Processing statistics reset")
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model information"""
        model_info = self.model_manager.get_model(model_id)
        if model_info:
            return asdict(model_info)
        return None
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get all available models"""
        return {model_id: asdict(model_info) for model_id, model_info in self.model_manager.get_all_models().items()}
    
    def _write_compact_geojson(self, data: Dict[str, Any], file_handle) -> None:
        """
        Write GeoJSON in compact format with each feature on its own line.
        Matches the style of search_enclosure.geojson.
        """
        import json
        
        # Write opening
        file_handle.write('{\n"type":"FeatureCollection",\n"features":[\n')
        
        # Write each feature on its own line
        features = data.get('features', [])
        for i, feature in enumerate(features):
            if i > 0:
                file_handle.write(',\n')
            # Write feature as compact JSON on single line
            feature_json = json.dumps(feature, separators=(',', ':'), ensure_ascii=False)
            file_handle.write(feature_json)
        
        # Write closing
        file_handle.write('\n]')
        
        # Add metadata if present
        if 'metadata' in data:
            metadata_json = json.dumps(data['metadata'], separators=(',', ':'), ensure_ascii=False)
            file_handle.write(f',\n"metadata":{metadata_json}')
        
        if 'statistics' in data:
            stats_json = json.dumps(data['statistics'], separators=(',', ':'), ensure_ascii=False)
            file_handle.write(f',\n"statistics":{stats_json}')
        
        file_handle.write('\n}')
