import json
import os
import re
from pathlib import Path


def clean_daily_reviews(input_path: str, output_path: str):
    """
    Clean daily review files by processing text and standardizing format.
    
    Args:
        input_path: Directory path containing input JSON files (e.g., 'data/raw')
        output_path: Directory path where cleaned JSON files will be saved (e.g., 'data/processed')
    
    Returns:
        None
    """
    # Create the output directory if it does not exist
    os.makedirs(output_path, exist_ok=True)
    
    # Get all JSON files in the input directory
    input_dir = Path(input_path)
    json_files = list(input_dir.glob('*.json'))
    
    # Process each JSON file
    for json_file in json_files:
        # Load reviews from the input file
        with open(json_file, 'r', encoding='utf-8') as f:
            reviews = json.load(f)
        
        # Clean each review
        cleaned_reviews = []
        for review in reviews:
            # Extract text and score (map 'content' to 'text')
            text = review.get('content') or review.get('text', '')
            score = review.get('score')
            
            # Skip if text or score is missing
            if not text or score is None:
                continue
            
            # Clean the text
            cleaned_text = clean_text(text)
            
            # Add cleaned review
            cleaned_reviews.append({
                'text': cleaned_text,
                'score': score
            })
        
        # Save cleaned reviews to output path with same filename
        output_file = Path(output_path) / json_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_reviews, f, indent=2, ensure_ascii=False)


def clean_text(text: str) -> str:
    """
    Clean text by converting to lowercase, stripping whitespace, 
    removing repeated newlines, and replacing emojis with space.
    
    Args:
        text: Input text to clean
    
    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace emojis with space
    # Using regex to match emoji patterns (Unicode ranges for emojis)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "\U00002700-\U000027BF"  # dingbats
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub(' ', text)
    
    # Remove repeated newlines (replace multiple newlines with single space)
    text = re.sub(r'\n+', ' ', text)
    
    # Strip extra whitespace (replace multiple spaces with single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    return text

