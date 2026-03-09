# =============================================================================
# Price Data Harmonisation Across Provinces
# Author: Giulia Mencarelli
#
# Reads the raw Osservatorio Prezzi data (one Excel sheet per province),
# filters to only the food categories identified in the coverage matrix,
# and reshapes everything into a single long-format dataset with one row
# per province-category-month combination.
#
# Input:  prezzi_oss.xlsx          (manually collected from Osservatorio
#                                   Prezzi; one sheet per province, first
#                                   column = category, remaining columns
#                                   = months)
#         presence_matrix.xlsx     (output of 03_price_coverage_matrix.py)
# Output: all_categories_prices_by_province.xlsx
# =============================================================================

import pandas as pd

# --- Load coverage matrix to get the agreed list of categories ---
presence_df   = pd.read_excel("presence_matrix.xlsx")
all_categories = presence_df["Category"].dropna().unique()

# --- Load raw price data (one sheet per province) ---
xls       = pd.ExcelFile("data/prezzi_oss.xlsx")
provinces = xls.sheet_names

print(f"Provinces found: {len(provinces)}")
print(f"Categories to keep: {len(all_categories)}")

# --- Reshape each province sheet and combine ---
all_data = []

for province in provinces:
    df = pd.read_excel(xls, sheet_name=province)

    # First column contains category names; rename for consistency
    df = df.rename(columns={df.columns[0]: "Category"})

    # Keep only categories present in the coverage matrix
    df = df[df["Category"].isin(all_categories)]

    # Reshape from wide (months as columns) to long format
    df_long = df.melt(id_vars="Category", var_name="Month", value_name="Price")
    df_long["Province"] = province

    all_data.append(df_long)

combined = pd.concat(all_data, ignore_index=True)

# --- Clean up whitespace in string columns ---
combined["Category"] = combined["Category"].str.strip()
combined["Month"]    = combined["Month"].astype(str).str.strip()

# --- Save output ---
combined.to_excel("all_categories_prices_by_province.xlsx", index=False)

print(f"\nHarmonised dataset saved: {combined.shape[0]:,} rows x {combined.shape[1]} columns")
print(combined.head(10).to_string(index=False))