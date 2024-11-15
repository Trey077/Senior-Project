from src.preprocessors import load_data, preprocess_data, vectorize_data
from src.clustering import cluster_ideas, print_cluster_results, save_clustered_ideas
from src.evaluate import evaluate_metrics
from src.visualize_results import visualize_clusters

def main():
    file_path = 'Data Sets/ideas.csv'
    df = load_data(file_path)

    if df is not None:
        "process of actually getting this to work"
        df = preprocess_data(df)

        x, vectorizer = vectorize_data(df)

        labels, kmeans = cluster_ideas(x, num_clusters=5)
        df['Cluster'] = labels  # Add cluster labels back to the original DataFrame

        print_cluster_results(df)  # Print cluster results for troubleshooting

        save_clustered_ideas(df, 'Data Sets/cluster_results.csv')


        evaluate_metrics(df,x, kmeans)


        visualize_clusters(df, x, kmeans)


if __name__ == '__main__':
    main()
