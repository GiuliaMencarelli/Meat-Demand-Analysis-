# =============================================================================
# HBS Data Extraction
# Author: Giulia Mencarelli
#
# Loads the raw ISTAT Household Budget Survey microdata (2023), selects the
# columns needed for the meat demand analysis, cleans missing value codes,
# and saves the result as a CSV for further preprocessing.
#
# Input:  microdata_2023_ISTAT.xlsx  (raw ISTAT HBS microdata)
# Output: micro_protein_cols.csv
#
# Data source: ISTAT Household Budget Survey (Indagine sulle Spese delle
# Famiglie), available at: https://www.istat.it/  [add direct link]
# =============================================================================

import pandas as pd
import numpy as np

# --- Columns to extract ---
# Household composition and demographics
#   c_Ncmp_*      : household size variables
#   c_relaz_*     : relationship to reference person (up to 12 members)
#   c_c_etacalc_* : age group code for each member (1=child, 2=18-34,
#                   3=35-64, 4=65+)
# Monthly expenditure items
#   d057-d069_mensile : detailed food expenditure categories
# Household-level variables
#   sp_tot_str    : total household expenditure
#   noalm_str     : non-food expenditure
#   d_01          : household size
#   b_01_*        : housing characteristics
#   w_anno        : annual survey weight
#   tipabitaz_new : dwelling type
#   povassc       : poverty indicator
#   rgn           : region code
#   rip           : macro-region code
#   Cod_elenco_d, Anno_d, Mese_d, Cod_periodo_d : survey identifiers

cols = [
    "c_Ncmp_altro", "c_Ncmp_fatto",
    "c_relaz_1",  "c_relaz_2",  "c_relaz_3",  "c_relaz_4",
    "c_relaz_5",  "c_relaz_6",  "c_relaz_7",  "c_relaz_8",
    "c_relaz_9",  "c_relaz_10", "c_relaz_11", "c_relaz_12",
    "c_c_etacalc_1",  "c_c_etacalc_2",  "c_c_etacalc_3",
    "c_c_etacalc_4",  "c_c_etacalc_5",  "c_c_etacalc_6",
    "c_c_etacalc_7",  "c_c_etacalc_8",  "c_c_etacalc_9",
    "c_c_etacalc_10", "c_c_etacalc_11", "c_c_etacalc_12",
    "d057_mensile", "d058_mensile", "d059_mensile", "d060_mensile",
    "d061_mensile", "d062_mensile", "d063_mensile", "d064_mensile",
    "d065_mensile", "d066_mensile", "d067_mensile", "d068_mensile",
    "d069_mensile",
    "sp_tot_str", "d_01",
    "b_01_1_1", "b_01_1_2", "b_01_1_3", "b_01_1_4", "b_01_1_5",
    "b_01_1_6", "b_01_1_7", "b_01_1_8", "b_01_1_9",
    "b_01_2_1", "b_01_2_2", "b_01_2_3", "b_01_2_4", "b_01_2_5",
    "b_01_2_6", "b_01_2_9", "b_01_3_0",
    "noalm_str", "Cod_elenco_d", "Anno_d", "Mese_d", "Cod_periodo_d",
    "w_anno", "tipabitaz_new", "povassc", "rgn", "rip"
]

# --- Load data ---
# Only selected columns are read to keep memory usage low
print("Loading raw HBS microdata...")
micro_aids = pd.read_excel(
    "data/microdata_2023_ISTAT.xlsx",
    usecols=cols,
    engine="openpyxl"
)
print(f"Loaded {len(micro_aids):,} rows and {len(micro_aids.columns)} columns")

# --- Clean missing values ---
# ISTAT encodes missing values as "." in the raw file
micro_aids = micro_aids.replace(".", np.nan)

# --- Convert expenditure and income columns to numeric ---
mensili_cols = [
    c for c in micro_aids.columns
    if c.startswith("d") or c in ["sp_tot_str", "noalm_str"]
]
micro_aids[mensili_cols] = micro_aids[mensili_cols].apply(
    pd.to_numeric, errors="coerce"
)

print(micro_aids.info())

# --- Save output ---
micro_aids.to_csv("micro_protein_cols.csv", index=False)
print("Saved to micro_protein_cols.csv")