import pandas as pd 
from check_ids import *

#GRADE FILE CLEAN_UP
grade_path = "../../orig_datasets/grades.xlsx"
grade_file = pd.ExcelFile(grade_path)
grade_sheets = grade_file.sheet_names

# print(pd.read_excel(grade_path, sheet_name=grade_sheets[0]).columns)

column_names = ['first_name', 'surname', 'grade', 'checkpoint_total',
       'Preview Activities total (Real)', 'Team Activities total (Real)',
       'WebWork total (Real)', '1.1.1',
       '1.2.1',
       '1.3.1',
       '1.4.1',
       '1.5.1',
       '1.6.1',
       '1.7.1',
       '1.8.1',
       '2.1.1',
       '2.2.1',
       '2.3.1',
       '2.4.1',
       '2.5.1',
       '2.6.1',
       '2.7.1',
       '2.8.1',
       '3.1.1',
       '3.2.1',
       '3.3.1',
       '3.4.1',
       '3.5.1',
       '4.1.1',
       '4.2.1',
       '4.4.1',
       '4.3.1',
       'Preview Activities total (Real).1',
       'Attendance: Team Activities (Real)', 'Team Activities total (Real).1',
       'webwork_1',
       'webwork_2',
       'webwork_3',
       'webwork_4',
       'webwork_5',
       'webwork_6',
       'webwork_7',
       'webwork_8',
       'webwork_9',
       'webwork_10',
       'webwork_11',
       'webwork_12',
       'webwork_13', 'WebWork total (Real).1',
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
semester_col = grade_pd['semester']
#drop unnecessary columns
grade_pd = grade_pd.drop(columns = column_names[49:])
grade_pd = grade_pd.drop(columns = column_names[32:35])
grade_pd = grade_pd.drop(columns = column_names[4:7])
grade_pd = grade_pd.drop(columns = ['first_name', 'surname', 'full_name'])

first_column = grade_pd.pop('ID')
grade_pd.insert(0, 'ID', first_column)
grade_pd['semester'] = semester_col

#turn the dataframe into a csv file
grade_pd.to_csv("~/Desktop/hale.github.io/assets/datasets/sbg_csv/grades.csv")
grade_pd.to_excel("../../clean_datasets/excel_file/grade.xlsx", index=False)
