"""
Dynamic Model Manager
=====================

Professional configuration-driven model management system with plugin support,
dynamic model loading, and extensible architecture.

Features:
- Dynamic model configuration loading
- Model detection and field extraction
- Plugin support for custom validators
- Model statistics and performance tracking
- Export/import model configurations
- Extensible validation rules

Author: Savin Ionut Razvan
Version: 2025.10.05
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from ..utils.exceptions import ConfigurationError, ModelError
    from ..utils.logger import get_logger
except ImportError:
    # Handle direct imports when running from main.py
    from utils.exceptions import ConfigurationError, ModelError
    from utils.logger import get_logger


class ModelLayer(Enum):
    """Model layer enumeration"""
    MAIN = "main"
    SEARCH = "search"


@dataclass
class ModelInfo:
    """Model information data class"""
    name: str
    layer: ModelLayer
    description: str
    required_fields: List[str]
    extract_fields: List[str]
    field_mappings: Dict[str, Any]
    plugin_name: Optional[str] = None


class ModelManager:
    """
    Dynamic model manager with configuration-driven model loading and plugin support.
    """
    
    def __init__(self, config_path: str = "config/models.json"):
        self.config_path = Path(config_path)
        self.models: Dict[str, ModelInfo] = {}
        self.plugins: Dict[str, Any] = {}
        self.logger = get_logger(__name__)
        
        self._load_models()
    
    def _load_models(self):
        """Load models from configuration file"""
        try:
            if not self.config_path.exists():
                raise ConfigurationError(f"Model configuration file not found: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            models_config = config_data.get('models', {})
            
            for model_id, model_config in models_config.items():
                model_info = self._create_model_info(model_id, model_config)
                self.models[model_id] = model_info
                self.logger.info(f"Loaded model: {model_id} ({model_info.name})")
            
            self.logger.info(f"Successfully loaded {len(self.models)} models")
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load models: {str(e)}")
    
    def _create_model_info(self, model_id: str, model_config: Dict[str, Any]) -> ModelInfo:
        """Create ModelInfo from configuration"""
        try:
            layer = ModelLayer(model_config.get('layer', 'custom'))
            
            return ModelInfo(
                name=model_config.get('name', model_id),
                layer=layer,
                description=model_config.get('description', ''),
                required_fields=model_config.get('required_fields', []),
                extract_fields=model_config.get('extract_fields', []),
                field_mappings=model_config.get('field_mappings', {}),
                plugin_name=model_config.get('plugin_name')
            )
        except Exception as e:
            raise ConfigurationError(f"Invalid model configuration for {model_id}: {str(e)}")
    
    def get_model(self, model_id: str) -> Optional[ModelInfo]:
        """Get model by ID"""
        return self.models.get(model_id)
    
    def get_models_by_layer(self, layer: ModelLayer) -> Dict[str, ModelInfo]:
        """Get all models for a specific layer"""
        return {model_id: model_info for model_id, model_info in self.models.items() 
                if model_info.layer == layer}
    
    def get_all_models(self) -> Dict[str, ModelInfo]:
        """Get all models"""
        return self.models.copy()
    
    def detect_model(self, file_fields: List[str]) -> Optional[str]:
        """
        Detect model based on file fields using header matching.
        Returns the first model with 100% required field match.
        
        Args:
            file_fields: List of field names from the file
            
        Returns:
            Model ID if detected, None otherwise
        """
        file_fields_set = set(field.upper() for field in file_fields)
        
        for model_id, model_info in self.models.items():
            required_fields = set(field.upper() for field in model_info.required_fields)
            
            # Check if all required fields are present (100% match)
            if required_fields.issubset(file_fields_set):
                self.logger.info(f"Detected model: {model_id} (100% header match)")
                return model_id
        
        return None
    
    def detect_all_matching_models(self, file_fields: List[str]) -> List[str]:
        """
        Detect ALL models that have 100% required field match.
        Allows multiple models to process the same file.
        
        Args:
            file_fields: List of field names from the file
            
        Returns:
            List of model IDs that match
        """
        file_fields_set = set(field.upper() for field in file_fields)
        matching_models = []
        
        for model_id, model_info in self.models.items():
            required_fields = set(field.upper() for field in model_info.required_fields)
            
            # Check if all required fields are present (100% match)
            if required_fields.issubset(file_fields_set):
                matching_models.append(model_id)
                self.logger.info(f"Model match: {model_id} (100% header match)")
        
        if matching_models:
            self.logger.info(f"Found {len(matching_models)} matching models: {matching_models}")
        
        return matching_models
    
    def validate_model_data(self, model_id: str, data: Dict[str, Any]) -> bool:
        """
        Validate data against model requirements.
        
        Args:
            model_id: Model ID to validate against
            data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        model_info = self.get_model(model_id)
        if not model_info:
            return False
        
        # Check required fields
        for field in model_info.required_fields:
            if field not in data or data[field] is None or data[field] == '':
                return False
        
        return True
    
    def extract_fields(self, model_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract fields according to model configuration.
        
        Args:
            model_id: Model ID
            data: Source data
            
        Returns:
            Extracted fields dictionary
        """
        model_info = self.get_model(model_id)
        if not model_info:
            raise ModelError(f"Model not found: {model_id}")
        
        extracted = {}
        for field in model_info.extract_fields:
            if field in data:
                extracted[field] = data[field]
        
        return extracted
    
    def add_custom_model(self, model_id: str, model_config: Dict[str, Any]):
        """
        Add a custom model dynamically.
        
        Args:
            model_id: Unique model identifier
            model_config: Model configuration
        """
        try:
            model_info = self._create_model_info(model_id, model_config)
            self.models[model_id] = model_info
            self.logger.info(f"Added custom model: {model_id}")
        except Exception as e:
            raise ModelError(f"Failed to add custom model {model_id}: {str(e)}")
    
    def remove_model(self, model_id: str) -> bool:
        """
        Remove a model.
        
        Args:
            model_id: Model ID to remove
            
        Returns:
            True if removed, False if not found
        """
        if model_id in self.models:
            del self.models[model_id]
            self.logger.info(f"Removed model: {model_id}")
            return True
        return False
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Get model statistics"""
        stats = {
            'total_models': len(self.models),
            'models_by_layer': {},
            'models_with_plugins': 0,
            'average_required_fields': 0,
            'average_extract_fields': 0
        }
        
        # Count by layer
        for model_info in self.models.values():
            layer = model_info.layer.value
            stats['models_by_layer'][layer] = stats['models_by_layer'].get(layer, 0) + 1
            
            if model_info.plugin_name:
                stats['models_with_plugins'] += 1
        
        # Calculate averages
        if self.models:
            total_required = sum(len(model.required_fields) for model in self.models.values())
            total_extract = sum(len(model.extract_fields) for model in self.models.values())
            
            stats['average_required_fields'] = total_required / len(self.models)
            stats['average_extract_fields'] = total_extract / len(self.models)
        
        return stats
    
    def export_model_config(self, output_path: str):
        """Export current model configuration to file"""
        try:
            config_data = {
                'version': '2.0',
                'description': 'Exported model configuration',
                'models': {}
            }
            
            for model_id, model_info in self.models.items():
                config_data['models'][model_id] = {
                    'name': model_info.name,
                    'layer': model_info.layer.value,
                    'description': model_info.description,
                    'required_fields': model_info.required_fields,
                    'extract_fields': model_info.extract_fields,
                    'field_mappings': model_info.field_mappings,
                    'plugin_name': model_info.plugin_name
                }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported model configuration to: {output_path}")
            
        except Exception as e:
            raise ConfigurationError(f"Failed to export model configuration: {str(e)}")
    
    def reload_models(self):
        """Reload models from configuration file"""
        self.models.clear()
        self._load_models()
        self.logger.info("Models reloaded from configuration")
