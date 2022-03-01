import pandas as pd 
import numpy as np

#read csv file
checkpoint_df = pd.read_csv("https://github.com/hvrlxy/hvrlxy.github.io/tree/main/assets/datasets/sbg_csv/checkpoints.csv")
grade_df = pd.read_csv("https://github.com/hvrlxy/hvrlxy.github.io/tree/main/assets/datasets/sbg_csv/grades.csv")
checkpoint_df = checkpoint_df.drop(columns=['Unnamed: 0'])
grade_df = grade_df.drop(columns=['Unnamed: 0'])

#clean the start date of each checkpoints, so - become None
checkpoint_df.loc[checkpoint_df['started'] == '-', 'started'] = None
checkpoint_df.loc[checkpoint_df['checkpoints'] == '-', 'checkpoints'] = 0

#change started column into datetime
checkpoint_df['started']= pd.to_datetime(checkpoint_df['started'])
#change checkpoint to int
checkpoint_df['checkpoints']= pd.to_numeric(checkpoint_df['checkpoints'])
checkpoint_df['grade']= pd.to_numeric(checkpoint_df['grade'])

#get the list of student_ids
student_list = list(set(checkpoint_df['ID']))


def calculate_total_checkpoint_time (student_id: int, checkpoint: int):
	# given the student id and the checkpoint id, find the 
	# total number of attempts the student made, and the 
	# total time needed to finished the checkpoints and the
	# final score of the checkpoint

	student_df = checkpoint_df.loc[(checkpoint_df['ID'] == student_id) & (checkpoint_df['checkpoints'] == checkpoint)]
	total_attempt = len(student_df)

	final_score = list(student_df['grade'])[-1]
	total_time = 0

	if total_attempt > 1:
		total_time = (list(student_df['started'])[-1] - list(student_df['started'])[0]).total_seconds() / 86400

	return total_attempt, final_score, total_time

columns = ['ID', 'final_grade', 'final_checkpoints']

def get_student_info(student_id: int):
	student_grade = 'F'
	student_checkpoint = 0 

	if len(grade_df.loc[grade_df['ID'] == student_id]['grade']) > 0:
		student_grade = list(grade_df.loc[grade_df['ID'] == student_id]['grade'])[0]
	student_checkpoint = len(checkpoint_df.loc[(checkpoint_df['ID'] == student_id) & (checkpoint_df['grade'] == 1)])

	return student_grade, student_checkpoint

for i in range(1, 25):
	columns.append('chp ' + str(i) + ' total_attempt')
	columns.append('chp ' + str(i) + ' final_score')
	columns.append('chp ' + str(i) + ' total_time')

col_values = []
for ID in student_list:
	student_info = []
	student_grade, student_checkpoint = get_student_info(ID)
	student_info.append(ID)
	student_info.append(student_grade)
	student_info.append(student_checkpoint)

	col_index = 3
	for i in range (1,25):
		total_attempt, final_score, total_time = calculate_total_checkpoint_time(ID, i)
		student_info.append(total_attempt)
		student_info.append(final_score)
		student_info.append(total_time)
		col_index += 3

	col_values.append(student_info)

merge_checkpoint_df = pd.DataFrame(col_values, columns=columns)
merge_checkpoint_df['ID'] = merge_checkpoint_df['ID'].astype(np.int64)

merge_checkpoint_df.to_csv("../../clean_datasets/csv_file/merge_checkpoints.csv")
merge_checkpoint_df.to_excel("../../clean_datasets/excel_file/merge_checkpoints.xlsx", index=False)
