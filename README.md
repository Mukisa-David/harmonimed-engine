# HarmoniMed Engine

An open-source DICOM metadata harmonization and PHI anonymization engine designed for healthcare machine learning pipelines.

## Features
* **PHI Anonymization:** Redacts standard patient identifiers and removes private vendor creator elements.
* **Metadata Harmonization:** Standardizes cross-vendor series descriptions (Siemens, GE, Philips) into uniform ML classes.
* **Schema-Driven Rules:** Customizable YAML config for modality-specific attribute validation.
* **Flexible Export:** Parses DICOM file trees directly into Parquet or CSV feature manifests.

## Live Interactive Demo
Try the live Streamlit web application: [HarmoniMed Live Demo](https://harmonimed-engine.streamlit.app/)

## Quickstart

### Installation
```bash
pip install harmonimed-engine
