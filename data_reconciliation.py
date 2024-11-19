import pandas as pd
import random

data_cite = {
    'DOI': ['10.1000/xyz123', '10.1000/xyz456', '10.1000/xyz789'],
    'Authors': ['Smith, John; Doe, Jane', 'Brown, Alice', 'Taylor, Bob; White, Claire'],
    'Title': ['Research Paper A', 'Research Paper B', 'Research Paper C'],
    'Publication Year': [2020, 2021, 2022],
    'Journal': ['Journal A', 'Journal B', 'Journal C']
}

crossref_data = {
    'DOI': ['10.1000/xyz123', '10.1000/xyz456', '10.1000/xyz999'],
    'Authors': ['Smith, John; Doe, Jane', 'Brown, Alice; Green, Charlie', 'Taylor, Bob; White, Claire'],
    'Title': ['Research Paper A', 'Research Paper B', 'Research Paper D'],
    'Publication Year': [2020, 2021, 2023],
    'Journal': ['Journal A', 'Journal B', 'Journal D']
}

df_data_cite = pd.DataFrame(data_cite)
df_crossref = pd.DataFrame(crossref_data)
merged_data = pd.merge(df_data_cite, df_crossref, on='DOI', how='outer', suffixes=('_data_cite', '_crossref'))
log = []

def check_discrepancies(row):
    discrepancies = []
    
    if row['Authors_data_cite'] != row['Authors_crossref']:
        discrepancies.append(f"Author mismatch: {row['Authors_data_cite']} vs {row['Authors_crossref']}")
  
    if row['Publication Year_data_cite'] != row['Publication Year_crossref']:
        discrepancies.append(f"Year mismatch: {row['Publication Year_data_cite']} vs {row['Publication Year_crossref']}")
    
    if row['Journal_data_cite'] != row['Journal_crossref']:
        discrepancies.append(f"Journal mismatch: {row['Journal_data_cite']} vs {row['Journal_crossref']}")
    
    return discrepancies

for index, row in merged_data.iterrows():
    discrepancies = check_discrepancies(row)
    
    if discrepancies:
        log.append(f"Discrepancies for DOI {row['DOI']}: {', '.join(discrepancies)}")

merged_data.to_csv("data/reconciled_data.csv", index=False)

with open("logs/reconciliation_log.txt", "w") as log_file:
    log_file.write("\n".join(log))

print("Data reconciliation complete")
