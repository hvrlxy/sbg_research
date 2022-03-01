from check_ids import *

#REVISION FILE CLEAN_UP
revision_path = "../../orig_datasets/revision.xlsx"
revision_file = pd.ExcelFile(revision_path)
revision_sheets = revision_file.sheet_names

#construct a revision pd
column_names = ["timestamp", "email", "checkpoint", "mistakes", "preparation", "office_hours", 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11',
       'Unnamed: 12', "semester"]
revision_pd = pd.DataFrame(columns = column_names)

for sheet in revision_sheets:
	new_pd = revision_file.parse(sheet, header=None, names=column_names[:-1]).iloc[1: , :]
	new_pd["semester"] = sheet
	revision_pd = revision_pd.append(new_pd, ignore_index=True)
#drop nan
revision_pd.dropna(subset=['email'], inplace=True)

#assign the ids
revision_pd['ID'] = revision_pd["email"].apply(lambda x: get_ids(email=x))

#drop unnecessary columns
revision_pd = revision_pd.drop(columns = ['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11',
       'Unnamed: 12', "email"])
first_column = revision_pd.pop('ID')
revision_pd.insert(0, 'ID', first_column)

# print(revision_pd.head(5))
revision_pd.drop_duplicates(subset=['mistakes'])
#turn the dataframe into a csv file
revision_pd.to_csv("../../clean_datasets/csv_file/revisions.csv")

#convert to excel file
revision_pd.to_excel("../../clean_datasets/excel_file/revisions.xlsx", index=False)