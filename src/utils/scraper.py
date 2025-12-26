import json
import os
from datetime import datetime
from collections import defaultdict
from google_play_scraper import reviews, Sort


def fetch_and_save_reviews(package_id: str, save_path: str, max_reviews: int = 2000):
    """
    Fetch Google Play Store reviews and save them grouped by date.
    
    Args:
        package_id: The package ID of the app (e.g., 'com.example.app')
        save_path: Directory path where JSON files will be saved
        max_reviews: Maximum number of reviews to fetch (default: 2000)
    
    Returns:
        None
    """
    # Create the directory if it does not exist
    os.makedirs(save_path, exist_ok=True)
    
    # Fetch reviews using google_play_scraper
    result, continuation_token = reviews(
        package_id,
        lang='en',  # Language code
        country='in',  # Country code
        count=max_reviews,
        sort=Sort.NEWEST
    )
    
    # Group reviews by date
    reviews_by_date = defaultdict(list)
    
    for review in result:
        # Ignore reviews without 'at' or 'content'
        if 'at' not in review or 'content' not in review:
            continue
        
        # Extract fields: content, score, at (date)
        content = review.get('content')
        score = review.get('score')
        at = review.get('at')
        
        # Convert date to YYYY-MM-DD format
        if isinstance(at, datetime):
            date_str = at.strftime('%Y-%m-%d')
        elif isinstance(at, str):
            # If it's a string, try to parse it
            try:
                date_obj = datetime.fromisoformat(at.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d')
            except (ValueError, AttributeError):
                continue
        else:
            continue
        
        # Add review to the date group
        reviews_by_date[date_str].append({
            'content': content,
            'score': score,
            'at': date_str
        })
    
    # Save each day's reviews into separate JSON files
    for date_str, day_reviews in reviews_by_date.items():
        filename = f"{date_str}.json"
        filepath = os.path.join(save_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(day_reviews, f, indent=2, ensure_ascii=False)

