import os
from top2vec import Top2Vec
import pandas as pd


def generate_topic_dataframe(model_path, num_topics , topic_docs):
    """
    Generates a DataFrame of topics from a Top2Vec model.

    Args:
        model_path (str): Path to the saved Top2Vec model.
        num_topics (int): Number of topics in the model.

    Returns:
        pd.DataFrame: DataFrame containing topics and associated data.
    """
    try:
        # Resolve the model path relative to the root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        model_path = os.path.join(project_root, model_path)
        print(f"Resolved absolute model path: {model_path}")

        # Verify the file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        # Load the model
        print(f"Loading model from: {model_path}")
        model = Top2Vec.load(model_path)

        # Generate topic data
        all_docs, all_scores, all_ids, all_topics = [], [], [], []

        for topic_num in range(num_topics):
            try:
                num_docs = topic_docs[topic_num]

                # Retrieve documents, scores, and IDs for the current topic
                documents, doc_scores, doc_ids = model.search_documents_by_topic(topic_num, num_docs=num_docs)

                if documents is not None:
                    all_docs.extend(documents)
                    all_scores.extend(doc_scores)
                    all_ids.extend(doc_ids)
                    all_topics.extend([topic_num] * len(documents))

            except Exception as e:
                print(f"Error with topic {topic_num}: {e}")

        # Create a DataFrame
        topic_data = {'Topic': all_topics, 'Description': all_docs, 'ID': all_ids}
        df_topics = pd.DataFrame(topic_data)

        # Sort by ID
        df_topics.sort_values(by='ID', inplace=True)

        return df_topics

    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
    except Exception as e:
        print(f"Error generating topic data: {e}")


if __name__ == "__main__":
    # Specify the model path relative to the root of the project
    model_path = "Backend/models/Topic-Model"

    print("Starting topic generation...")
    df_topics = generate_topic_dataframe(model_path,num_topics=13, topic_docs=[451, 210, 180, 163, 157, 137, 136, 120, 116, 112, 104, 92, 92])

    if df_topics is not None:
        print("Generated topic data:")
        print(df_topics)
    else:
        print("No topic data generated.")
