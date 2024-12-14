import os
import pandas as pd
import logging
import ast
import datetime
from JANAS.scrape_jp.scrape_jp import get_articles as get_japanese_articles
from JANAS.scrape_am.scrape_am_articles import get_am_articles as get_american_articles
from JANAS.sentiment_scoring.sentiment import analyze_sentiment
from JANAS.translation.translation import translate_articles
#from JANAS.analysis.summarize import make_graphs as graph_generate

#loggins
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
        
        #scrape japanese artiles
        logger.info("Scraping Japanese articles")
        japanese_df = get_japanese_articles()
        current_time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        japanese_csv_path = os.path.join(data_folder_path, f"{current_time_stamp}_japanese_scraped_articles.csv")
        japanese_df.to_csv(japanese_csv_path, index=False)
        logger.info(f"Japanese articles saved to {japanese_csv_path}")

        #scrape american articles
        logger.info("Scraping American articles")
        american_df = get_american_articles()
        american_csv_path = os.path.join(data_folder_path, f"{current_time_stamp}_american_scraped_articles.csv")
        american_df.to_csv(american_csv_path, index=False)
        logger.info(f"American articles saved to {american_csv_path}")

        #add country columns
        logger.info("Adding country columns")
        japanese_df["Country"] = "Japan"
        american_df["Country"] = "US"

        #merging so we can parse one csv
        logger.info("Merging datasets")
        merged_df = pd.concat([japanese_df, american_df], ignore_index=True)

        #sentiment analysis on th emerged dataset
        logger.info("Sentiment analysis on merged dataset")

        merged_df["Sentiment"] = merged_df["content"].apply(analyze_sentiment)

        merged_df["Sentiment"] = merged_df["Sentiment"].apply(ast.literal_eval)
        sentiment_df = pd.json_normalize(merged_df["Sentiment"])
        sentiment_df = sentiment_df.reset_index(drop=True)
        sentiment_df = sentiment_df[['original_compound']]
        merged_df = merged_df.reset_index(drop=True)
        merged_df = pd.concat([merged_df.drop(columns=["Sentiment"]), sentiment_df], axis=1)

        merged_csv_path = os.path.join(data_folder_path, f"{current_time_stamp}_sentiment.csv")
        merged_df.to_csv(merged_csv_path, index=False)
        logger.info(f"Merged dataset with sentiment saved to {merged_csv_path}")

        #translate japanese articles
        logger.info("Translating Japanese articles")
        japanese_translated_df = translate_articles(japanese_df)
        logger.info("Performing sentiment analysis on translated content")

        #sentiment analysis on translated 
        japanese_translated_df["Translated_sentiment"] = japanese_translated_df["translation"].apply(analyze_sentiment)

        japanese_translated_df["Translated_sentiment"] = japanese_translated_df["Translated_sentiment"].apply(ast.literal_eval)
        t_sentiment_df = pd.json_normalize(japanese_translated_df["Translated_sentiment"])
        t_sentiment_df = t_sentiment_df.reset_index(drop=True)
        t_sentiment_df = t_sentiment_df[['translated_compound']]
        japanese_translated_df = japanese_translated_df.reset_index(drop=True)
        japanese_translated_df = pd.concat([japanese_translated_df.drop(columns=["Translated_sentiment"]), t_sentiment_df], axis=1)
        japanese_translated_df = pd.concat([merged_df, japanese_translated_df], ignore_index=True)

        translated_csv_path = os.path.join(data_folder_path, f"{current_time_stamp}_japanese_translated_sentiment.csv")
        japanese_translated_df.to_csv(translated_csv_path, index=False)
        logger.info(f"Japanese translated dataset saved to {translated_csv_path}")

        # Generate graphs/summaries
        #logger.info("Creating graphs")
        #graph_generate(merged_csv_path,translated_csv_path)

        logger.info("Finished")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
