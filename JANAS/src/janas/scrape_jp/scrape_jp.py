from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import logging

logger = logging.getLogger(__name__)

mainichi_topics = {
    "America": "https://mainichi.jp/north-america/",
    "Business": "https://mainichi.jp/enterprise/",
    "Politics": "https://mainichi.jp/policy/",
    "International": "https://mainichi.jp/asia-oceania/",
}

nhk_topics = {
    "Trending": "https://www3.nhk.or.jp/news/catnew.html",
    "Politics": "https://www3.nhk.or.jp/news/cat04.html",
    "International": "https://www3.nhk.or.jp/news/cat06.html",
    "Business": "https://www3.nhk.or.jp/news/business.html",
    "America": "https://www3.nhk.or.jp/news/word/0002362.html",
}

sankei_topics = {
    "International": "https://www.sankei.com/world/",
    "Business": "https://www.sankei.com/economy/business",
    "Politics": "https://www.sankei.com/politics/",
    "Trending": "https://www.sankei.com/flash/",
    "America": "https://www.sankei.com/world/america/",
}


def get_mainichi_art_urls(src_url):
    """
    Function to get list of article urls from topic page of Mainichi
    Return: URL to article
    """
    response = requests.get(src_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    url = soup.find("ul", class_="articlelist is-tophorizontal js-morelist")
    articles = []
    for a in url.find_all("a", href=True):
        article_url = a["href"][2:]
        articles.append("https://" + article_url)
    return articles


def get_sankei_art_urls(src_url):
    """
    Function to get list of articles from topic page of sankey
    """
    response = requests.get(src_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    url = soup.find_all(
        "article",
        class_="storycard border-bottom border-color-gray flex margin-bottom padding-bottom small-size col-item",
    )
    articles = []
    for u in url:
        a = u.find("a", href=True)
        article_url = a["href"]
        if article_url[:8] == "/article":
            articles.append(article_url)

    return articles


def get_nhk_art_urls(src_url):
    """
    Function to get list of articles from topic page of nhk
    """
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    try:
        # Open the target webpage
        driver.get(src_url)
        # Wait for the page to load (you can use WebDriverWait for more robust handling)
        time.sleep(3)
        # Find all the article links using XPath
        elements = driver.find_elements(
            By.XPATH, '//ul[@class="content--list grid--col-single"]/li/dl/dt/a'
        )
        # Extract the href attribute from each element
        article_links = [element.get_attribute("href") for element in elements]
        return article_links

    except Exception as e:
        logger.info("An error occurred:", e)
        return []

    finally:
        # Close the browser
        driver.quit()


def get_urls(topic_dict, src):
    """
    Get URLs from a topic dictionary
    """
    data = {"link": [], "source": [], "bias": [], "topic": []}
    for topic in topic_dict.keys():
        if src == "mainichi":
            logger.info("getting urls for mainichi " + topic)
            for article in get_mainichi_art_urls(topic_dict[topic]):
                data["link"].append(article)
                data["source"].append(src)
                data["bias"].append("left")
                data["topic"].append(topic)
        elif src == "nhk":
            logger.info("getting urls for nhk " + topic)
            for article in get_nhk_art_urls(topic_dict[topic]):
                data["link"].append(article)
                data["source"].append(src)
                data["bias"].append("neutral")
                data["topic"].append(topic)

        elif src == "sankei":
            logger.info("getting urls for sankei " + topic)
            for article in get_sankei_art_urls(topic_dict[topic]):
                data["link"].append("https://www.sankei.com" + article)
                data["source"].append(src)
                data["bias"].append("right")
                data["topic"].append(topic)
    return data


def get_mainichi_arts(article_url):
    """
    Function to get article from an article link from mainichi
    """
    logger.info("Parsing URL")
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    all_content = ""
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    all_content += title

    content_div = soup.find("section", class_="articledetail-body")
    if content_div:
        paragraphs = content_div.find_all("p")
        content_string = ""
        for p in paragraphs:
            content_string += p.get_text(strip=True)

        all_content += content_string
    else:
        all_content += "No content found in the article body."

    logger.info("Extracted URL successfully.")
    return title, all_content


def get_nhk_arts(article_url):
    """
    Function to get article from an article link from nhk
    """
    logger.info("Parsing URL")
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    all_content = ""
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    all_content += title
    # Extract the content inside the specific div and section
    content_div = soup.find("div", class_="content--detail-more")
    if content_div:
        body_section = content_div.find_all("section", class_="content--body")
        if body_section:
            for body in body_section:
                titles = body.find("h2", class_="body-title")
                body_text = body.find("div", class_="body-text")
                if body_text:
                    content_string = ""
                    for p in body_text.find("p"):
                        content_string += p.get_text(strip=True)
                if titles:
                    titles = titles.get_text()
                    all_content += titles
                if content_string:
                    all_content += content_string

    logger.info("Extracted URL")
    return title, all_content


def get_sankei_arts(article_url):
    """
    Function to get article from an article link from sankei
    """
    logger.info("Parsing URL")
    response = requests.get(article_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    all_content = ""
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    all_content += title
    content_div = soup.find("div", class_="article-body clearfix")
    if content_div:
        paragraphs = content_div.find_all("p", class_="article-text")
        content_string = ""
        for p in paragraphs:
            content_string += p.get_text(strip=True)

        all_content += content_string
    else:
        all_content += "No content found in the article body.\n"
    logger.info("Extracted URL successfully.")
    return title, all_content


def get_article_dict(topic_dict, src):
    """
    Function to get all articles from collected urls
    """
    if src == "mainichi":
        mainichi_art_urls = get_urls(topic_dict, "mainichi")
        mainichi_art_urls["title"] = []
        mainichi_art_urls["content"] = []
        for article in mainichi_art_urls["link"]:
            logger.info("Getting content for mainichi article at " + article)
            title, content = get_mainichi_arts(article)
            mainichi_art_urls["title"].append(title)
            mainichi_art_urls["content"].append(content)
        return mainichi_art_urls
    elif src == "nhk":
        nhk_arts_urls = get_urls(topic_dict, "nhk")
        nhk_arts_urls["title"] = []
        nhk_arts_urls["content"] = []
        for article in nhk_arts_urls["link"]:
            logger.info("Getting content for nhk article at " + article)
            title, content = get_nhk_arts(article)
            nhk_arts_urls["title"].append(title)
            nhk_arts_urls["content"].append(content)
        return nhk_arts_urls
    elif src == "sankei":
        sankei_arts_urls = get_urls(topic_dict, "sankei")
        sankei_arts_urls["title"] = []
        sankei_arts_urls["content"] = []
        for article in sankei_arts_urls["link"]:
            logger.info("Getting content for sankei article at " + article)
            title, content = get_sankei_arts(article)
            sankei_arts_urls["title"].append(title)
            sankei_arts_urls["content"].append(content)
        return sankei_arts_urls
    else:
        return None


def get_articles():
    """
    Function to get all articles from topic dictionaries
    """
    mainichi_arts = get_article_dict(mainichi_topics, "mainichi")
    mainichi_df = pd.DataFrame(mainichi_arts)
    nhk_arts = get_article_dict(nhk_topics, "nhk")
    nhk_df = pd.DataFrame(nhk_arts)
    sankei_arts = get_article_dict(sankei_topics, "sankei")
    sankei_df = pd.DataFrame(sankei_arts)

    all_jap_news = pd.concat([mainichi_df, nhk_df, sankei_df], ignore_index=True)
    return all_jap_news
