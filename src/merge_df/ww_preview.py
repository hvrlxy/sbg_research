import pandas as pd 
from datetime import datetime

path = "~/Desktop/hale.github.io/assets/datasets/sbg_csv/grades.csv"
grade_df = pd.read_csv(path)

fall_mapping = {"1.2.1" : "09/14/2021", 
				"1.1.1": "09/10/2021",
				"1.3.1": "09/17/2021",
				"1.4.1": "09/21/2021",
				"1.5.1": "09/24/2021",
				"1.6.1": "09/28/2021",
				"1.7.1": "10/01/2021",
				"1.8.1": "10/07/2021",
				"2.1.1": "10/08/2021",
				"2.2.1": "10/12/2021",
				"2.3.1": "10/14/2021",
				"2.4.1": "10/18/2021",
				"2.5.1": "10/19/2021",
				"2.6.1": "10/22/2021",
				"2.7.1": "10/29/2021",
				"2.8.1": "11/02/2021",
				"3.1.1": "11/05/2021",
				"3.2.1": "11/09/2021",
				"3.3.1": "11/12/2021",
				"3.4.1": "11/16/2021",
				"3.5.1": "11/19/2021",
				"4.1.1": "11/29/2021",
				"4.2.1": "11/30/2021",
				"4.3.1": "12/03/2021",
				"4.4.1": "12/06/2021"}

spring_mapping = {"1.2.1" : "02/04/2021", 
				"1.1.1": "02/08/2021",
				"1.3.1": "02/11/2021",
				"1.4.1": "02/15/2021",
				"1.5.1": "02/18/2021",
				"1.6.1": "02/22/2021",
				"1.7.1": "02/25/2021",
				"1.8.1": "03/01/2021",
				"2.1.1": "03/02/2021",
				"2.2.1": "03/05/2021",
				"2.3.1": "03/11/2021",
				"2.4.1": "03/15/2021",
				"2.5.1": "03/16/2021",
				"2.6.1": "03/19/2021",
				"2.7.1": "03/23/2021",
				"2.8.1": "03/26/2021",
				"3.1.1": "03/30/2021",
				"3.2.1": "04/05/2021",
				"3.3.1": "04/08/2021",
				"3.4.1": "04/12/2021",
				"3.5.1": "04/15/2021",
				"4.1.1": "04/20/2021",
				"4.2.1": "04/22/2021",
				"4.3.1": "04/26/2021",
				"4.4.1": "04/27/2021"}

ww_fall = {"webwork_2": "09/17/2021",
			"webwork_3": "09/24/2021",
			"webwork_4": "10/1/2021",
			"webwork_5": "10/8/2021",
			"webwork_6": "10/15/2021",
			"webwork_7": "10/22/2021",
			"webwork_8": "10/29/2021",
			"webwork_9": "11/5/2021",
			"webwork_10": "11/12/2021",
			"webwork_11": "11/19/2021",
			"webwork_12": "12/3/2021",
			"webwork_13": "12/10/2021",
			"webwork_1": "9/10/2021"}

ww_spring = {"webwork_1": "2/5/2021",
			"webwork_2": "2/12/2021",
			"webwork_3": "2/19/2021",
			"webwork_4": "2/26/2021",
			"webwork_5": "3/5/2021",
			"webwork_6": "3/12/2021",
			"webwork_7": "3/19/2021",
			"webwork_8": "3/26/2021",
			"webwork_9": "4/9/2021",
			"webwork_10": "4/16/2021",
			"webwork_11": "4/22/2021",
			"webwork_12": "4/27/2021",
			"webwork_13": "5/6/2021"}

# for key in fall_mapping:
# 	fall_date = datetime.strptime(fall_mapping[key], "%m/%d/%Y")
# 	spring_date = datetime.strptime(spring_mapping[key], "%m/%d/%Y")
# 	fall_mapping[key] = fall_date
# 	spring_mapping[key] = spring_date

# for key in ww_fall:
# 	fall_date = datetime.strptime(ww_fall[key], "%m/%d/%Y")
# 	spring_date = datetime.strptime(ww_spring[key], "%m/%d/%Y")
# 	ww_fall[key] = fall_date
# 	ww_spring[key] = spring_date

cols = grade_df.columns

spring_df = grade_df.loc[grade_df['semester'] != "F21 - 002"]
fall_df = grade_df.loc[grade_df['semester'] == "F21 - 002"]

activities_df = pd.DataFrame(columns=['ID', 'timeframe', 'activities', 'semester'])

for col in ww_fall:
	for i in range(0, len(spring_df)):
		if list(spring_df[col])[i] == 1:
			new_line = [list(spring_df['ID'])[i], ww_spring[col], col, 'SP21']
			activities_df.loc[len(activities_df)] = new_line

	for i in range(0, len(fall_df)):
		if list(fall_df[col])[i] == 1:
			new_line = [list(fall_df['ID'])[i], ww_fall[col], col, 'F21']
			activities_df.loc[len(activities_df)] = new_line


for col in spring_mapping:
	for i in range(0, len(spring_df)):
		if list(spring_df[col])[i] == 1:
			new_line = [list(spring_df['ID'])[i], spring_mapping[col], col, 'SP21']
			activities_df.loc[len(activities_df)] = new_line

	for i in range(0, len(fall_df)):
		if list(fall_df[col])[i] == 1:
			new_line = [list(fall_df['ID'])[i], fall_mapping[col], col, 'F21']
			activities_df.loc[len(activities_df)] = new_line

activities_df.to_csv("~/Desktop/hale.github.io/assets/datasets/sbg_csv/ww.csv")



