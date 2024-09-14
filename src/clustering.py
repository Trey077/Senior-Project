from sklearn.cluster import KMeans

def cluster_ideas(x, num_clusters=5):
    """
    Clusters vectorized data into specified number of clusters.
    """
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(x)
    return labels, kmeans

def print_cluster_results(df):
    """
    Prints out the results of clustering to help troubleshoot.
    """
    for cluster in df['Cluster'].unique():
        print(f"\nCluster {cluster}:")
        print(df[df['Cluster'] == cluster][['Idea ID', 'Description']].head())




def save_clustered_ideas(df, output_file='cluster_results.csv'):
    df.to_csv(output_file, index=False)
    print(f"Saved cluster results to {output_file}")