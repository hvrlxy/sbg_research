import pandas as pd 
import random as rd

#assign each student a unique id
ids = []
name_dict = {}
email_dict = {}

def create_new_id():
	new_id = rd.randint(10000, 99999)
	while new_id in ids:
		new_id = rd.randint(10000, 99999)
	ids.append(new_id)
	return new_id

checkpoints_pd["full_name"] = checkpoints_pd['surname'] + " " + checkpoints_pd["first name"]

for i in range(len(checkpoints_pd)):
	name = checkpoints_pd["full_name"][i]
	email = checkpoints_pd["email"][i]

	if name not in name_dict.keys():
		new_id = create_new_id()
		name_dict[name] = new_id
		email_dict[email] = new_id

name_df = pd.DataFrame(name_dict.items(), columns = ["name", "id"])
email_df = pd.DataFrame(email_dict.items(), columns = ["email", "id"])

print(email_df.head(5))