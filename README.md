
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.10-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-lightgrey)
![API](https://img.shields.io/badge/Gemini-2.0-ff8800)


# Review Trend AI

**Review Trend AI** is an intelligent analytics tool designed to extract, process, and analyze daily customer feedback trends from Google Play app reviews. By leveraging Large Language Models (LLMs), it transforms unstructured user reviews into actionable insights, helping product teams identify recurring issues like "delivery delay" or "food cold" and track their frequency over time.

---

## 🚀 Features

- **Automated Scraping**: Collects raw reviews from the Google Play Store for specified dates.
- **Intelligent Topic Extraction**: Uses Google's **Gemini 1.5 Flash** model to extract root-cause issues (e.g., "pricing", "missing items") from review text.
- **Topic Normalization**: Maps varied user phrases (e.g., "too expensive", "costly") into standardized categories for consistent tracking.
- **Daily Processing**: Aggregates and counts topic frequencies on a daily basis.
- **Trend Analysis**: Generates a longitudinal trend report (CSV) showing how specific issues evolve over time.

---

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **AI Model**: Google Gemini 1.5 Flash (via `google-genai` SDK)
- **Data Handling**: Pandas, JSON
- **Scraping**: `google-play-scraper` (assumed, based on standard usage)
- **Utilities**: `tqdm` for progress tracking

---

## 📂 Folder Structure

```
review_trend_ai/
├── data/
│   ├── raw/                 # Raw JSON reviews scraped from Play Store
│   └── processed/           # Preprocessed daily review files
├── output/
│   └── reports/             # Generated trend reports (trend.csv)
├── src/
│   ├── agents/
│   │   ├── topic_agent.py           # Gemini API integration for topic extraction
│   │   ├── daily_topic_processor.py # Normalizes topics and aggregates daily counts
│   │   ├── topic_memory.py          # Manages state of identified topics
│   │   └── trend_builder.py         # Compiles daily data into trend reports
│   └── utils/
│       ├── scraper.py               # Scrapes reviews from Google Play
│       └── preprocess.py            # Cleans and prepares raw text
├── main.py                  # Entry point for the application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/review_trend_ai.git
   cd review_trend_ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Key**:
   You need a Google Gemini API key to run the topic extraction.
   
   **Windows (PowerShell)**:
   ```powershell
   $env:GOOGLE_API_KEY="your_actual_api_key_here"
   ```
   
   **Linux/macOS**:
   ```bash
   export GOOGLE_API_KEY="your_actual_api_key_here"
   ```

---

## 🏃 Usage

### 1. Collect Reviews
Scrape reviews for a specific date range or app ID using the scraper utility.
*(Note: Ensure `src/utils/scraper.py` is configured with your target App ID)*

```bash
# Example usage (depending on implementation details in scraper.py)
python src/utils/scraper.py
```

### 2. Process Daily Reviews
Analyze reviews for a specific date to extract and count topics. This step calls the Gemini API for each review.

```bash
python main.py --mode day --date 2024-06-01
```

### 3. Generate Trend Report
Compile all processed daily data into a single trend report.

```bash
python main.py --mode trend
```

The output will be saved to `output/reports/trend.csv`.

---

## 📋 Sample Workflow

Here is how you might process a week's worth of data:

```powershell
# Process consecutive days
python main.py --mode day --date 2024-06-01
python main.py --mode day --date 2024-06-02
python main.py --mode day --date 2024-06-03
python main.py --mode day --date 2024-06-04
python main.py --mode day --date 2024-06-05

# Generate the final trend report
python main.py --mode trend
```

---

## 📊 Output Format

The generated `trend.csv` contains rows for each date and columns for each normalized topic.

| Date       | pricing | delivery delay | food cold | missing items | bad quality |
|------------|---------|----------------|-----------|---------------|-------------|
| 2024-06-01 | 15      | 8              | 12        | 3             | 5           |
| 2024-06-02 | 10      | 25             | 9         | 4             | 6           |
| 2024-06-03 | 18      | 5              | 11        | 2             | 4           |

---

## ⚠️ Limitations

- **API Quotas**: The Free Tier of Gemini API has rate limits (RPM/TPM). Processing large volumes of reviews may hit these limits, requiring a delay or paid plan.
- **Processing Speed**: LLM-based extraction is slower than keyword matching. Expect processing times of ~1-2 seconds per review.
- **Context Window**: Extremely long reviews might be truncated depending on the model's token limit (though usually sufficient for app reviews).

---

## 🚀 Future Improvements

- **Sentiment Analysis**: Integrate sentiment scoring alongside topic extraction.
- **Dashboarding**: Build a Streamlit or Dash frontend to visualize the `trend.csv` data interactively.
- **Parallel Processing**: Implement async API calls to speed up the daily processing step.
- **Multi-language Support**: Add support for non-English reviews using Gemini's translation capabilities.

---

## 🎓 Citation

If you use this project for academic or research purposes, please cite it as follows:

> **Review Trend AI**: An automated system for extracting customer feedback trends using Large Language Models. [Year]. [Repository URL].

---

## 👤 Author

**[Mohammad Arshad ALi]**  
*Student / Developer*  

