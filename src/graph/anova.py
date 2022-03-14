from scipy.stats import f_oneway
import pandas as pd
import numpy as np

attempts_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/attempts.csv")
attempts_df = attempts_df.drop(columns=['Unnamed: 0'])
attempts_df = attempts_df.dropna()
# attempts_df = attempts_df.loc[attempts_df['duration'] != -1]
# print(list(attempts_df['office_hours']))

print(f_oneway(attempts_df['is_passed'].to_numpy(), attempts_df['year'].to_numpy()))