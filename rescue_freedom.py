import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

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


def plot(df, label):
    fig = plt.figure(figsize=(8, 8))
    colors = ['b', 'k', 'g', 'r', 'orange', 'purple', 'yellow', 'magenta']
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['gov_effort'], df['ngo_effort'], df['civil_pol_protect'], c=label, cmap=matplotlib.colors.ListedColormap(colors), s = 40)
    plt.savefig('data/data.png')


if __name__ == '__main__':
    df = main()
    df_regions = add_region(df)
    df = gov_df(df_regions)
    df['est_sexual_slavery']= df['estimated_numb']* df['perc_sexual_slavery']*.01
    df['ss_per_100000'] = df['est_sexual_slavery']/df['population']*100000
    df['gov_effort']= df['sum']/df['ss_per_100000']
    df['ngo_effort']= df['num_NGOs']/df['ss_per_100000']
    df['vul_mean'] = (df['civil_pol_protect']+df['soc_health_eco_rigths']+df['security']+df['refugee_and_conflict'])/4.
    #df['vul_mean'] = df['vul_mean']*df['ss_per_100000']
    df = df.dropna()
    df = df[df.country != 'United States']
    x = df[['gov_effort', 'ngo_effort', 'civil_pol_protect']].values
    label = kmeans_clustering(x)
    df['labels']=label
    plot(df, label)
