# =============================================================================
# HBS Meat Category Construction
# Author: Giulia Mencarelli
#
# Maps raw ISTAT expenditure codes to labelled meat categories, computes
# budget shares within total meat expenditure, and exports the enriched
# dataset for merging with price data in R.
#
# Input:  micro_protein_cols.csv  (output of 01_hbs_extraction.py)
# Output: micro_identified_proteins.csv
# =============================================================================

import pandas as pd
import numpy as np

# --- Load extracted HBS data ---
micro = pd.read_csv("micro_protein_cols.csv")

# --- Map ISTAT expenditure codes to meat categories ---
# Each key is a descriptive category name; each value is the corresponding
# monthly expenditure variable in the raw HBS microdata
protein_mapping = {
    "ham_and_whole_meat_coldcuts":          "d058_mensile",
    "salami_mortadella_sausages_minced_meat": "d059_mensile",
    "live_animals_for_food":                "d060_mensile",
    "beef":                                 "d061_mensile",
    "pork":                                 "d062_mensile",
    "mutton":                               "d063_mensile",
    "poultry":                              "d064_mensile",
    "other_meats":                          "d065_mensile",
    "dried_salted_smoked_meats":            "d066_mensile",
    "offal":                                "d067_mensile",
    "sausages_and_meat_preparations":       "d068_mensile",
    "tot_carne":                            "b_01_1_2"   # total meat expenditure
}

# --- Create labelled expenditure columns ---
# Missing values are treated as zero expenditure
for new_var, source_var in protein_mapping.items():
    micro[new_var] = pd.to_numeric(micro[source_var], errors="coerce").fillna(0)

# --- Compute budget shares within total meat expenditure ---
# Share = category expenditure / total meat expenditure
# Households with zero total meat expenditure receive a share of 0
for var in protein_mapping:
    if var == "tot_carne":
        continue
    micro[f"w_{var}"] = (
        micro[var]
        .div(micro["tot_carne"])
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

# --- Summary statistics ---
categories = list(protein_mapping.keys())

summary = pd.DataFrame({
    "Category":   categories,
    "Mean (EUR)":  [round(micro[v].mean(), 2) for v in categories],
    "Median (EUR)": [round(micro[v].median(), 2) for v in categories],
    "Share mean":  [
        round(micro[f"w_{v}"].mean(), 3) if v != "tot_carne" else np.nan
        for v in categories
    ]
})
print(summary.to_string(index=False))

# --- Save output ---
micro.to_csv("micro_identified_proteins.csv", index=False)
print("Saved to micro_identified_proteins.csv")