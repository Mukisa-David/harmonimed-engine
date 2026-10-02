Contributing to HarmoniMed Engine

Thank you for your interest in contributing to HarmoniMed Engine! We welcome contributions from developers, clinical data scientists, and medical imaging researchers.

This document provides a set of guidelines and steps for contributing code, extending DICOM schema rules, and submitting pull requests (PRs).

Code of Conduct

By participating in this project, you agree to maintain a welcoming, inclusive, and respectful environment for all contributors.

How to Contribute

1. Extending DICOM Harmonization Schema Rules

harmonimed-engine uses a YAML-driven configuration to govern tag sanitization and vendor description normalization. Adding support for new imaging vendors (e.g., Toshiba, Canon, Hitachi) or modalities (e.g., Ultrasound, PET) is one of the most impactful ways to contribute.

To extend harmonization rules:

Open harmonimed/config/schema.yaml.

Locate or create the target section (e.g., phi_tags, vendor_mappings, or modality_rules).

Add your new mapping rules using valid YAML syntax:

vendor_mappings:
  toshiba:
    match_patterns:
      - "TOSHIBA"
      - "CANON_MEDICAL_SYSTEMS"
    normalized_name: "CANON_TOSHIBA"


Add unit test coverage in tests/ verifying that your new schema rule correctly parses sample headers.

2. Development Setup

Follow these steps to set up a local development environment:

Fork the Repository on GitHub and clone your fork locally:

git clone https://github.com/YOUR_USERNAME/harmonimed-engine.git
cd harmonimed-engine


Create a Virtual Environment:

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


Install Dependencies in Editable Mode:

pip install -e ".[dev]"
pip install pytest


3. Running Tests

Before submitting changes, ensure that all unit tests pass locally across the test suite:

pytest tests/


If you are adding new features, include corresponding unit tests under tests/.

4. Submitting a Pull Request (PR)

Create a Feature Branch:

git checkout -b feature/your-feature-name


Commit Your Changes:
Follow conventional commit messages (e.g., feat: add Toshiba CT series mapping, fix: handle missing PatientAge VR).

git commit -m "feat: add Toshiba CT series description harmonization"


Push to Your Fork and Open a PR:

git push origin feature/your-feature-name


Open a Pull Request against the main branch of Mukisa-David/harmonimed-engine.

CI/CD Pipeline Validation:
Your PR will automatically trigger the GitHub Actions workflow to run tests across Python 3.9–3.12. Ensure all automated checks pass.

Questions or Feature Requests?

Feel free to open an issue on GitHub to discuss planned features, report bugs, or request additional vendor schema mappings!