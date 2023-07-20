import germa_parl_parser as gpp
import open_data_parser as odp
import pandas as pd

df_gp = gpp.get_data()
df_od = odp.get_data()

# merge dataframes
merged_df = pd.concat([df_od, df_gp], ignore_index=True)

# set continuous IDs
merged_df['id'] = range(0, len(merged_df))
merged_df['id'] = 'SP-' + merged_df['date'].dt.year.astype(str) + '-' + merged_df['id'].astype(str)
merged_df = merged_df.reset_index(drop=True)

# set unqiue speaker IDs
merged_df['speaker_id'] = merged_df.groupby('speaker_name').ngroup() + 1

# get rid of mostly_male and mostly_female gender classification
merged_df['speaker_gender'] = merged_df['speaker_gender'].replace('mostly_male', 'male')
merged_df['speaker_gender'] = merged_df['speaker_gender'].replace('mostly_female', 'female')

# save dataframe to a pickled file
merged_df.to_pickle('data_merged.pkl')
print("dataframe has been saved to 'data_merged.pkl'")