import numpy as np
import pandas as pd
from datetime import timedelta
import datetime as dt

class Vectorize:
	def __init__(self):
		self.checkpoint_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/checkpoints.csv")
		self.revision_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/revisions.csv")
		self.grade_df = pd.read_csv("https://hvrlxy.github.io/assets/datasets/sbg_csv/grades.csv")

		self.checkpoint_df = self.checkpoint_df.drop(columns=['Unnamed: 0'])
		self.revision_df = self.revision_df.drop(columns=['Unnamed: 0'])
		self.grade_df = self.grade_df.drop(columns=['Unnamed: 0'])

		#clean the start date of each checkpoints, so - become None
		self.checkpoint_df.loc[self.checkpoint_df['started'] == '-', 'started'] = None
		self.checkpoint_df.dropna(subset=['started'])
		self.revision_df.dropna(subset=['timestamp'])

		#change started column into datetime
		self.checkpoint_df['started']= pd.to_datetime(self.checkpoint_df['started'])
		self.revision_df['timestamp']= pd.to_datetime(self.revision_df['timestamp'])

		#get the list of student_ids
		self.student_list = list(set(self.checkpoint_df['ID']))

		self.F21 = pd.date_range(start= '9/13/21', end='12/20/2021', freq='W')
		self.S21 = pd.date_range(start='2/5/21', end='5/8/2021', freq='W')

	def get_student_activity(self, student_id: int):
		checkpoint_timestamp = self.checkpoint_df.loc[self.checkpoint_df['ID'] == student_id]
		revision_timestamp = self.revision_df.loc[self.revision_df['ID'] == student_id]

		checkpoint_timestamp = checkpoint_timestamp['started']
		revision_timestamp = revision_timestamp['timestamp']

		timestamps = checkpoint_timestamp.append(revision_timestamp)
		return timestamps.dropna()

	def get_calendar(self, student_id):
		student_df = self.checkpoint_df.loc[self.checkpoint_df['ID'] == student_id]
		semester = list(student_df['semester'])[0]
		if semester == 'Fa21 - 002':
			return self.F21
		else:
			return self.S21

	def find_num_activity(self, student_act, week):
		delta = timedelta(days=7)
		num_act = 0
		for timestamp in student_act:
			if (week - timestamp).days <= 7 and (week - timestamp).days >= 0:
				# print('start timestamp:', week, 'current timestamp:', timestamp, 'time_different:', (week - timestamp).days)
				num_act +=1
		return num_act

	def activity_vector(self, student_id):
		student_act = self.get_student_activity(student_id)
		# print(student_act)
		calendar = self.get_calendar(student_id)
		# print(len(calendar))
		vector = [0 for i in range(len(calendar))]

		for i in range(len(calendar)):
			vector[i] = self.find_num_activity(student_act, calendar[i])

		return vector

	def export_csv(self, path):
		df_rows= []
		for ID in self.student_list:
			df_rows.append([ID] + self.activity_vector(ID))
		columns = ['ID']
		for i in range(1,15):
			columns.append('week ' + str(i))
		activity_df = pd.DataFrame(df_rows, columns=columns)
		activity_df.to_csv(path)



#test
vct = Vectorize()
vct.export_csv('../../../hale.github.io/assets/datasets/sbg_csv/weekly_activity.csv')
# print(vct.S21)
# print(set(vct.checkpoint_df['semester']))
# print(vct.activity_vector(31208))
# print(vct.activity_vector(57894))