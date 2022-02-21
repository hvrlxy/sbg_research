import pandas as pd 
from check_ids import *

#GRADE FILE CLEAN_UP
grade_path = "../../orig_datasets/grades.xlsx"
grade_file = pd.ExcelFile(grade_path)
grade_sheets = grade_file.sheet_names

# print(pd.read_excel(grade_path, sheet_name=grade_sheets[0]).columns)

column_names = ['first_name', 'surname', 'grade', 'checkpoint_total',
       'Preview Activities total (Real)', 'Team Activities total (Real)',
       'WebWork total (Real)', 'Assignment: Preview Activity 1.1.1 (Real)',
       'Assignment: Preview Activity 1.2.1 (Real)',
       'Assignment: Preview Activity 1.3.1 (Real)',
       'Assignment: Preview Activity 1.4.1 (Real)',
       'Assignment: Preview Activity 1.5.1 (Real)',
       'Assignment: Preview Activity 1.6.1 (Real)',
       'Assignment: Preview Activity 1.7.1 (Real)',
       'Assignment: Preview Activity 1.8.1 (Real)',
       'Assignment: Preview Activity 2.1.1 (Real)',
       'Assignment: Preview Activity 2.2.1 (Real)',
       'Assignment: Preview Activity 2.3.1 (Real)',
       'Assignment: Preview Activity 2.4.1 (Real)',
       'Assignment: Preview Activity 2.5.1 (Real)',
       'Assignment: Preview Activity 2.6.1 (Real)',
       'Assignment: Preview Activity 2.7.1 (Real)',
       'Assignment: Preview Activity 2.8.1 (Real)',
       'Assignment: Preview Activity 3.1.1 (Real)',
       'Assignment: Preview Activity 3.2.1 (Real)',
       'Assignment: Preview Activity 3.3.1 (Real)',
       'Assignment: Preview Activity 3.4.1 (Real)',
       'Assignment: Preview Activity 3.5.1 (Real)',
       'Assignment: Preview Activity 4.1.1 (Real)',
       'Assignment: Preview Activity 4.2.1 (Real)',
       'Assignment: Preview Activity 4.4.1 (Real)',
       'Assignment: Preview Activity 4.3.1 (Real)',
       'Preview Activities total (Real).1',
       'Attendance: Team Activities (Real)', 'Team Activities total (Real).1',
       'Assignment: WebWork Assignment 1 (Real)',
       'Assignment: WebWork Assignment 2 (Real)',
       'Assignment: WebWork Assignment 3 (Real)',
       'Assignment: WebWork Assignment 4 (Real)',
       'Assignment: WebWork Assignment 5 (Real)',
       'Assignment: WebWork Assignment 6 (Real)',
       'Assignment: WebWork Assignment 7 (Real)',
       'Assignment: WebWork Assignment 8 (Real)',
       'Assignment: WebWork Assignment 9 (Real)',
       'Assignment: WebWork Assignment 10 (Real)',
       'Assignment: WebWork Assignment 11 (Real)',
       'Assignment: WebWork Assignment 12 (Real)',
       'Assignment: WebWork Assignment 13 (Real)', 'WebWork total (Real).1',
       'Quiz: Checkpoint 1 (Real)', 'Quiz: Checkpoint 2 (Real)',
       'Quiz: Checkpoint 3 (Real)', 'Quiz: Checkpoint 4 (Real)',
       'Quiz: Checkpoint 5 (Real)', 'Quiz: Checkpoint 6 (Real)',
       'Quiz: Checkpoint 7 (Real)', 'Quiz: Checkpoint 8 (Real)',
       'Quiz: Checkpoint 9 (Real)', 'Quiz: Checkpoint 10 (Real)',
       'Quiz: Checkpoint 11 (Real)', 'Quiz: Checkpoint 12 (Real)',
       'Quiz: Checkpoint 13 (Real)', 'Quiz: Checkpoint 14 (Real)',
       'Quiz: Checkpoint 15 (Real)', 'Quiz: Checkpoint 16 (Real)',
       'Quiz: Checkpoint 17 (Real)', 'Quiz: Checkpoint 18 (Real)',
       'Quiz: Checkpoint 19 (Real)', 'Quiz: Checkpoint 20 (Real)',
       'Quiz: Checkpoint 21 (Real)', 'Quiz: Checkpoint 22 (Real)',
       'Quiz: Checkpoint 23 (Real)', 'Quiz: Checkpoint 24 (Real)',
       'Checkpoints total (Real).1', 'Course total (Real)',
       'Last downloaded from this course', 'semester']

grade_pd = pd.DataFrame(columns = column_names)
for sheet in grade_sheets:
	new_pd = grade_file.parse(sheet, header=None, names=column_names[:-1]).iloc[1: , :]
	new_pd["semester"] = sheet
	grade_pd = grade_pd.append(new_pd, ignore_index=True)

#drop nan
grade_pd.dropna(subset=['first_name', 'surname'], inplace=True)
grade_pd['full_name'] = grade_pd['surname'] + " " + grade_pd['first_name']

#assign the ids
grade_pd['ID'] = grade_pd["full_name"].apply(lambda x: get_ids(name=x))

#drop unnecessary columns
grade_pd = grade_pd.drop(columns = column_names[4:])
grade_pd = grade_pd.drop(columns = ['first_name', 'surname', 'full_name'])

first_column = grade_pd.pop('ID')
grade_pd.insert(0, 'ID', first_column)

#turn the dataframe into a csv file
grade_pd.to_csv("csv_file/grades.csv")
grade_pd.to_excel("excel_file/grade.xlsx", index=False)
