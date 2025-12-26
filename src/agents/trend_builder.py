import os
import glob
import pandas as pd
from src.agents.daily_topic_processor import process_day
import json


def build_trend_table(dates: list[str], memory_path: str = 'topic_memory.json') -> pd.DataFrame:
    """
    Build a trend table DataFrame showing topic frequencies across multiple days.
    
    Args:
        dates: List of date strings in format YYYY-MM-DD (e.g., ['2024-06-01', '2024-06-02'])
        memory_path: Path to topic memory JSON file (default: 'topic_memory.json')
    
    Returns:
        pandas DataFrame with topics as index (rows) and dates as columns (values = frequencies)
    """
    # Extract pure date strings from file paths
    dates = [os.path.basename(f).replace(".json", "") for f in glob.glob("data/processed/*.json")]
    
    # Clean dates - remove any path components that might have leaked in
    dates = [d.replace("processed\\", "").replace("processed/", "").strip() for d in dates]
    
    # Sort dates chronologically
    sorted_dates = sorted(dates)
    
    # Dictionary to store topic frequencies for each date
    all_topic_data = {}
    
    # Process each date
    for date_str in sorted_dates:
        processed_path = f"data/processed/{date_str}.json"
        try:
            with open(processed_path, "r", encoding="utf-8") as f:
                day_topics = json.load(f)  # this must load a dict of {topic: count}
                if not isinstance(day_topics, dict):
                    print(f"Invalid format in {processed_path}, skipping...")
                    continue
        except FileNotFoundError:
            print(f"Processed file not found: {processed_path}")
            continue
        all_topic_data[date_str] = day_topics
    
    # Collect all unique topics across all days
    all_topics = set()
    for day_topics in all_topic_data.values():
        all_topics.update(day_topics.keys())
    
    # Sort topics for consistent ordering
    sorted_topics = sorted(all_topics)
    
    # Build DataFrame
    # Initialize with zeros
    # Create DataFrame with topics as index and dates as columns
    df = pd.DataFrame(0, index=sorted_topics, columns=sorted_dates)
    
    # Populate DataFrame
    for date_str in sorted_dates:
        if date_str in all_topic_data:
            day_topics = all_topic_data[date_str]
            for topic, count in day_topics.items():
                if topic in df.index:
                    df.at[topic, date_str] = count

    # --- CLEAN COLUMN NAMES ---
    # remove any 'processed\' or 'processed/' prefix from column names
    df.columns = [c.replace("processed\\", "").replace("processed/", "").replace("processed", "").strip() for c in df.columns]
    # --------------------------------
    
    # Fill any missing values with 0 (shouldn't be needed, but just in case)
    df = df.fillna(0)
    
    # Ensure all values are integers
    df = df.astype(int)
    
    return df


def save_trend_table(df: pd.DataFrame, output_path: str = 'output/reports/trend.csv') -> None:
    """
    Save trend table DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame to save
        output_path: Path where CSV file will be saved (default: 'output/reports/trend.csv')
    """
    df.to_csv(output_path)
