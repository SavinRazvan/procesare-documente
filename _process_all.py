#!/usr/bin/env python3
"""
Master Processor - Process All Models
====================================

Orchestrates individual processing for all 18 specialized model processors.
Creates both individual processed files and centralized output for each model.
Includes data standardization, cleaning, and comprehensive validation.

Author: Savin Ionut Razvan
Version: 2.1
Date: 26.10.2025
"""

import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ProcessingResult:
    """Result of processing a model type"""
    model_type: str
    success: bool
    individual_files_created: int
    centralized_file_created: bool
    total_features: int
    duplicates_skipped: int
    processing_time: float
    error_message: str = ""

class MasterProcessor:
    """
    Master processor that orchestrates all 18 specialized model processors.
    Manages data standardization, cleaning, validation, and duplicate detection.
    Creates centralized output files and individual processed files for each model.
    """
    
    def __init__(self, enable_duplicate_detection: bool = True):
        """Initialize the master processor"""
        self.enable_duplicate_detection = enable_duplicate_detection
        self.results = {}
        self.total_processing_time = 0
        
        # Define all 18 specialized processors (14 main + 4 search)
        self.processors = {
            "camereta": "_camereta.py",
            "enclosure": "_enclosure.py", 
            "hub": "_hub.py",
            "localitati": "_localitati.py",
            "stalpi": "_stalpi.py",
            "zona_hub": "_zona_hub.py",
            "zone_interventie": "_zone_interventie.py",
            "case": "_case.py",
            "spliter": "_spliter.py",
            "zona_pon": "_zona_pon.py",
            "zona_spliter": "_zona_spliter.py",
            "fibra": "_fibra.py",
            "scari": "_scari.py",
            "zona_pon_re_ftth1000": "_zona_pon_re_ftth1000.py",
            "fttb_search": "_fttb_search.py",
            "scari_search": "_scari_search.py",
            "camereta_search": "_camereta_search.py",
            "enclosure_search": "_enclosure_search.py"
        }
    
    def process_model(self, model_type: str, input_dir: str, output_dir: str) -> ProcessingResult:
        """Process a specific model type"""
        if model_type not in self.processors:
            return ProcessingResult(
                model_type=model_type,
                success=False,
                individual_files_created=0,
                centralized_file_created=False,
                total_features=0,
                duplicates_skipped=0,
                processing_time=0,
                error_message=f"Unknown model type: {model_type}"
            )
        
        processor_script = self.processors[model_type]
        start_time = time.time()
        
        try:
            # Build command
            cmd = [
                sys.executable, processor_script,
                input_dir, output_dir
            ]
            
            if not self.enable_duplicate_detection:
                cmd.append("--no-duplicates")
            
            # Run the processor
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            processing_time = time.time() - start_time
            
            if result.returncode == 0:
                # Parse output for statistics
                output_lines = result.stdout.split('\n')
                total_features = 0
                duplicates_skipped = 0
                files_processed = 0
                
                for line in output_lines:
                    if "Total features:" in line:
                        try:
                            total_features = int(line.split(":")[1].strip())
                        except:
                            pass
                    elif "Duplicates skipped:" in line:
                        try:
                            duplicates_skipped = int(line.split(":")[1].strip())
                        except:
                            pass
                    elif "Processed:" in line and "/" in line:
                        try:
                            files_processed = int(line.split(":")[1].strip().split("/")[0].strip())
                        except:
                            pass
                
                return ProcessingResult(
                    model_type=model_type,
                    success=True,
                    individual_files_created=files_processed,
                    centralized_file_created=True,
                    total_features=total_features,
                    duplicates_skipped=duplicates_skipped,
                    processing_time=processing_time
                )
            else:
                return ProcessingResult(
                    model_type=model_type,
                    success=False,
                    individual_files_created=0,
                    centralized_file_created=False,
                    total_features=0,
                    duplicates_skipped=0,
                    processing_time=processing_time,
                    error_message=result.stderr
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                model_type=model_type,
                success=False,
                individual_files_created=0,
                centralized_file_created=False,
                total_features=0,
                duplicates_skipped=0,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    def process_all_models(self, input_dir: str, output_dir: str, models: List[str] = None) -> Dict[str, ProcessingResult]:
        """Process all specified models with data standardization and cleaning"""
        if models is None:
            models = list(self.processors.keys())
        
        print(f"🚀 Starting processing for {len(models)} model types...")
        print(f"📁 Input directory: {input_dir}")
        print(f"📁 Output directory: {output_dir}")
        print(f"🔄 Duplicate detection: {'Enabled' if self.enable_duplicate_detection else 'Disabled'}")
        print("=" * 80)
        
        start_time = time.time()
        
        for i, model_type in enumerate(models, 1):
            print(f"\n[{i}/{len(models)}] Processing {model_type}...")
            
            result = self.process_model(model_type, input_dir, output_dir)
            self.results[model_type] = result
            
            if result.success:
                print(f"✅ {model_type}: {result.individual_files_created} files, {result.total_features} features, {result.duplicates_skipped} duplicates skipped ({result.processing_time:.2f}s)")
            else:
                print(f"❌ {model_type}: Failed - {result.error_message}")
        
        self.total_processing_time = time.time() - start_time
        
        # Print final summary
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        """Print processing summary"""
        print("\n" + "=" * 80)
        print("🎉 PROCESSING COMPLETE - SUMMARY")
        print("=" * 80)
        
        successful_models = [r for r in self.results.values() if r.success]
        failed_models = [r for r in self.results.values() if not r.success]
        
        print(f"📊 Total models: {len(self.results)}")
        print(f"✅ Successful: {len(successful_models)}")
        print(f"❌ Failed: {len(failed_models)}")
        print(f"⏱️  Total time: {self.total_processing_time:.2f}s")
        
        if successful_models:
            total_features = sum(r.total_features for r in successful_models)
            total_duplicates = sum(r.duplicates_skipped for r in successful_models)
            total_files = sum(r.individual_files_created for r in successful_models)
            
            print(f"🔢 Total features processed: {total_features}")
            print(f"🔄 Total duplicates skipped: {total_duplicates}")
            print(f"📁 Total individual files created: {total_files}")
            print(f"📋 Centralized files created: {len(successful_models)}")
        
        if failed_models:
            print("\n❌ Failed models:")
            for result in failed_models:
                print(f"  - {result.model_type}: {result.error_message}")
        
        print("=" * 80)

def main():
    """Main function for processing all 18 specialized models with standardization and cleaning"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process all 18 specialized model types with data standardization, cleaning, and centralized output")
    parser.add_argument("input_dir", help="Input directory containing GeoJSON files")
    parser.add_argument("output_dir", help="Output directory for processed files")
    parser.add_argument("--no-duplicates", action="store_true", help="Disable duplicate detection")
    parser.add_argument("--models", nargs="+", help="Specific models to process (default: all)")
    
    args = parser.parse_args()
    
    # Validate input directory
    input_path = Path(args.input_dir)
    if not input_path.exists():
        print(f"Error: Input directory {input_path} does not exist")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize processor
    processor = MasterProcessor(enable_duplicate_detection=not args.no_duplicates)
    
    # Process all models
    results = processor.process_all_models(
        str(input_path), 
        str(output_path), 
        args.models
    )
    
    # Exit with error code if any models failed
    failed_count = sum(1 for r in results.values() if not r.success)
    if failed_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
