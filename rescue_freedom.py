import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier

def load_data():
    prev_df = pd.read_csv('../../documents/prevelence.csv', thousands=',')
    gov_df = pd.read_csv('../../documents/gov_support.csv', thousands=',')
    vuln_df = pd.read_csv('../../documents/vulnerabilty_measures.csv', thousands=',')
    df = pd.merge(gov_df, vuln_df, on = 'country')
    df = pd.merge(df, prev_df, on = 'country')
    df = df.drop(['total_score','mean', 'rank'], 1)
    return df

def plot():
    scatter_matrix(df,figsize=[15,15],marker='o')
    plt.show()

def main():
    df = load_data()
    return df



if __name__ == '__main__':
    df = main()
    df_ngo = pd.read_csv('data/num_ngos.csv')
    df_new = pd.merge(df, df_ngo, how = 'outer', on='country')
    df_new['num_NGOs']=df_new['num_NGOs'].fillna(0)
    df_new['num_NGOs'][156]=5.0
    df_new['support_rate']= df_new['num_NGOs']/df_new['estimated_numb']
