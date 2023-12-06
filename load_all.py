import germa_parl_parser as gpp
import open_data_parser as odp
import gender_classification as gc
import pandas as pd
import re

df_gp = gpp.get_data()
df_od = odp.get_data()

# method for removing non-alphabetic characters from strings
def clean_names(input_string):
    return re.sub(r'P{L}', '', input_string)

# merge dataframes
merged_df = pd.concat([df_od, df_gp], ignore_index=True) # TODO prüfen ob index nach df.drop() noch stimmt

# set continuous IDs
merged_df['id'] = range(0, len(merged_df))
merged_df['id'] = 'SP-' + merged_df['date'].dt.year.astype(str) + '-' + merged_df['id'].astype(str)
merged_df = merged_df.reset_index(drop=True)

# replace double occurences of the same speaker
merged_df['speaker_name'] = merged_df['speaker_name'].replace({'Kersten Naumann': 'Kersten Steinke', 'Cajus Julius Caesar': 'Cajus Caesar', 'Matern von Marschall von Bieberstein': ' Matern von Marschall'})

# get rid of mostly_male, mostly_female and unknown gender classification
merged_df['speaker_gender'] = merged_df['speaker_gender'].replace({'mostly_male': 'male', 'mostly_female': 'female'})
merged_df.drop(merged_df[merged_df['speaker_gender'] == 'unknown'].index, inplace=True)

# fix faulty gender classification due to whitespace characters
unknown_rows = merged_df[merged_df['speaker_gender'] == 'unknown']
for index, row in unknown_rows.iterrows():
    without_ws = re.sub('(\s){1,}', '', row['speaker_name'])
    spaced_capitals = re.sub(r"(\w)([A-Z])", r"\1 \2", without_ws)

    merged_df.loc[index, 'speaker_name'] = spaced_capitals
    merged_df.loc[index, 'speaker_gender'] = gc.get_gender(row['speaker_name'].split()[0])
    
# clean speaker name strings
merged_df['speaker_name'] = merged_df['speaker_name'].str.lower().apply(clean_names)

# set unqiue speaker IDs based on lowercase & cleaned speaker names
merged_df['speaker_id'] = merged_df.groupby('speaker_name').ngroup() + 1

# convert speaker_names to title case again
merged_df['speaker_name'] = merged_df['speaker_name'].str.title()

# add column for speech length
merged_df['speech_length'] = merged_df['text'].apply(len)

# save dataframe to a pickled file
merged_df.to_pickle('data_merged.pkl')
print("dataframe has been saved to 'data_merged.pkl'")