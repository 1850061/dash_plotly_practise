import plotly.express as px
from DataProcess import *
import pandas as pd
import numpy as np

df_school_type = pd.read_csv(
    '../lab3_datasets/college-salaries/salaries-by-college-type.csv')
df_school_type = data_handle(df_school_type)
dff = df_school_type[df_school_type['School Name'] == 'Massachusetts Institute of Technology (MIT)']
arr = np.array(dff)[0][2:-1]
print(arr)
