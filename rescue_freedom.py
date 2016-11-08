import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

def load_data():
    prev_df = pd.read_csv('../../documents/prevelence.csv', thousands=',')
    vuln_df = pd.read_csv('../../documents/vulnerabilty_measures.csv', thousands=',')
    df = pd.merge(prev_df, vuln_df, on = 'country')
    df = df.drop(['mean', 'rank'], 1)
    df_ngo = pd.read_csv('data/num_ngos.csv')
    df_new = pd.merge(df, df_ngo, how = 'outer', on='country')
    df_new['num_NGOs']=df_new['num_NGOs'].fillna(0)
    df_new['num_NGOs'][156]=5.0
    return df_new

def plot():
    scatter_matrix(df,figsize=[15,15],marker='o')
    plt.show()

def main():
    df = load_data()
    return df

def gov_df(df):
    gov_df = pd.read_csv('data/gov.csv')
    gov_df.set_index('country', drop=False, inplace=True)
    gov_df['sum']=gov_df.sum(axis=1)
    sum_df = gov_df[['country', 'sum']]
    df = pd.merge(sum_df, df, how='outer', on='country')
    return df

def add_region(df):
    df_region = pd.read_csv('data/region.csv', delimiter= ':')
    df = pd.merge(df, df_region, how='inner', on='country')
    #data from IOM
    perc_sexual_slavery_by_region = {'South Asia':24.8, 'Central Asia':24.8, 'Western Asia':16.1, 'Southeast Asia':8.4, 'East Asia':8.4, 'South America':23.0, 'Oceania':20.0, 'North America':11.4, 'Europe':22.1, 'Central America':10.9, 'Caribbean':10.9, 'Africa':12.3}
    df['perc_sexual_slavery']=[perc_sexual_slavery_by_region[key] for key in df['region']]
    return df

def kmeans_clustering(x):
    kmeans = KMeans(n_clusters=8, random_state=0).fit(x)
    return kmeans.labels_


def plot(df):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    zero=df[df['labels']==0]
    one=df[df['labels']==1]
    two=df[df['labels']==2]
    three=df[df['labels']==3]
    four=df[df['labels']==4]
    five=df[df['labels']==5]
    six=df[df['labels']==6]
    seven=df[df['labels']==7]
    ax.scatter(zero['gov_effort'], zero['ngo_effort'], zero['vul_mean'], c='r', s = 40)
    ax.scatter(one['gov_effort'], one['ngo_effort'], one['vul_mean'], c='b', s = 40 )
    ax.scatter(one['gov_effort'], one['ngo_effort'], one['vul_mean'], c='b', s = 40)
    ax.scatter(two['gov_effort'], two['ngo_effort'], two['vul_mean'], c='k', s = 40)
    ax.scatter(three['gov_effort'], three['ngo_effort'], three['vul_mean'], c='g', s = 40)
    ax.scatter(four['gov_effort'], four['ngo_effort'], four['vul_mean'], c='purple', s = 40)
    ax.scatter(five['gov_effort'], five['ngo_effort'], five['vul_mean'], c='yellow', s = 40)
    ax.scatter(six['gov_effort'], six['ngo_effort'], six['vul_mean'], c='orange', s = 40)
    ax.scatter(seven['gov_effort'], seven['ngo_effort'], seven['vul_mean'], c='orange', s = 40)
    plt.show()


if __name__ == '__main__':
    df = main()
    df_regions = add_region(df)
    df = gov_df(df_regions)
    df['est_sexual_slavery']= df['estimated_numb']* df['perc_sexual_slavery']*.01
    df['ss_per_100000'] = df['est_sexual_slavery']/df['population']*100000
    df['gov_effort']= df['sum']/df['ss_per_100000']
    df['ngo_effort']= df['num_NGOs']/df['ss_per_100000']
    df['vul_mean'] = (df['civil_pol_protect']+df['soc_health_eco_rigths']+df['security']+df['refugee_and_conflict'])/4.
    df = df.dropna()
    df = df[df.country != 'United States']
    x = df[['gov_effort', 'ngo_effort', 'vul_mean']].values
    label = kmeans_clustering(x)
    df['labels']=label
    plot(df)
