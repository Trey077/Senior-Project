import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def visualize_clusters(df, x, kmeans):
    """Visualizes the clusters using PCA."""
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x.toarray())

    plt.scatter(principal_components[:, 0], principal_components[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.title('Cluster Visualization using PCA')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')
    plt.show()
