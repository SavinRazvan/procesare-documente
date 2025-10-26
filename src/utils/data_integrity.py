"""
Data Integrity and Validation System
===================================

Professional data integrity checks, validation rules, and quality assurance
with comprehensive validation framework and extensible rules.

Features:
- Comprehensive field validation with custom rules
- Data integrity checks and quality scoring
- Extensible validation framework
- Professional error reporting
- Performance monitoring and statistics
- Custom validator support

Author: Savin Ionut Razvan
Version: 2.1
Date: 26.10.2025
"""

import re
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum

try:
    from .exceptions import ValidationError, DataIntegrityError
except ImportError:
    from exceptions import ValidationError, DataIntegrityError


class ValidationRule(Enum):
    """Validation rule types"""
    REQUIRED = "required"
    TYPE_CHECK = "type_check"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"
    PATTERN = "pattern"
    CUSTOM = "custom"


@dataclass
class ValidationResult:
    """Validation result data class"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    field_results: Dict[str, bool]


class DataValidator:
    """
    Professional data validator with extensible validation rules.
    """
    
    def __init__(self):
        self._custom_validators: Dict[str, Callable] = {}
        self._validation_stats = {
            'total_validations': 0,
            'passed_validations': 0,
            'failed_validations': 0,
            'validation_errors': []
        }
    
    def register_custom_validator(self, name: str, validator_func: Callable):
        """Register a custom validator function"""
        self._custom_validators[name] = validator_func
    
    def validate_field(self, field_name: str, value: Any, rules: Dict[str, Any]) -> bool:
        """
        Validate a single field against rules.
        
        Args:
            field_name: Name of the field
            value: Value to validate
            rules: Validation rules dictionary
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Required field check
            if rules.get('required', False) and (value is None or value == ''):
                raise ValidationError(
                    f"Field '{field_name}' is required but is empty",
                    field_name, value, 'required'
                )
            
            # Skip validation if field is not required and empty
            if not rules.get('required', False) and (value is None or value == ''):
                return True
            
            # Type validation
            if 'type' in rules:
                if not self._validate_type(value, rules['type']):
                    raise ValidationError(
                        f"Field '{field_name}' has invalid type. Expected: {rules['type']}, Got: {type(value).__name__}",
                        field_name, value, 'type_check'
                    )
            
            # String validations
            if isinstance(value, str):
                self._validate_string(field_name, value, rules)
            
            # Numeric validations
            if isinstance(value, (int, float)):
                self._validate_numeric(field_name, value, rules)
            
            # Pattern validation
            if 'pattern' in rules:
                if not re.match(rules['pattern'], str(value)):
                    raise ValidationError(
                        f"Field '{field_name}' does not match required pattern: {rules['pattern']}",
                        field_name, value, 'pattern'
                    )
            
            # Custom validation
            if 'custom_validator' in rules:
                validator_name = rules['custom_validator']
                if validator_name in self._custom_validators:
                    if not self._custom_validators[validator_name](value):
                        raise ValidationError(
                            f"Field '{field_name}' failed custom validation: {validator_name}",
                            field_name, value, 'custom'
                        )
            
            return True
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(
                f"Unexpected validation error for field '{field_name}': {str(e)}",
                field_name, value, 'unknown'
            )
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate data type"""
        type_mapping = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }
        
        expected = type_mapping.get(expected_type)
        if expected is None:
            return True  # Unknown type, skip validation
        
        return isinstance(value, expected)
    
    def _validate_string(self, field_name: str, value: str, rules: Dict[str, Any]):
        """Validate string-specific rules"""
        if 'min_length' in rules and len(value) < rules['min_length']:
            raise ValidationError(
                f"Field '{field_name}' is too short. Minimum length: {rules['min_length']}",
                field_name, value, 'min_length'
            )
        
        if 'max_length' in rules and len(value) > rules['max_length']:
            raise ValidationError(
                f"Field '{field_name}' is too long. Maximum length: {rules['max_length']}",
                field_name, value, 'max_length'
            )
    
    def _validate_numeric(self, field_name: str, value: Union[int, float], rules: Dict[str, Any]):
        """Validate numeric-specific rules"""
        if 'min_value' in rules and value < rules['min_value']:
            raise ValidationError(
                f"Field '{field_name}' is too small. Minimum value: {rules['min_value']}",
                field_name, value, 'min_value'
            )
        
        if 'max_value' in rules and value > rules['max_value']:
            raise ValidationError(
                f"Field '{field_name}' is too large. Maximum value: {rules['max_value']}",
                field_name, value, 'max_value'
            )
    
    def validate_model_data(self, data: Dict[str, Any], model_config: Dict[str, Any]) -> ValidationResult:
        """
        Validate data against model configuration.
        
        Args:
            data: Data to validate
            model_config: Model configuration with field mappings
            
        Returns:
            ValidationResult with validation status and details
        """
        errors = []
        warnings = []
        field_results = {}
        
        field_mappings = model_config.get('field_mappings', {})
        
        # Validate required fields
        required_fields = model_config.get('required_fields', [])
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                errors.append(f"Required field '{field}' is missing or empty")
                field_results[field] = False
        
        # Validate each field
        for field_name, value in data.items():
            if field_name in field_mappings:
                rules = field_mappings[field_name]
                try:
                    is_valid = self.validate_field(field_name, value, rules)
                    field_results[field_name] = is_valid
                except ValidationError as e:
                    errors.append(str(e))
                    field_results[field_name] = False
        
        # Check for unknown fields
        known_fields = set(field_mappings.keys())
        unknown_fields = set(data.keys()) - known_fields
        if unknown_fields:
            warnings.append(f"Unknown fields found: {', '.join(unknown_fields)}")
        
        is_valid = len(errors) == 0
        
        # Update statistics
        self._validation_stats['total_validations'] += 1
        if is_valid:
            self._validation_stats['passed_validations'] += 1
        else:
            self._validation_stats['failed_validations'] += 1
            self._validation_stats['validation_errors'].extend(errors)
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            field_results=field_results
        )
    
    def check_data_integrity(self, data: List[Dict[str, Any]], model_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive data integrity checks.
        
        Args:
            data: List of data records
            model_config: Model configuration
            
        Returns:
            Integrity check results
        """
        integrity_results = {
            'total_records': len(data),
            'valid_records': 0,
            'invalid_records': 0,
            'duplicate_records': 0,
            'missing_required_fields': 0,
            'data_quality_score': 0.0,
            'field_completeness': {},
            'field_consistency': {},
            'recommendations': []
        }
        
        if not data:
            return integrity_results
        
        # Check field completeness
        field_mappings = model_config.get('field_mappings', {})
        for field_name in field_mappings.keys():
            non_empty_count = sum(1 for record in data if record.get(field_name) not in [None, ''])
            completeness = non_empty_count / len(data)
            integrity_results['field_completeness'][field_name] = completeness
        
        # Check each record
        for record in data:
            validation_result = self.validate_model_data(record, model_config)
            
            if validation_result.is_valid:
                integrity_results['valid_records'] += 1
            else:
                integrity_results['invalid_records'] += 1
                if not all(record.get(field) for field in model_config.get('required_fields', [])):
                    integrity_results['missing_required_fields'] += 1
        
        # Check for duplicates (simple hash-based check)
        record_hashes = set()
        for record in data:
            record_hash = hash(tuple(sorted(record.items())))
            if record_hash in record_hashes:
                integrity_results['duplicate_records'] += 1
            else:
                record_hashes.add(record_hash)
        
        # Calculate data quality score
        total_checks = integrity_results['total_records']
        passed_checks = integrity_results['valid_records']
        integrity_results['data_quality_score'] = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # Generate recommendations
        if integrity_results['data_quality_score'] < 80:
            integrity_results['recommendations'].append("Data quality is below 80%. Review validation errors.")
        
        if integrity_results['duplicate_records'] > 0:
            integrity_results['recommendations'].append(f"Found {integrity_results['duplicate_records']} duplicate records.")
        
        return integrity_results
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return self._validation_stats.copy()
    
    def reset_stats(self):
        """Reset validation statistics"""
        self._validation_stats = {
            'total_validations': 0,
            'passed_validations': 0,
            'failed_validations': 0,
            'validation_errors': []
        }
