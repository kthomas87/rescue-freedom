import pandas as pd
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from sklearn.metrics import silhouette_samples, silhouette_score
import pickle

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
    # Drop columns that address only Labor slavery
    drop = [col for col in gov_df.columns if 'm5' in col]
    gov_df = gov_df.drop(drop, 1)
    keep = ['m2_1.1.8','m2_1.2.5','m2_1.2.6']
    drop2 = [col for col in gov_df.columns if 'm2' in col and col not in keep]
    gov_df = gov_df.drop(drop2, 1)
    drop3 = ['m4_1.3.2', 'm4_1.6.3', 'm4_1.6.5', 'm4_1.6.7', 'm4_1.8.1']
    gov_df = gov_df.drop(drop3, 1)
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
    kmeans = KMeans(n_clusters=9, random_state=0).fit(x)
    return kmeans.labels_


def plot(df, label):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['gov_effort'], df['ngo_effort'], df['vul_mean'], c=label.astype(np.float), s=df['ss_per_100000'])
    ax.set_title('Visualization of Country clusters', fontsize=25)
    ax.set_xlabel("NGO Effort", fontsize=18)
    ax.set_ylabel("Government Effort", fontsize=18)
    ax.set_zlabel('Vulnerabilty measures', fontsize=18)
    plt.savefig('data/2d_with_us2.png');
    plt.show()
    # pickle.dump(fig, file('FigureObject.fig.pickle', 'wb'))

def silhouette_plot(X):
    range_n_clusters = [8, 9, 10, 11, 12, 13]

    for n_clusters in range_n_clusters:
        # Create a subplot with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(16, 7)
        ax1.set_xlim([-0.1, 1])
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)
        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        y_lower = 10
        for i in range(n_clusters):
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        # 2nd Plot showing the actual clusters formed
        colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
        ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                    c=colors)

        # Labeling the clusters
        centers = clusterer.cluster_centers_
        # Draw white circles at cluster centers
        ax2.scatter(centers[:, 0], centers[:, 1],
                    marker='o', c="white", alpha=1, s=200)
        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50)
        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")

        plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                      "with n_clusters = %d" % n_clusters),
                     fontsize=14, fontweight='bold')

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
    #df['vul_mean'] = df['vul_mean']*df['ss_per_100000']
    df = df.dropna()
    #df = df[df.country != 'United States']
    X = df[['gov_effort', 'ngo_effort', 'vul_mean']].values
    #silhouette_plot(X)
    label = kmeans_clustering(X)
    df['labels']=label

    plot(df, label)
    df[['country', 'labels']].to_csv('data/labels.csv', index=False)
    # figx = pickle.load(file('FigureObject.fig.pickle', 'rb'))
    # figx.show()
