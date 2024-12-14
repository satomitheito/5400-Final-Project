import pandas as pd
import newspaper
import logging

# Initialize Logger
logger = logging.getLogger(__name__)


def fetch_and_save_articles(sections, source_name, bias):
    """
    Function to fetch articles from a section and return final df for pipeline

    Inputs: 
    - sections --> dictionary of links to parse
    - source_name --> name of news source to include
    - bias --> string indicating the bias of the source
    """
    data = {
        "link": [],
        "source": [],
        "bias": [],
        "topic": [],
        "title": [],
        "content": []
    }

    # Using `newspaper`, iterate over the links
    for section, section_url in sections.items():
        logger.info(f"Fetching articles from {source_name} - {section} at {section_url}")

        try:
            # Build Newspaper
            newspaper_section = newspaper.build(section_url, memoize_articles = False)
            
            
            articles = newspaper_section.articles[5:35]

            # Iterate over the articles within the Newspaper
            for article in articles:
                # Create Article Object
                article.download()
                article.parse()
                article.nlp()
                article_url = article.url
                title = article.title
                content = article.text
                

                # Replace newlines with just spaces
                content = content.replace("\n", " ")

                if title and content:
                    data["link"].append(article_url)
                    data["source"].append(source_name)
                    data["bias"].append(bias)
                    data["topic"].append(section)
                    data["title"].append(title)
                    data["content"].append(content)
                   
            
        except Exception as e:
            logger.info(f"Error processing section {section_url}: {e}")

    return data  

    

# Main function to scrape articles from NHK and CNN
def get_am_articles():
    """
    Utility function to scrape american articles
    """
   
    # Define Sections with Links to parse through
    cnn_sections = {
        "Trending": "https://www.cnn.com/us",
        "Politics": "https://www.cnn.com/politics",
        "International": "https://www.cnn.com/world",
        "Business": "https://www.cnn.com/business",
        "Japan": "https://www.cnn.com/world/asia/japan"
    }

    huff_sections = {
        "Trending": "https://www.huffpost.com/news/", 
        "Politics": "https://www.huffpost.com/news/politics",
        "International": "https://www.huffpost.com/topic/international", 
        "Business": "https://www.huffpost.com/impact/business", 
        "Japan": "https://www.huffpost.com/news/topic/japan"
    }

    fox_sections = {
        "Trending": "https://www.foxnews.com/category/topic/trending-news", 
        "Politics": "https://www.foxnews.com/politics",
        "International": "https://www.foxnews.com/world", 
        "Business": "https://www.foxbusiness.com/economy", 
        "Japan": "https://www.foxnews.com/category/world/world-regions/japan"
    }

    logger.info("Fetching CNN articles...")
    cnn_art = fetch_and_save_articles(cnn_sections, "CNN", "left")

    logger.info("Fetching Huffington Post articles...")
    huff_art = fetch_and_save_articles(huff_sections, "Huffington Post", "neutral")

    logger.info("Fetching Fox News articles...")
    fox_art = fetch_and_save_articles(fox_sections, "Fox News", "right")

    # Combine all data dictionaries into a single DataFrame
    cnn_df = pd.DataFrame(cnn_art)
    huff_df = pd.DataFrame(huff_art)
    fox_df = pd.DataFrame(fox_art)

    all_eng_news = pd.concat([cnn_df, huff_df, fox_df], ignore_index=True)


    # Return final dataframe
    return all_eng_news