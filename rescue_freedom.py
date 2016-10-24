import pandas as pd
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt

prev_df = pd.read_csv('../../documents/prevelence.csv', thousands=',')
gov_df = pd.read_csv('../../documents/gov_support.csv', thousands=',')
vuln_df = pd.read_csv('../../documents/vulnerabilty_measures.csv', thousands=',')


df = pd.merge(gov_df, vuln_df, on = 'country')
df = pd.merge(df, prev_df, on = 'country')

df = df.drop(['total_score','mean'], 1)
scatter_matrix(df,figsize=[15,15],marker='o')
plt.show()
