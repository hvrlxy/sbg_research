import pandas as pd 
import numpy as np
from datetime import datetime
import statsmodels.api as sm

attempts_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/attempts.csv")

attempts_df = attempts_df.drop(columns=['Unnamed: 0'])
attempts_df = attempts_df.dropna()
print(attempts_df.columns)

attempts_checkpoint_1 = attempts_df.loc[attempts_df['checkpoint_no'] == 3]

X = attempts_df.iloc[:, [i for i in range(2, 9)]].to_numpy()
Y = attempts_df['is_passed'].to_numpy()

X2 = sm.add_constant(X)
est = sm.OLS(Y, X2)
# print(X)
est2 = est.fit()
print(est2.summary())

