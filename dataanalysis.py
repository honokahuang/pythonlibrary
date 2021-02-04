import pandas as pd
import numpy as np
from scipy import stats

excel = pd.read_excel('analysis1.xlsx')
temp = excel.describe()
print(temp)
temp.to_excel('result analysis.xlsx')