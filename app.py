import os
import tempfile
import pandas as pd
import streamlit as st
from harmonimed.parser import DICOMHarmonizer

st.set_page_config(page_title="HarmoniMed Engine Demo", layout="wide")

st.title("HarmoniMed DICOM Engine Demo")
st.write(
    "Upload raw DICOM files to parse, anonymize PHI, and extract harmonized ML feature manifests live."
)

uploaded_files = st.file_uploader(
    "Upload DICOM Files", accept_multiple_files=True, type=["dcm", "dicom"]
)

if uploaded_files:
    with tempfile.TemporaryDirectory() as tmpdir:
        for file in uploaded_files:
            filepath = os.path.join(tmpdir, file.name)
            with open(filepath, "wb") as f:
                f.write(file.getbuffer())

        schema_path = os.path.join("harmonimed", "config", "schema.yaml")
        engine = DICOMHarmonizer(schema_path=schema_path)
        
        with st.spinner("Processing DICOM files and stripping PHI..."):
            df = engine.process_directory(tmpdir)

        st.subheader("Harmonized Metadata Output")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV Manifest",
            data=csv,
            file_name="harmonized_dicom.csv",
            mime="text/csv",
        )