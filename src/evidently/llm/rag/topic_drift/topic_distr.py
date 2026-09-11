from bertopic import BERTopic

def get_topic_distr(embedding_model, text):
    """
    Get the topic distribution based on an embedding model
    """
    topic_model = BERTopic(
        embedding_model=embedding_model,
        min_topic_size=3,
        verbose=True
    )

    topics, probs = topic_model.fit_transform(text)

    topic_info = topic_model.get_topic_info()

    topic_distribution = {}

    for topic_id in topic_info.Topic:
        if topic_id == -1:
            continue

        words = topic_model.get_topic(topic_id)

        topic_distribution[f"Topic {topic_id}"] = {
            word: float(score)
            for word, score in words
        }

    return topic_distribution
