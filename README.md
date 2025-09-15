# CQWW Contest Data Pipeline

This repository contains scripts to crawl, parse, and preprocess amateur radio contest logs (**CQ WW CW 2024**).  
It produces cleaned **header** and **log** tables that can be loaded directly into Jupyter notebooks for exploratory data analysis.

---

## Quickstart

### 1. Requirements
- Python 3.13.2 (confirmed with `!python --version`)
- Install dependencies:


At minimum, the following Python packages are required:
- requests  
- beautifulsoup4  
- pandas  
- numpy  

---

### 2. Project Structure
Create the following directories before running scripts:

RepoRoot/
Data/
Raw/
2024 CQ WW CW Contest/
Pre-Processed/
Scripts/ # optional, store helper .py files here
Notebooks/ # optional, for Jupyter notebooks



---

### 3. Download Raw Logs
Fetch the contest logs from the CQWW public site:

python crawl_log.py


This saves logs to:

Data/Raw/2024 CQ WW CW Contest/<CALLSIGN>.txt


---

### 4. Parse Logs → Base Pickles
Convert raw logs into structured pickles:

python parser_main.py


This generates:

Data/Pre-Processed/header.pickle
Data/Pre-Processed/logs.pickle


---

### 5. Build `header_updated.pickle`
Update the header with QSO counts and save:

import pandas as pd
import numpy as np

Load base pickles
header = pd.read_pickle("Data/Pre-Processed/header.pickle")
logs = pd.read_pickle("Data/Pre-Processed/logs.pickle")

Uppercase calls
for c in ["sent_call", "rcvd_call"]:
logs[c] = logs[c].str.upper()

Compute QSO_COUNT
def count_qsos(callsign: str) -> int:
return logs.loc[logs["sent_call"].str.upper() == str(callsign).upper()].shape

header["QSO_COUNT"] = header["CALLSIGN"].apply(count_qsos)

Save updated header
header.to_pickle("Data/Pre-Processed/header_updated.pickle")


---

## Notes
- If your notebook is in a different folder, adjust paths like `../Data/Pre-Processed/...` accordingly.  
- Re-run **Step 5** if you regenerate `logs.pickle` and need an updated header.  
