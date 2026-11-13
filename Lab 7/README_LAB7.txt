# Lab 7 — Fuzzing for Input Validation Bugs

## Submission files
- `processor.py` — fixed application script (required deliverable)
- `test_processor.py` — Hypothesis fuzz tests and regression tests (required deliverable)
- `reference/processor_original.py` — unchanged original application, retained for reference
- `requirements.txt` — dependencies

## Install and run
```powershell
python -m pip install -r requirements.txt
python -m pytest -v test_processor.py
python processor.py
```

## Defensive behavior
- Invalid dates return `Pass Expiry: INVALID`.
- Invalid, non-finite, negative-drop, or non-positive-distance gradient inputs return `0.0`.
- Unknown or malformed lift zone codes return `0.0`.

## Important evidence note
The handout asks for a PDF containing four screenshots: original application execution,
Hypothesis failures against the original, fixed application execution, and passing tests
against the fixed application. This package includes the required code deliverables,
but it does not fabricate screenshots from the student's computer. Add the genuine
terminal screenshots to the PDF before submitting if your instructor strictly requires
screenshots.
