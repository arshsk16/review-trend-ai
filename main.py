import argparse
import os
import glob
from src.utils.preprocess import clean_daily_reviews
from src.agents.daily_topic_processor import process_day
from src.agents.trend_builder import build_trend_table, save_trend_table

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Trend Agent Runner")
    parser.add_argument("--mode", type=str, required=True,
                        choices=["clean", "day", "trend"],
                        help="clean = preprocess raw reviews, day = extract topics for a single day, trend = build trend across all days")

    parser.add_argument("--date", type=str, help="Date format YYYY-MM-DD for mode=day")

    args = parser.parse_args()

    if args.mode == "clean":
        clean_daily_reviews("data/raw", "data/processed")
        print("Cleaning complete.")

    elif args.mode == "day":
        if not args.date:
            raise ValueError("Please provide --date for day mode")
        result = process_day(args.date, "data/processed")
        print(result)

    elif args.mode == "trend":
        dates = [os.path.basename(f).replace(".json", "") for f in glob.glob("data/processed/*.json")]
        df = build_trend_table(dates)
        save_trend_table(df)
        print("Trend table saved to output/reports/trend.csv")

