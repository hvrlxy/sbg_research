import pandas as pd 
import numpy as np

checkpoint_df = pd.read_csv("../../clean_datasets/csv_file/merge_checkpoints.csv")

columns = ['checkpoint', 'min_attempt', 'max_attempt', 'avg_attempt', 'med_attempt', 'min_time', 'max_time', 'avg_time']

data = []

for i in range(1, 25):

	attempt_col = 'chp ' + str(i) + ' total_attempt'
	time_col = 'chp ' + str(i) + ' total_time'

	attempt_list = checkpoint_df[attempt_col]
	time_list = checkpoint_df[time_col]

	col_values = [i, attempt_list.min(), attempt_list.max(), attempt_list.mean(), attempt_list.median(), time_list.min(), time_list.max(), time_list.mean()]
	data.append(col_values)

checkpoint_summary = pd.DataFrame(data, columns = columns)
# print(checkpoint_summary)

checkpoint_summary.to_csv("../../clean_datasets/csv_file/checkpoint_summary.csv")
checkpoint_summary.to_excel("../../clean_datasets/excel_file/checkpoint_summary.xlsx", index=False)