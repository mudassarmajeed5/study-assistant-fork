from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

class DifficultyPlanner:
    
    def __init__(self):
        self.n_clusters = 3
    
    def cluster_topics_by_similarity(self, topics: List[Dict]) -> Dict[int, List[str]]:
        topic_names = [t["main"] for t in topics]
        
        if len(topic_names) < 3:
            clusters = {0: topic_names}
            return clusters
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(topic_names)
        
        kmeans = KMeans(n_clusters=min(3, len(topic_names)), random_state=42)
        labels = kmeans.fit_predict(X)
        
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(topic_names[idx])
        
        return clusters
    
    def get_topic_clusters_by_difficulty(self, topics: List[Dict]) -> Dict[str, List[str]]:
        if not topics:
            return {"Easy": [], "Medium": [], "Hard": []}
        
        clusters = self.cluster_topics_by_similarity(topics)
        cluster_list = sorted(clusters.items())
        
        result = {"Easy": [], "Medium": [], "Hard": []}
        
        if len(cluster_list) >= 3:
            result["Easy"] = cluster_list[0][1]
            result["Medium"] = cluster_list[1][1]
            result["Hard"] = cluster_list[2][1]
        elif len(cluster_list) == 2:
            result["Easy"] = cluster_list[0][1]
            result["Medium"] = cluster_list[1][1]
        else:
            result["Easy"] = cluster_list[0][1]
        
        return result
    
    def get_progressive_quiz_sequence(self, topics: List[Dict]) -> List[str]:
        clusters = self.get_topic_clusters_by_difficulty(topics)
        sequence = clusters["Easy"] + clusters["Medium"] + clusters["Hard"]
        return sequence
