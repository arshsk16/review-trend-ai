import json
import os
from collections import Counter
from tqdm import tqdm

from src.agents.topic_agent import extract_topic_phrases
from src.agents.topic_memory import TopicMemory

TOPIC_MAP = {
    "pricing": ["price", "expensive", "high price", "overpriced", "cost", "value for money", "affordable"],
    "delivery delay": ["late", "delay", "slow", "waiting", "wait time", "delivery time", "not on time"],
    "food cold": ["cold", "not hot", "temperature", "chilled", "food arrived cold"],
    "small quantity": ["small", "less", "portion", "quantity", "not enough", "insufficient"],
    "missing items": ["missing", "not received", "forgot", "item not delivered", "incomplete"],
    "no coupons": ["no offer", "no coupon", "no discount", "no promo"],
    "good quality": ["good", "excellent", "nice", "tasty", "quality maintained"],
    "bad quality": ["bad", "poor", "stale", "burnt", "not good", "worse"],
}

def normalize_topic(raw_topic: str) -> str:
    raw_topic = raw_topic.lower()
    for canonical, keywords in TOPIC_MAP.items():
        for kw in keywords:
            if kw in raw_topic:
                return canonical
    return None

def process_day(date_str: str, input_dir: str = 'data/processed', memory_path: str = 'topic_memory.json') -> dict[str, int]:
    """
    Process reviews for a specific day, extract topics, and count topic frequencies.
    
    Args:
        date_str: Date string in format YYYY-MM-DD (e.g., '2024-06-01')
        input_dir: Directory containing processed review JSON files (default: 'data/processed')
        memory_path: Path to topic memory JSON file (default: 'topic_memory.json')
    
    Returns:
        Dictionary mapping stable topic names to their frequency counts for that day
    """
    # Construct file path
    file_path = os.path.join(input_dir, f"{date_str}.json")
    
    # Load reviews from JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return {}
    
    # Collect all topics
    topics = []
    
    # Process each review with progress bar
    for review in tqdm(reviews, desc=f"Processing {date_str}"):
        # Get review text
        review_text = review.get('text', '')
        
        if not review_text:
            continue
        
        # Extract topic phrases from review
        extracted_phrases = extract_topic_phrases(review_text)
        
        # Map each phrase to canonical topic name and add to list
        for phrase in extracted_phrases:
            if phrase:  # Skip empty phrases
                normalized = normalize_topic(phrase)
                if normalized:    # ignore unmatched topics
                    topics.append(normalized)
    
    # Count topic frequencies using Counter
    topic_counts = Counter(topics)
    
    # Return as dict
    return dict(topic_counts)
