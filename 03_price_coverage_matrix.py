# =============================================================================
# Price Category Coverage Matrix
# Author: Giulia Mencarelli
#
# Builds a presence/absence matrix showing which food price categories are
# available for each province in the Osservatorio Prezzi data. This is used
# to identify categories with sufficient provincial coverage and decide which
# to exclude from the analysis due to too many missing provinces.
#
# Input:  categories_by_province.xlsx  (manually compiled from Osservatorio
#         Prezzi; one column per province, rows listing available categories)
# Output: presence_matrix.xlsx
# =============================================================================

import pandas as pd

# --- Load category-by-province reference table ---
df = pd.read_excel("data/categories_by_province.xlsx", sheet_name="Sheet1")

# --- Build unified list of all categories appearing in any province ---
unique_categories = pd.unique(df.melt(value_name="Category")["Category"])

# --- Construct presence/absence matrix ---
# For each province, mark True if the category is available, False otherwise
presence_matrix = pd.DataFrame({"Category": unique_categories})

for province in df.columns:
    province_items = df[province].dropna().unique()
    presence_matrix[province] = presence_matrix["Category"].isin(province_items)

# --- Count how many provinces report each category ---
presence_matrix["CoverageCount"] = presence_matrix[df.columns].sum(axis=1)

# --- Sort by coverage (most widely available categories first) ---
presence_matrix = (
    presence_matrix
    .sort_values("CoverageCount", ascending=False)
    .reset_index(drop=True)
)

# --- Save and summarise ---
presence_matrix.to_excel("presence_matrix.xlsx", index=False)

print("Coverage summary (top 10 categories):")
print(presence_matrix[["Category", "CoverageCount"]].head(10).to_string(index=False))
print(f"\nTotal categories found: {len(presence_matrix)}")
print(f"Total provinces:        {len(df.columns)}")