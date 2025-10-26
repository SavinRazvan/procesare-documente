"""
Professional Logging System for GeoJSON Processor V2
====================================================

Centralized logging with structured formatting, multiple handlers, and performance monitoring.
Following the user's preference for Python's built-in logging library.

Features:
- Structured logging with multiple handlers
- Performance monitoring and metrics
- Rotating file logs with size limits
- Console and file output with professional formatting
- Error context logging and statistics
- Extensible logging configuration

Author: Savin Ionut Razvan
Version: 2.1
Date: 26.10.2025
"""

import logging
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

try:
    from .exceptions import LoggingError
except ImportError:
    from exceptions import LoggingError


@dataclass
class LogConfig:
    """Logging configuration data class"""
    level: str = "INFO"
    format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    console_output: bool = True
    file_output: bool = True
    log_directory: str = "logs"
    max_file_size: str = "10MB"
    backup_count: int = 5


class ProfessionalLogger:
    """
    Professional logging system with structured formatting and performance monitoring.
    """
    
    def __init__(self, config: LogConfig):
        self.config = config
        self._setup_logging()
        self._performance_metrics = {}
    
    def _setup_logging(self):
        """Setup professional logging configuration"""
        try:
            # Clear existing handlers
            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Set logging level
            level = getattr(logging, self.config.level.upper(), logging.INFO)
            root_logger.setLevel(level)
            
            # Create formatter
            formatter = logging.Formatter(
                fmt=self.config.format,
                datefmt=self.config.date_format
            )
            
            # Console handler
            if self.config.console_output:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                console_handler.setLevel(level)
                root_logger.addHandler(console_handler)
            
            # File handler
            if self.config.file_output:
                self._setup_file_logging(formatter, level)
            
        except Exception as e:
            raise LoggingError(f"Failed to setup logging: {str(e)}")
    
    def _setup_file_logging(self, formatter: logging.Formatter, level: int):
        """Setup file logging with rotation"""
        try:
            log_dir = Path(self.config.log_directory)
            log_dir.mkdir(exist_ok=True)
            
            # Calculate max file size in bytes
            max_size = self._parse_size(self.config.max_file_size)
            
            # Create rotating file handler
            from logging.handlers import RotatingFileHandler
            
            log_file = log_dir / f"geojson_processor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_size,
                backupCount=self.config.backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            
            root_logger = logging.getLogger()
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            raise LoggingError(f"Failed to setup file logging: {str(e)}")
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string to bytes"""
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance"""
        return logging.getLogger(name)
    
    def log_performance(self, operation: str, duration: float, details: Optional[Dict[str, Any]] = None):
        """Log performance metrics"""
        self._performance_metrics[operation] = {
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        
        logger = self.get_logger('performance')
        logger.info(f"Performance: {operation} completed in {duration:.3f}s")
    
    def log_processing_stats(self, stats: Dict[str, Any]):
        """Log processing statistics"""
        logger = self.get_logger('processing')
        logger.info(f"Processing Statistics: {json.dumps(stats, indent=2)}")
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any]):
        """Log error with additional context"""
        logger = self.get_logger('error')
        logger.error(f"Error: {str(error)} | Context: {json.dumps(context, indent=2)}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        return {
            'metrics': self._performance_metrics,
            'total_operations': len(self._performance_metrics),
            'average_duration': sum(m['duration'] for m in self._performance_metrics.values()) / len(self._performance_metrics) if self._performance_metrics else 0
        }


def setup_logging(config_path: Optional[str] = None) -> ProfessionalLogger:
    """
    Setup professional logging system.
    
    Args:
        config_path: Path to logging configuration file
        
    Returns:
        ProfessionalLogger instance
    """
    if config_path:
        # Load configuration from file
        config = _load_logging_config(config_path)
    else:
        # Use default configuration
        config = LogConfig()
    
    return ProfessionalLogger(config)


def _load_logging_config(config_path: str) -> LogConfig:
    """Load logging configuration from JSON file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        logging_config = config_data.get('logging', {})
        return LogConfig(**logging_config)
        
    except Exception as e:
        raise LoggingError(f"Failed to load logging configuration: {str(e)}")


# Global logger instance
_logger_instance: Optional[ProfessionalLogger] = None


def get_logger(name: str) -> logging.Logger:
    """Get logger instance (singleton pattern)"""
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = setup_logging()
    
    return _logger_instance.get_logger(name)


def get_performance_logger() -> ProfessionalLogger:
    """Get performance logger instance"""
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = setup_logging()
    
    return _logger_instance
