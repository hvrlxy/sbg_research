import pandas as pd 
import numpy as np
from datetime import datetime


checkpoint_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/checkpoints.csv")
background_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/cleaned_survey.csv")
revision_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/revisions.csv")

#clean up the datesets
checkpoint_df = checkpoint_df.drop(columns=['Unnamed: 0', 'time taken'])
checkpoint_df = checkpoint_df.loc[checkpoint_df['started'] != '-']
checkpoint_df['started'] = pd.to_datetime(checkpoint_df['started'])

checkpoint_df['checkpoints'] = checkpoint_df['checkpoints'].dropna()

background_df = background_df.drop(columns=['Unnamed: 0'])

revision_df = revision_df.drop(columns=['Unnamed: 0'])
# print(revision_df.head(5))
student_list = list(set(checkpoint_df['ID']))

spring_checkpoint_date = ['2/5/2021', '2/11/2021', '2/16/2021', '2/19/2021', '2/23/2021', '2/26/2021', '3/1/2021', '3/5/2021', '3/16/2021', '3/16/2021', '3/19/2021', '3/23/2021', '3/26/2021', '3/30/2021', '4/5/2021', '4/8/2021', '4/12/2021', '4/15/2021', '4/22/2021', '4/26/2021', '4/26/2021', '4/27/2021', '4/27/2021', '4/27/2021']
fall_checkpoint_date = ['9/13/2021', '9/16/2021', '9/23/2021', '9/27/2021', '9/30/2021', '10/4/2021', '10/7/2021', '10/12/2021', '10/19/2021', '10/19/2021', '10/22/2021', '10/29/2021', '11/2/2021', '11/5/2021', '11/9/2021', '11/12/2021', '11/16/2021', '11/19/2021', '11/30/2021', '12/3/2021', '12/3/2021', '12/6/2021', '12/6/2021', '12/6/2021']

spring_checkpoint_date = [datetime.strptime(x, '%m/%d/%Y') for x in spring_checkpoint_date]
fall_checkpoint_date = [datetime.strptime(x, '%m/%d/%Y') for x in fall_checkpoint_date]

def find_checkpoint(current_date, is_spring = True):

	'''
	Given the current date and the semester, find out how many 
	checkpoints have been open for submission
	'''

	for i in range(24):
		if (current_date - spring_checkpoint_date[i]).days < 0:
			# print(current_date, spring_checkpoint_date[i - 1])
			return i

	if (current_date - spring_checkpoint_date[23]).days >= 0:
		return 24

	return [current_date, is_spring]

student_dict = {student_id: {'total_completed': 0, 'attempt': {i: 0 for i in range(1,25)}, 'office_hours': {i: 0 for i in range(1,25)}, 'checkpoint_complete': {i: False for i in range(1,25)} } for student_id in student_list}

df_values = []

def find_office_hours(student_id: int, checkpoint_no: int, no_attempt: int, current_date):
	# need to fill in later
	student_revision_df = revision_df.loc[revision_df['ID'] == student_id].loc[revision_df['checkpoint'] == checkpoint_no]
	if len(student_revision_df) == 0:
		return 0
	office_hours_lst = list(student_revision_df['office_hours'])[:max((no_attempt-1), 0)]
	return len([x for x in office_hours_lst if x == 'Yes'])

def find_background_info(student_id: int):
	#need to fill in later
	student_df = background_df.loc[background_df['ID'] == student_id]
	if len(student_df) == 0:
		return -1, -1, -1
	else:
		# print(student_df)
		duration = list(student_df['last_semester'])[0]
		confidence = list(student_df['ratings'])[0]
		year = list(student_df['class'])[0]
		return duration, confidence, year

def find_avg_attempt(student_id):
	total_time = 0.0
	total_checkpoint_complete = student_dict[student_id]['total_completed']
	for i in range(1, 25):
		if student_dict[student_id]['checkpoint_complete'][i]:
			total_time += student_dict[student_id]['attempt'][i]

	if total_checkpoint_complete == 0:
		return 1000 #return a large number
	else:
		return total_time/total_checkpoint_complete

for i in checkpoint_df.index:
	is_spring = not checkpoint_df['semester'][i] == 'Fa21 - 002'

	student_id = checkpoint_df['ID'][i]
	average_attempt = find_avg_attempt(student_id)
	current_date = checkpoint_df['started'][i]
	checkpoint_no = checkpoint_df['checkpoints'][i]
	is_passed = checkpoint_df['grade'][i] == 1

	if is_passed:
		student_dict[student_id]['total_completed'] += 1
		student_dict[student_id]['checkpoint_complete'][checkpoint_no] = True

	no_attempt = student_dict[student_id]['attempt'][checkpoint_no]
	student_dict[student_id]['attempt'][checkpoint_no] += 1
	student_dict[student_id]['office_hours'][checkpoint_no] = find_office_hours(student_id, checkpoint_no, no_attempt, current_date)

	office_hours = student_dict[student_id]['office_hours'][checkpoint_no]
	
	percentage_checkpoint = student_dict[student_id]['total_completed'] / find_checkpoint(current_date, is_spring)
	# print(percentage_checkpoint)
	duration, confidence, year = find_background_info(student_id)

	df_values.append([student_id, checkpoint_no, duration, confidence, year, percentage_checkpoint, no_attempt, average_attempt, office_hours, is_passed])

final_df = pd.DataFrame(df_values, columns=['student_id', 'checkpoint_no', 'duration', 'confidence', 'year', 'percentage_checkpoint', 'no_attempt', 'average_attempt', 'office_hours', 'is_passed'])
final_df.to_csv('../../../hale.github.io/assets/datasets/sbg_csv/attempts.csv')



		



# print(checkpoint_df['ID'][1])
