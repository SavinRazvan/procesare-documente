"""
GeoJSON Processor V2 - Professional Document Processing System
=============================================================

A modular, configuration-driven system for processing GeoJSON files
with centralized processing capabilities.

Features:
- Modular processor architecture
- Configuration-driven processing
- Centralized output generation
- Professional error handling
- Performance monitoring
- Extensible plugin system

Author: Savin Ionut Razvan
Version: 2025.10.05
"""

__version__ = "2.0.0"
__author__ = "Savin Ionut Razvan"

from .core.engine import GeoJSONProcessor, ProcessingResult
from .utils.exceptions import FileProcessingError
from .utils.logger import get_logger, get_performance_logger

__all__ = [
    "GeoJSONProcessor",
    "ProcessingResult", 
    "FileProcessingError",
    "get_logger",
    "get_performance_logger",
]

