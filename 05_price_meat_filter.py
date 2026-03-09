# =============================================================================
# Meat Price Category Selection
# Author: Giulia Mencarelli
#
# Filters the harmonised price dataset down to the six meat categories used
# in the LA-AIDS demand model. These categories were selected based on their
# coverage across provinces and their correspondence to the four meat groups
# defined in the HBS expenditure data (beef, pork, poultry, processed).
#
# Input:  all_categories_prices_by_province.xlsx
#                                (output of 04_price_harmonisation.py)
# Output: filtered_prices.xlsx   (used as price input in meat_demand_LA_AIDS.R)
# =============================================================================

import pandas as pd

# --- Load harmonised price data ---
df = pd.read_excel("all_categories_prices_by_province.xlsx")

# --- Select the six meat price categories ---
# These map to the four model goods in R as follows:
#   beef      <- Carne Fresca Bovino Adulto
#   pork      <- Carne Fresca Suina Con Osso
#   poultry   <- Petto Di Pollo
#   processed <- average of Prosciutto Cotto, Prosciutto Crudo, Pancetta
categories_of_interest = [
    "Carne Fresca Bovino Adulto, Primo Taglio (1000 Gr)",
    "Carne Fresca Suina Con Osso (1000 Gr)",
    "Petto Di Pollo (1000 Gr)",
    "Prosciutto Cotto (1000 Gr)",
    "Prosciutto Crudo (1000 Gr)",
    "Pancetta In Confezione (1000 Gr)"
]

filtered_df = df[df["Category"].isin(categories_of_interest)]

# --- Save output ---
filtered_df.to_excel("filtered_prices.xlsx", index=False)

print(f"Rows retained: {len(filtered_df):,} out of {len(df):,}")
print(filtered_df["Category"].value_counts().to_string())