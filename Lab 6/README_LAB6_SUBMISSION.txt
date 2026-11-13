Lab 6 — Code and Branch Coverage

Files:
- ski_resort_pass.py: supplied application under test
- CodeCoverageTest_xxxx_application.py: line/code coverage test suite
- BranchCoverageTest_xxxx_application.py: branch coverage test suite

Run each suite separately from this folder:
  python -m pip install pytest coverage
  coverage erase
  coverage run --branch --source=ski_resort_pass -m pytest -q CodeCoverageTest_xxxx_application.py
  coverage report -m
  coverage erase
  coverage run --branch --source=ski_resort_pass -m pytest -q BranchCoverageTest_xxxx_application.py
  coverage report -m

Capture terminal screenshots of each final report. The two commits must be made
separately after adding the corresponding test file and screenshot.
