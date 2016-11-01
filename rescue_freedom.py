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
    df_new = df.drop(['country', 'credit_rating', 'population', 'estimated_numb'], 1)
    df_new = df_new.dropna()
    # y = df_new.pop('estimated_perc_pop').values
    # X = df_new.values
    #
    # X_train, X_test, y_train, y_test = train_test_split(X, y)
    # rf = RandomForestClassifier(n_estimators=100, oob_score=True)
    # rf.fit(X_train, y_train)
