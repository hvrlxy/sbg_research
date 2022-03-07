import pandas as pd 
from check_ids import *

path = '../../orig_datasets/survey.csv'
columns = ['Term', 'firstname', 'surname', 'Gustavus ID',
       'class',
       'latest_course',
       'enjoy',
       'ratings',
       'last_semester',
       'Unnamed: 9']

survey_df = pd.read_csv(path)
survey_df.columns = columns

#clean up some of the column
survey_df['fullname'] = survey_df['surname'].apply(lambda x: x.capitalize()) + ' ' + survey_df['firstname'].apply(lambda x: x.capitalize())
# survey_df['fullname'] = survey_df['fullname'].apply(lambda x: x.capitalize())
survey_df['class'] = survey_df['class'].apply(lambda x: 1 if x == 'First-year' else x)
survey_df['class'] = survey_df['class'].apply(lambda x: 2 if x == 'Second-year' else x)
survey_df['class'] = survey_df['class'].apply(lambda x: 3 if x == 'Third-year' else x)
survey_df['class'] = survey_df['class'].apply(lambda x: 4 if x == 'Fourth-year and beyond' else x)

#drop unnecessary columns
survey_df['ID'] = survey_df["fullname"].apply(lambda x: get_ids(name=x))
survey_df = survey_df.drop(columns=['Unnamed: 9', 'firstname', 'surname', 'Gustavus ID', 'fullname'])

#test print
# print(survey_df.head(30))
survey_df = survey_df.dropna(subset=['ID'])
survey_df.to_csv("../../../hale.github.io/assets/datasets/sbg_csv/cleaned_survey.csv")
print(survey_df.head(30))
