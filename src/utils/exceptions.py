"""
Professional Exception Hierarchy for GeoJSON Processor V2
========================================================

Custom exceptions following professional Python standards with clear error messages
and proper exception chaining.

Features:
- Comprehensive exception hierarchy
- Clear error messages with context
- Proper exception chaining
- Error code support
- Detailed error information
- Professional error handling

Author: Savin Ionut Razvan
Version: 2025.10.05
"""

from typing import Optional, Dict, Any


class GeoJSONProcessorError(Exception):
    """Base exception for all GeoJSON processor errors"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ConfigurationError(GeoJSONProcessorError):
    """Raised when configuration is invalid or missing"""


class ModelError(GeoJSONProcessorError):
    """Raised when model-related operations fail"""


class ValidationError(GeoJSONProcessorError):
    """Raised when data validation fails"""
    
    def __init__(self, message: str, field: str, value: Any, rule: str, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.field = field
        self.value = value
        self.rule = rule


class FileProcessingError(GeoJSONProcessorError):
    """Raised when file processing fails"""
    
    def __init__(self, message: str, file_path: str, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.file_path = file_path


class ModelDetectionError(GeoJSONProcessorError):
    """Raised when model detection fails"""
    
    def __init__(self, message: str, file_path: str, available_fields: list, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.file_path = file_path
        self.available_fields = available_fields


class DataIntegrityError(GeoJSONProcessorError):
    """Raised when data integrity checks fail"""
    
    def __init__(self, message: str, integrity_checks: Dict[str, Any], error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.integrity_checks = integrity_checks


class PluginError(GeoJSONProcessorError):
    """Raised when plugin operations fail"""
    
    def __init__(self, message: str, plugin_name: str, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.plugin_name = plugin_name


class LoggingError(GeoJSONProcessorError):
    """Raised when logging operations fail"""


class PerformanceError(GeoJSONProcessorError):
    """Raised when performance limits are exceeded"""
    
    def __init__(self, message: str, metric: str, limit: Any, actual: Any, error_code: Optional[str] = None):
        super().__init__(message, error_code)
        self.metric = metric
        self.limit = limit
        self.actual = actual
