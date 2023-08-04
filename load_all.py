import germa_parl_parser as gpp
import open_data_parser as odp
import gender_classification as gc
import pandas as pd
import re

df_gp = gpp.get_data()
df_od = odp.get_data()

# merge dataframes
merged_df = pd.concat([df_od, df_gp], ignore_index=True)

# set continuous IDs
merged_df['id'] = range(0, len(merged_df))
merged_df['id'] = 'SP-' + merged_df['date'].dt.year.astype(str) + '-' + merged_df['id'].astype(str)
merged_df = merged_df.reset_index(drop=True)

# replace double occurences of the same speaker and unknown genders
merged_df['speaker_name'] = merged_df['speaker_name'].replace({'Kersten Naumann': 'Kersten Steinke', 'Cajus Julius Caesar': 'Cajus Caesar', 'Matern von Marschall von Bieberstein': ' Matern von Marschall'})

# set unqiue speaker IDs
merged_df['speaker_id'] = merged_df.groupby('speaker_name').ngroup() + 1

# get rid of mostly_male and mostly_female gender classification
merged_df['speaker_gender'] = merged_df['speaker_gender'].replace('mostly_male', 'male')
merged_df['speaker_gender'] = merged_df['speaker_gender'].replace('mostly_female', 'female')

# fix faulty gender classification due to whitespace characters
unknown_rows = merged_df[merged_df['speaker_gender'] == 'unknown']
for index, row in unknown_rows.iterrows():
    without_ws = re.sub('(\s){1,}', '', row['speaker_name'])
    spaced_capitals = re.sub(r"(\w)([A-Z])", r"\1 \2", without_ws)

    merged_df.loc[index, 'speaker_name'] = spaced_capitals
    merged_df.loc[index, 'speaker_gender'] = gc.get_gender(row['speaker_name'].split()[0])

# save dataframe to a pickled file
merged_df.to_pickle('data_merged.pkl')
print("dataframe has been saved to 'data_merged.pkl'")