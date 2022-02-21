import pandas as pd 

name_df = pd.read_csv("./csv_file/name_id.csv")
name_df = pd.DataFrame(name_df,columns=["name", "id"])
email_df = pd.read_csv("./csv_file/email_id.csv")
email_df = pd.DataFrame(email_df, columns=["email", "id"])

def get_ids(name=None, email=None):
	if name is not None:
		df = name_df.loc[name_df["name"] == name]
		if len(df) != 0:
			return list(df["id"])[0]
		else:
			print(name)
			return None
	elif email is not None:
		df = email_df.loc[email_df["email"] == email]
		return list(df["id"])[0]
	else:
		print("please provide a name or email")
		return None
