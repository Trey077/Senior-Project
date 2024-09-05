#evaluate accuracy of the model
from sklearn.metrics import silhouette_score


def evaluate_metrics(df, x, kmeans):
    "Evaluates our algorithm to ensure we have an accurate cluster"
    score = silhouette_score(x, kmeans.labels_)

    print(f"Silhouette score: {score:.4f}")


