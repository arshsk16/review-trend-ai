import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path


class TopicMemory:
    """
    Manages topic embeddings and maps raw extracted topic phrases to stable topic names.
    """
    
    def __init__(self, memory_path: str = "topic_memory.json"):
        """
        Initialize TopicMemory.
        
        Args:
            memory_path: Path to the JSON file storing topic embeddings (default: "topic_memory.json")
        """
        # Get project root (assuming this is run from project root)
        project_root = Path(__file__).parent.parent.parent
        self.memory_path = project_root / memory_path
        self.memory = {}
        
        # Initialize SentenceTransformer model
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        # Load existing memory if file exists
        if self.memory_path.exists():
            self.load_memory()
    
    def load_memory(self) -> dict:
        """
        Load topic embeddings from JSON file.
        
        Returns:
            Dictionary mapping topic names to embedding vectors
        """
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
            return self.memory
        except (FileNotFoundError, json.JSONDecodeError):
            self.memory = {}
            return self.memory
    
    def save_memory(self) -> None:
        """
        Save topic embeddings to JSON file.
        """
        # Create parent directory if it doesn't exist
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
    
    def get_embedding(self, text: str) -> list[float]:
        """
        Get embedding vector for a text using SentenceTransformers.
        
        Args:
            text: Input text to embed
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Encode text and convert to list
            embedding = self.model.encode([text])[0]
            return embedding.tolist()
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return []
    
    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """
        Compute cosine similarity between two vectors.
        
        Args:
            vec1: First embedding vector
            vec2: Second embedding vector
        
        Returns:
            Cosine similarity score (0 to 1)
        """
        vec1_array = np.array(vec1)
        vec2_array = np.array(vec2)
        
        dot_product = np.dot(vec1_array, vec2_array)
        norm1 = np.linalg.norm(vec1_array)
        norm2 = np.linalg.norm(vec2_array)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def find_closest_topic(self, new_topic: str, threshold: float = 0.85) -> str | None:
        """
        Find the closest existing topic to a new topic phrase.
        
        Args:
            new_topic: New topic phrase to match
            threshold: Minimum cosine similarity threshold (default: 0.85)
        
        Returns:
            Existing topic name if similarity >= threshold, else None
        """
        if not self.memory:
            return None
        
        # Get embedding for new topic
        new_embedding = self.get_embedding(new_topic)
        if not new_embedding:
            return None
        
        # Find maximum similarity with existing topics
        max_similarity = 0.0
        closest_topic = None
        
        for topic_name, stored_embedding in self.memory.items():
            similarity = self.cosine_similarity(new_embedding, stored_embedding)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_topic = topic_name
        
        # Return closest topic if similarity meets threshold
        if max_similarity >= threshold:
            return closest_topic
        
        return None
    
    def register_topic(self, new_topic: str) -> str:
        """
        Register a new topic or return existing similar topic.
        
        Args:
            new_topic: New topic phrase to register
        
        Returns:
            Existing topic name if similar topic found, else the new topic name
        """
        # Check if similar topic already exists
        existing_topic = self.find_closest_topic(new_topic)
        
        if existing_topic:
            return existing_topic
        
        # Register new topic
        embedding = self.get_embedding(new_topic)
        if embedding:
            self.memory[new_topic] = embedding
            self.save_memory()
        
        return new_topic
