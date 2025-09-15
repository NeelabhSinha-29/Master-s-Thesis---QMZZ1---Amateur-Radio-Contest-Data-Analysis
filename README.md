# Master-s-Thesis---QMZZ1---Amateur-Radio-Contest-Data-Analysis


Quickstart (build pickles for the main notebook)
1) Requirements

Python 3.10+

pip install -r requirements.txt with at least:

requests
beautifulsoup4
pandas
numpy


(You can add plotting libs later for EDA.)

2) Project folders

Create this minimal structure (exact casing matters):

RepoRoot/
  Data/
    Raw/
      2024 CQ WW CW Contest/
    Pre-Processed/
  Scripts/    # optional, if you want to store .py files here
  Notebooks/  # optional, if your Jupyter notebooks live here

3) Download raw logs (CQ WW CW 2024)

Run:

python crawl_log.py


This crawls the CQWW public logs page and saves each log to:

Data/Raw/2024 CQ WW CW Contest/<CALLSIGN>.txt


(Calls with “/” are safely renamed to “_”.) 

crawl_log

4) Parse logs → make base pickles (header.pickle, logs.pickle)

Run:

python parser_main.py


This:

pulls the list of callsigns from the public logs page,

parses headers & QSO rows for each callsign using the Cabrillo parser, and

writes:

Data/Pre-Processed/header.pickle

Data/Pre-Processed/logs.pickle
(using cabrillo_parser.header_parser and cabrillo_parser.log_parser). 

parser_main

 

cabrillo_parser

5) Build header_updated.pickle

Now create the updated header with QSO_COUNT (and keep logs in upper-case for joins). Run this one-off snippet (as a script or in a small setup notebook):

import pandas as pd
import numpy as np

# Load base pickles
header = pd.read_pickle("Data/Pre-Processed/header.pickle")
logs = pd.read_pickle("Data/Pre-Processed/logs.pickle")

# Clean log callsigns to uppercase (to match consistently)
for c in ["sent_call", "rcvd_call"]:
    logs[c] = logs[c].str.upper()

# Compute QSO_COUNT per header callsign
def count_qsos(callsign: str) -> int:
    return logs.loc[logs["sent_call"].str.upper() == str(callsign).upper()].shape[0]

header["QSO_COUNT"] = header["CALLSIGN"].apply(count_qsos)

# Save updated header
header.to_pickle("Data/Pre-Processed/header_updated.pickle")


(This mirrors the “count + save” step used in your exploratory notebook c
