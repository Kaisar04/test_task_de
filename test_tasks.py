import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient

# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27018/")
# database
db = client["Employee"]
# collections
list = ["18MoreAnd21andLess","35AndMore","ArchitectEnterTime"] # list of collections to be created
for each_val in list1:
    print (each_val)
    col = db[each_val]



d = {'Name': ['Alex', 'Justin', 'Set', 'Carlos', 'Gareth', 'John', 'Bob'], 
     'Surname': ['Smur', 'Forman', 'Carey', 'Carey', 'Chapman', 'James', 'James'], 
     'Age': [21,25,35,40,19,27,25], 
     'Job': ['Python Developer', 'Java Developer', 'Project Manager', 'Enterprise architect', 'Python Developer', 'IOS Developer', 'Python Developer'], 
     'Datetime': ['2022-01-01T09:45:12', '2022-01-01T11:50:25', '2022-01-01T10:00:45', '2022-01-01T09:07:36', '2022-01-01T11:54:10', '2022-01-01T09:56:40', '2022-01-01T09:52:45']}


df = pd.DataFrame(data=d)
df['Datetime'] = pd.to_datetime(df['Datetime'])


# Conditions
conditions = [
    (df['Age'] > 18) & (df['Age'] <= 21) & (df['Job'].str.contains("Developer")),
    (df['Age'] > 21) & (df['Job'].str.contains("Developer")),
    (df['Age'] >= 35) & (df['Job'].str.contains("Developer")==False) & (df['Job'].str.contains("Manager")==False),
    (df['Age'] < 35) & (df['Job'].str.contains("Developer")==False) & (df['Job'].str.contains("Manager")==False),
    (df['Job'].str.contains("architect")),
    (df['Job'].str.contains("architect")==False),
    ]

# create a list of the values we want to assign for each condition
values = ['2022-01-01 09:00:00', '2022-01-01 09:15:00', '2022-01-01 11:00:00', '2022-01-01 09:30:00', '2022-01-01 10:30:00', '2022-01-01 09:10:00']

# create a new column and use np.select to assign values to it using our lists as arguments
df['TimeToEnter'] = np.select(conditions, values)
df['TimeToEnter'] = pd.to_datetime(df['TimeToEnter'])



df1 = df.loc[(df['Job'].str.contains("Developer"))]
df2 = df.loc[(df['Job'].str.contains("Developer")==False) & (df['Job'].str.contains("Manager")==False)]
df3 = df.loc[(df['Job'].str.contains("Developer")==False)]


# excel
df1.to_excel("18MoreAnd21andLess.xlsx")
df2.to_excel("35AndMore.xlsx")
df3.to_excel("ArchitectEnterTime.xlsx")

#mongodb
db.18MoreAnd21andLess.insert_many(df1.to_dict('records'))
db.35AndMore.insert_many(df2.to_dict('records'))
db.ArchitectEnterTime.insert_many(df3.to_dict('records'))
