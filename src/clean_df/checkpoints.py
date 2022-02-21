import pandas as pd 
import random as rd
from check_ids import *

#CHECKPOINTS FILE CLEAN_UP
#read the check points file
checkpoint_path = "../../orig_datasets/checkpoints.xlsx"
checkpoint_file = pd.ExcelFile(checkpoint_path)
checkpoints_sheets = checkpoint_file.sheet_names

column_names = ["surname", "first name", "email", "section", "checkpoints", "started", "finished", "time taken", "grade", "Q1", "semester"]
checkpoints_pd = pd.DataFrame(columns = column_names)

for sheet in checkpoints_sheets:
	new_pd = checkpoint_file.parse(sheet, header=None, names=column_names[:-1]).iloc[1: , :]
	new_pd["semester"] = sheet
	checkpoints_pd = checkpoints_pd.append(new_pd, ignore_index=True)


checkpoints_pd["full_name"] = checkpoints_pd['surname'] + " " + checkpoints_pd["first name"]

#clean up the dataframe
checkpoints_pd['ID'] = checkpoints_pd["full_name"].apply(lambda x: get_ids(name=x))
checkpoints_pd = checkpoints_pd.drop(columns = ['full_name', "surname", "first name", "email", "Q1", "finished"])
first_column = checkpoints_pd.pop('ID')
checkpoints_pd.insert(0, 'ID', first_column)

#turn the dataframe into a csv file
checkpoints_pd.to_csv("csv_file/checkpoints.csv")
checkpoints_pd.to_excel("excel_file/checkpoints.xlsx", index=False)


