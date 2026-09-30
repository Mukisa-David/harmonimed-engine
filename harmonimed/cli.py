import os
import click
import pandas as pd
from harmonimed.parser import DICOMHarmonizer

@click.group()
def cli():
    """HarmoniMed DICOM Metadata Harmonization Tool"""
    pass

@cli.command()
@click.option("--input-dir", "-i", required=True, type=click.Path(exists=True), help="Path to raw DICOM directory.")
@click.option("--output", "-o", required=True, type=click.Path(), help="Output path (.parquet or .csv).")
@click.option("--schema", "-s", default=None, type=click.Path(), help="Custom YAML schema file.")
def sanitize(input_dir: str, output: str, schema: str):
    """Parses raw DICOM directory, removes PHI, normalizes tags, and exports structured metadata."""
    if schema is None:
        schema = os.path.join(os.path.dirname(__file__), "config", "schema.yaml")

    click.echo(f"Processing DICOM files in {input_dir}...")
    engine = DICOMHarmonizer(schema_path=schema)
    df = engine.process_directory(input_dir)

    if output.endswith(".parquet"):
        df.to_parquet(output, index=False)
    else:
        df.to_csv(output, index=False)

    click.echo(f"Harmonization complete. Processed {len(df)} files -> Exported to {output}")

if __name__ == "__main__":
    cli()