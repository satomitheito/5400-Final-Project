import os
import pandas as pd
import logging
from JANAS.scrape_jp.scrape_jp import get_articles as get_japanese_articles
from JANAS.scrape_am import get_am_articles as get_american_articles
from sentiment_scoring.sentiment import analyze_sentiment
from translation.translation import translate_articles
#from analysis.summarize import generate_graphs

logging.basicConfig(
    level=logging.INFO,
    filename="../../../logs.txt",
    filemode='w',
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__) 

if __name__ == "__main__":
    logger.info("Starting main program")

    data_folder_path = "../../data"
    #graph_folder_path = 

    try:

        logger.info("Scraping Japanese articles")
        japanese_df = get_japanese_articles()
        japanese_csv_path = os.path.join(data_folder_path, "japanese_scraped_articles.csv")
        japanese_df.to_csv(japanese_csv_path, index=False)
        logger.info(f"Japanese articles saved to {japanese_csv_path}")

        logger.info("Scraping American articles")
        american_df = get_american_articles()
        american_csv_path = os.path.join(data_folder_path, "american_scraped_articles.csv")
        american_df.to_csv(american_csv_path, index=False)
        logger.info(f"American articles saved to {american_csv_path}")

        logger.info("Adding country columns")
        japanese_df["Country"] = "Japan"
        american_df["Country"] = "US"

        logger.info("Merging datasets")
        merged_df = pd.concat([japanese_df, american_df], ignore_index=True)

        logger.info("Sentiment analysis on merged dataset")
        merged_df["Sentiment"] = merged_df["content"].apply(analyze_sentiment)
        merged_csv_path = os.path.join(data_folder_path, "merged_sentiment.csv")
        merged_df.to_csv(merged_csv_path, index=False)
        logger.info(f"Merged dataset with sentiment saved to {merged_csv_path}")

        logger.info("Translating Japanese articles")
        japanese_translated_df = translate_articles(japanese_df)
        logger.info("Performing sentiment analysis on translated content")
        japanese_translated_df["ranslated_sentiment"] = japanese_translated_df["translation"].apply(analyze_sentiment)
        translated_csv_path = os.path.join(data_folder_path, "japanese_translated_sentiment.csv")
        japanese_translated_df.to_csv(translated_csv_path, index=False)
        logger.info(f"Japanese translated dataset saved to {translated_csv_path}")

        # Generate graphs

    except Exception as e:
        logger.error(f"An error occurred: {e}")
