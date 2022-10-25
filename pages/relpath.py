

path="/Users/eefje/python_projects/ovfiets/data/ovfietsen_2022-10-24.csv"


import os
dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path="/Users/eefje/python_projects/ovfiets/data/ovfietsen_2022-10-24.csv"
filename = os.path.join(dirname, 'data/ovfietsen_2022-10-24.csv')

print(filename)