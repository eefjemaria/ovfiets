import pandas as pd

def load_data(user:str):
    data = pd.read_csv(f'/Users/eefje/python_projects/stijn/chargingpoints_availability_2022-02-08.csv')
    data = data[data['user']==user]
    return data