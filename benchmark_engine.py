import time
import os
from pathlib import Path
from harmonimed.parser import DICOMHarmonizer

def run_benchmark(input_directory: str, output_parquet: str):
    print("=" * 60)
    print("      HarmoniMed Engine Multi-Vendor Benchmark")
    print("=" * 60)
    
    # Track file count
    dicom_files = list(Path(input_directory).rglob("*.dcm"))
    total_files = len(dicom_files)
    
    if total_files == 0:
        print(f"No .dcm files found in {input_directory}. Ensure files are downloaded.")
        return

    print(f"Target Directory : {input_directory}")
    print(f"Total DICOMs     : {total_files} files")
    
    # Initialize Engine with explicit schema path
    schema_file = os.path.join("harmonimed", "config", "schema.yaml")
    engine = DICOMHarmonizer(schema_path=schema_file)
    
    # Start Benchmark Timer
    start_time = time.perf_counter()
    
    # Process Directory
    df = engine.process_directory(input_directory)
    
    # Save Manifest
    df.to_parquet(output_parquet)
    
    elapsed_time = time.perf_counter() - start_time
    fps = total_files / elapsed_time if elapsed_time > 0 else 0
    
    # Summary Output
    print("\nBenchmark Results:")
    print(f"  - Total Elapsed Time   : {elapsed_time:.2f} seconds")
    print(f"  - Processing Throughput: {fps:.2f} DICOMs/sec")
    print(f"  - Manifest Size       : {os.path.getsize(output_parquet) / 1024:.2f} KB")
    print(f"  - Extracted Features  : {len(df.columns)} columns")
    if 'Manufacturer' in df.columns:
        print(f"  - Unique Vendors      : {df['Manufacturer'].unique().tolist()}")
    print("=" * 60)

if __name__ == "__main__":
    run_benchmark("./tcia_benchmarks", "tcia_manifest.parquet")