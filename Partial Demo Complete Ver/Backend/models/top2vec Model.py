from top2vec import Top2Vec
import pandas as pd
from Flask_Application.Backend.Data_Processing.Data_Cleaning import data_processing

umap_args = { 'n_neighbors' : 10,
              'n_components' : 2,
              'metric' : 'cosine',
              'random_state' : 42,
            }

hdbscan_args = {
                'min_cluster_size' : 10,
                'min_samples' : 5,
                'metric' : 'euclidean',
                'cluster_selection_method': 'eom'
}

def run_model():
    docs, _ = data_processing()
    model_ngrams = Top2Vec(docs, ngram_vocab=True, embedding_model='doc2vec', speed='deep-learn',workers=4,umap_args=umap_args,hdbscan_args=hdbscan_args)
    print(model_ngrams.get_topic_sizes())


run_model()

