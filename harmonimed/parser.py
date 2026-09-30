import os
from typing import Dict, Any, List
import pydicom
import pandas as pd
import yaml

class DICOMHarmonizer:
    def __init__(self, schema_path: str):
        with open(schema_path, "r") as f:
            self.schema = yaml.safe_load(f)

    def strip_phi(self, ds: pydicom.Dataset) -> pydicom.Dataset:
        """Removes PHI elements and drops all private creator/vendor tags."""
        # Remove vendor private elements (odd group numbers)
        ds.remove_private_tags()
        
        # Redact configured PHI attributes
        for tag_name in self.schema.get("phi_tags_to_anonymize", []):
            if tag_name in ds:
                setattr(ds, tag_name, "ANONYMIZED")
        return ds

    def normalize_series_description(self, raw_desc: str) -> str:
        """Harmonizes vendor-specific series names into uniform ML classes."""
        if not raw_desc:
            return "UNKNOWN"
        
        clean_desc = raw_desc.upper().strip()
        for normalized_category, patterns in self.schema.get("series_description_normalization", {}).items():
            for pattern in patterns:
                if pattern in clean_desc:
                    return normalized_category
        return clean_desc

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parses a single DICOM file into a structured dictionary."""
        try:
            ds = pydicom.dcmread(file_path, stop_before_pixels=True)
            ds = self.strip_phi(ds)

            pixel_spacing = getattr(ds, "PixelSpacing", [None, None])
            raw_series_desc = getattr(ds, "SeriesDescription", "")

            extracted = {
                "file_path": file_path,
                "sop_instance_uid": getattr(ds, "SOPInstanceUID", None),
                "series_instance_uid": getattr(ds, "SeriesInstanceUID", None),
                "study_instance_uid": getattr(ds, "StudyInstanceUID", None),
                "modality": getattr(ds, "Modality", None),
                "manufacturer": getattr(ds, "Manufacturer", "UNKNOWN"),
                "slice_thickness": float(getattr(ds, "SliceThickness", 0.0) or 0.0),
                "pixel_spacing_x": float(pixel_spacing[0]) if pixel_spacing[0] else None,
                "pixel_spacing_y": float(pixel_spacing[1]) if pixel_spacing[1] else None,
                "raw_series_description": raw_series_desc,
                "normalized_series_description": self.normalize_series_description(raw_series_desc),
                "kvp": float(getattr(ds, "KVP", 0.0) or 0.0),
                "rows": int(getattr(ds, "Rows", 0) or 0),
                "columns": int(getattr(ds, "Columns", 0) or 0),
            }
            return extracted
        except Exception as e:
            return {"file_path": file_path, "error": str(e)}

    def process_directory(self, root_dir: str) -> pd.DataFrame:
        """Traverses directory trees and builds a metadata DataFrame."""
        records = []
        for dirpath, _, filenames in os.walk(root_dir):
            for fname in filenames:
                if fname.endswith((".dcm", ".dicom")) or not "." in fname:
                    full_path = os.path.join(dirpath, fname)
                    record = self.parse_file(full_path)
                    records.append(record)
        
        df = pd.DataFrame(records)
        return df