import numpy as np
import pandas as pd
import calmap

class HeatMap:
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

	def get_student_activity(self, student_id: int):
		checkpoint_timestamp = self.checkpoint_df.loc[self.checkpoint_df['ID'] == student_id]
		revision_timestamp = self.revision_df.loc[self.revision_df['ID'] == student_id]

		checkpoint_timestamp = checkpoint_timestamp['started']
		revision_timestamp = revision_timestamp['timestamp']

		timestamps = checkpoint_timestamp.append(revision_timestamp)
		return timestamps.dropna()

	def group_timestamp(self, student_id):
		timestamps = self.get_student_activity(student_id)
		df = (pd.to_datetime(timestamps)
	       .dt.floor('d')
	       .value_counts())
		return df 

	def get_student_grade(self, student_id):
		student_grade = 'F'
		if len(self.grade_df.loc[self.grade_df['ID'] == student_id]['grade']) > 0:
			student_grade = list(self.grade_df.loc[self.grade_df['ID'] == student_id]['grade'])[0]
		return student_grade[0]

	def find_cmap(self,student_id):
		student_grade = self.get_student_grade(student_id)
		if student_grade == 'A':
			return 'YlGn'
		elif student_grade == 'B':
			return 'Blues'
		elif student_grade == 'C':
			return 'YlOrBr'
		else:
			return 'Reds'

	def plot_student_heatmap(self, student_id):
		cmap = self.find_cmap(student_id)
		events = self.group_timestamp(student_id)
		if len(events) == 0:
			# print("Events size is 0, cannot plot")
			return
		calmap.calendarplot(events, cmap = cmap)

	def plot_heatmap_by_grade(self, grade: str):
		for ID in self.student_list:
			student_grade = self.get_student_grade(ID)
			if student_grade == grade:
				self.plot_student_heatmap(ID)

	









