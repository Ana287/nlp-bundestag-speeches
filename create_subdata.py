import pandas as pd
import os

df_merged = pd.read_pickle('data_merged.pkl')

for year in df_merged['date'].dt.year.unique():

    # filter dataframe for each year in the list of unique years
    sub_df = df_merged[df_merged['date'].dt.year == year]

    # save subdataframes to pickle in given directory
    output_dir = 'data_yearly'
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f'subdata_{year}.pkl')

    sub_df.to_pickle(filename)