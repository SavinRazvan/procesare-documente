#!/usr/bin/env python3
"""
Master Synthetic Data Generator - Process All Synthetic Models
=============================================================

Orchestrates individual synthetic data generation for all specialized model processors.
Processes main synthetic models first, then search synthetic models at the end.

Features:
- Two-phase processing: Main models first, then search models
- Preserves all original fields and geometries while anonymizing sensitive data
- Uses deterministic generation based on salt for consistency
- Comprehensive error handling and progress reporting
- Compatible with current processor field structure

Processing Phases:
  PHASE 1 - Main Models:
    - camereta, case, enclosure, fibra, hub, localitati
    - scari, spliter, stalpi, zona_acoperire_hub
    - zona_pon, zona_pon_re_ftth1000, zona_sp, zone_interventie
  
  PHASE 2 - Search Models:
    - search_camereta, search_enclosure, search_fttb, search_scari

Usage:
  python _process_all_synth.py                    # Process all models
  python _process_all_synth.py --main-only        # Process only main models
  python _process_all_synth.py --search-only      # Process only search models
  python _process_all_synth.py --models camereta search_camereta  # Specific models

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
class SyntheticGenerationResult:
    """Result of generating synthetic data for a model type"""
    model_type: str
    success: bool
    features_generated: int
    output_file_created: bool
    processing_time: float
    error_message: str = ""

class MasterSyntheticProcessor:
    """
    Master processor that orchestrates all synthetic data generation scripts.
    Manages synthetic data creation that matches current processor field structure.
    Creates synthetic data compatible with real data processors.
    """
    
    def __init__(self):
        """Initialize the master synthetic processor"""
        self.results = {}
        self.total_processing_time = 0
        
        # Define all synthetic data generators (main models + search models)
        self.synthetic_generators = {
            # Main models - updated to match current processor structure
            "camereta": "_camereta_synth_data.py",
            "case": "_case_synth_all.py", 
            "enclosure": "_enclosure_synth_data.py",
            "fibra": "_fibra_synth_data.py",
            "hub": "_hub_synth_data.py",
            "localitati": "_localitati_synth_data.py",
            "scari": "_scari_synth_data.py",
            "spliter": "_spliter_synth_data.py",
            "stalpi": "_stalpi_synth_data.py",
            "zona_acoperire_hub": "_zona_acoperire_hub_synth_data.py",
            "zona_pon": "_zona_pon_synth_data.py",
            "zona_pon_re_ftth1000": "_zona_pon_re_ftth1000_synth_data.py",
            "zona_sp": "_zona_sp_synth_data.py",
            "zone_interventie": "_zone_interventie_synth_data.py",
            
            # Search models
            "search_camereta": "_search_camereta_synth_data.py",
            "search_enclosure": "_search_enclosure_synth_data.py",
            "search_fttb": "_search_fttb_synth_data.py",
            "search_scari": "_search_scari_synth_data.py"
        }
    
    def generate_synthetic_data(self, model_type: str) -> SyntheticGenerationResult:
        """Generate synthetic data for a specific model type"""
        if model_type not in self.synthetic_generators:
            return SyntheticGenerationResult(
                model_type=model_type,
                success=False,
                features_generated=0,
                output_file_created=False,
                processing_time=0,
                error_message=f"Unknown model type: {model_type}"
            )
        
        generator_script = self.synthetic_generators[model_type]
        start_time = time.time()
        
        try:
            # Build command to run the synthetic data generator
            cmd = [sys.executable, generator_script]
            
            # Run the synthetic data generator
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
                features_generated = 0
                output_file_created = False
                
                for line in output_lines:
                    if "Generated" in line and "features" in line:
                        try:
                            # Extract number from "✅ Generated X synthetic features"
                            parts = line.split()
                            for part in parts:
                                if part.isdigit():
                                    features_generated = int(part)
                                    break
                        except:
                            pass
                    elif "Wrote synthetic" in line or "📁 Wrote" in line:
                        output_file_created = True
                
                return SyntheticGenerationResult(
                    model_type=model_type,
                    success=True,
                    features_generated=features_generated,
                    output_file_created=output_file_created,
                    processing_time=processing_time
                )
            else:
                return SyntheticGenerationResult(
                    model_type=model_type,
                    success=False,
                    features_generated=0,
                    output_file_created=False,
                    processing_time=processing_time,
                    error_message=result.stderr or result.stdout
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            return SyntheticGenerationResult(
                model_type=model_type,
                success=False,
                features_generated=0,
                output_file_created=False,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    def generate_all_synthetic_data(self, models: List[str] = None) -> Dict[str, SyntheticGenerationResult]:
        """Generate synthetic data for all specified models"""
        if models is None:
            models = list(self.synthetic_generators.keys())
        
        print(f"🚀 Starting synthetic data generation for {len(models)} model types...")
        print(f"📁 Output directory: _synthetic_data/data/_synth_output")
        print("🔄 Generating data compatible with current processor structure")
        print("=" * 80)
        
        start_time = time.time()
        
        # Separate main models from search models
        main_models = [m for m in models if not m.startswith("search_")]
        search_models = [m for m in models if m.startswith("search_")]
        
        # Process main models first
        if main_models:
            print(f"\n📋 PHASE 1: Processing {len(main_models)} main synthetic models...")
            print("-" * 60)
            
            for i, model_type in enumerate(main_models, 1):
                print(f"\n[{i}/{len(main_models)}] Generating synthetic data for {model_type}...")
                
                result = self.generate_synthetic_data(model_type)
                self.results[model_type] = result
                
                if result.success:
                    print(f"✅ {model_type}: {result.features_generated} features generated ({result.processing_time:.2f}s)")
                else:
                    print(f"❌ {model_type}: Failed - {result.error_message}")
        
        # Process search models at the end
        if search_models:
            print(f"\n📋 PHASE 2: Processing {len(search_models)} search synthetic models...")
            print("-" * 60)
            
            for i, model_type in enumerate(search_models, 1):
                print(f"\n[{i}/{len(search_models)}] Generating synthetic data for {model_type}...")
                
                result = self.generate_synthetic_data(model_type)
                self.results[model_type] = result
                
                if result.success:
                    print(f"✅ {model_type}: {result.features_generated} features generated ({result.processing_time:.2f}s)")
                else:
                    print(f"❌ {model_type}: Failed - {result.error_message}")
        
        self.total_processing_time = time.time() - start_time
        
        # Print final summary
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        """Print synthetic data generation summary"""
        print("\n" + "=" * 80)
        print("🎉 SYNTHETIC DATA GENERATION COMPLETE - SUMMARY")
        print("=" * 80)
        
        successful_models = [r for r in self.results.values() if r.success]
        failed_models = [r for r in self.results.values() if not r.success]
        
        # Separate main and search models for summary
        main_successful = [r for r in successful_models if not r.model_type.startswith("search_")]
        search_successful = [r for r in successful_models if r.model_type.startswith("search_")]
        main_failed = [r for r in failed_models if not r.model_type.startswith("search_")]
        search_failed = [r for r in failed_models if r.model_type.startswith("search_")]
        
        print(f"📊 Total models: {len(self.results)}")
        print(f"✅ Successful: {len(successful_models)}")
        print(f"❌ Failed: {len(failed_models)}")
        print(f"⏱️  Total time: {self.total_processing_time:.2f}s")
        
        if successful_models:
            total_features = sum(r.features_generated for r in successful_models)
            output_files = sum(1 for r in successful_models if r.output_file_created)
            
            print(f"🔢 Total synthetic features generated: {total_features}")
            print(f"📁 Output files created: {output_files}")
            
            # Show breakdown by phase
            if main_successful:
                print(f"\n📋 PHASE 1 - Main Models ({len(main_successful)} successful):")
                for result in main_successful:
                    print(f"  - {result.model_type}: {result.features_generated} features")
            
            if search_successful:
                print(f"\n📋 PHASE 2 - Search Models ({len(search_successful)} successful):")
                for result in search_successful:
                    print(f"  - {result.model_type}: {result.features_generated} features")
        
        if failed_models:
            print("\n❌ Failed models:")
            if main_failed:
                print("  Main Models:")
                for result in main_failed:
                    print(f"    - {result.model_type}: {result.error_message}")
            if search_failed:
                print("  Search Models:")
                for result in search_failed:
                    print(f"    - {result.model_type}: {result.error_message}")
        
        print("=" * 80)
        print("💡 Next steps:")
        print("  1. Verify generated files in _synthetic_data/data/_synth_output/")
        print("  2. Test with real processors to ensure compatibility")
        print("  3. Use synthetic data for development and testing")

def main():
    """Main function for generating synthetic data for all models"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic data for all model types compatible with current processor structure")
    parser.add_argument("--models", nargs="+", help="Specific models to generate (default: all)")
    parser.add_argument("--main-only", action="store_true", help="Generate only main models (exclude search models)")
    parser.add_argument("--search-only", action="store_true", help="Generate only search models")
    
    args = parser.parse_args()
    
    # Initialize processor
    processor = MasterSyntheticProcessor()
    
    # Determine which models to process
    models_to_process = None
    if args.models:
        models_to_process = args.models
    elif args.main_only:
        models_to_process = [k for k in processor.synthetic_generators.keys() if not k.startswith("search_")]
    elif args.search_only:
        models_to_process = [k for k in processor.synthetic_generators.keys() if k.startswith("search_")]
    
    # Generate synthetic data
    results = processor.generate_all_synthetic_data(models_to_process)
    
    # Exit with error code if any models failed
    failed_count = sum(1 for r in results.values() if not r.success)
    if failed_count > 0:
        print(f"\n⚠️  {failed_count} model(s) failed. Check error messages above.")
        sys.exit(1)
    else:
        print(f"\n🎉 All {len(results)} models processed successfully!")

if __name__ == "__main__":
    main()
