# Extracted pipeline related to building/saving header pickle
# Source: Explatory_Data_Analysis.ipynb
# Target region ends at cell 14

# ---- Imports ----
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import maidenhead as mh
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns

# ---- Relevant cells up to target ----

# ---- Cell 2 ----
!pip install maidenhead pandas matplotlib numpy cartopy seaborn

# ---- Cell 3 ----
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import maidenhead as mh
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns

# ---- Cell 4 ----
header = pd.read_pickle("../Data/Pre-Processed/header.pickle")

# ---- Cell 5 ----
logs = pd.read_pickle("../Data/Pre-Processed/logs.pickle")

# ---- Cell 7 ----
header.head()

# ---- Cell 8 ----
header_summary = header.describe(include='all')
print(header_summary)

# ---- Cell 10 ----
logs.head()

# ---- Cell 11 ----
def count_QSO_logs(callsign):
    """
    Count the number of QSO logs for a given callsign.
    """
    return logs[logs['sent_call'] == callsign].shape[0]

print(count_QSO_logs(header['CALLSIGN'][0]))

# ---- Cell 12 ----
# Clean up log data

log_cols_to_upper = ['sent_call', 'rcvd_call']
for col in log_cols_to_upper:
    logs[col] = logs[col].str.upper()

# ---- Cell 14 ----
# DO NOT RUN AGAIN (after doing once) -----
count = []
for callsign in header['CALLSIGN']:
    count.append(count_QSO_logs(callsign))

header['QSO_COUNT'] = count
header_updated = header
header_updated.to_pickle("../Data/Pre-Processed/header_updated.pickle")
