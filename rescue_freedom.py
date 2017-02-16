import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.cm as cm
from sklearn.metrics import silhouette_samples, silhouette_score
import pickle

def load_data():
    '''bring in data summary data of each country'''
    df = pd.read_csv('data/final_df.csv', thousands=',')
    print df.head()
    return df

def kmeans_clustering(x, n):
    kmeans = KMeans(n_clusters=n, random_state=0).fit(x)
    return kmeans.labels_


def plot(x, y, z, label):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z, c=label.astype(np.float), s=df['ss_per_100000'])
    ax.set_title('Visualization of Country clusters', fontsize=25)
    ax.set_xlabel("Goverment effort", fontsize=18)
    ax.set_ylabel("NGOs working in county", fontsize=18)
    ax.set_zlabel('Vulnerability mean', fontsize=18)
    plt.savefig('data/2d_with_us2.png');
    # line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                #    interval=50, blit=False)
    plt.show()

def plot2D(x, y, label):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.scatter(x, y,  c=label.astype(np.float))
    ax.set_title('Visualization of Country clusters', fontsize=25)
    ax.set_xlabel("Goverment effort", fontsize=20)
    ax.set_ylabel("NGO Effort", fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.savefig('data/2d.png');
    plt.show()
    # pickle.dump(fig, file('FigureObject.fig.pickle', 'wb'))

def df_with_country_codes(df):
    world_df = pd.read_csv('data/world_countries.csv')
    # print world_df.head()
    df_with_codes = pd.merge(world_df, df,how = 'outer', on = 'country')
    df_with_codes.to_csv('data/labels2.csv', index=False)
    return df_with_codes




if __name__ == '__main__':
    df = load_data()
    X = df[['gov_effort', 'ngo_effort', 'vul_mean']].values
    # silhouette_plot(X)
    label = kmeans_clustering(X,9)
    df['labels']=label

    plot(df['gov_effort'], df['ngo_effort'], df['vul_mean'], label)
    # X=df[['gov_effort', 'ngo_effort']].values
    # label = kmeans_clustering(X)
    plot2D(df['gov_effort'], df['ngo_effort'], label)
    # df['test']=df['sum']+df['num_NGOs']
    # df['eff']=df['test']/df['ss_per_100000']
    # X2 = df[['eff', 'vul_mean']].values
    # # silhouette_plot(X2)
    # plot2D(df['eff'], df['vul_mean'], kmeans_clustering(X2))
    # label = kmeans_clustering(X2, 8)

    # df[['country', 'labels']].to_csv('data/labels.csv', index=False)
    # world = df_with_country_codes(df[['country', 'labels']])
    # figx = pickle.load(file('FigureObject.fig.pickle', 'rb'))
    # figx.show()
