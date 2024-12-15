import pandas as pd
from janas.scrape_am.scrape_am_articles import fetch_and_save_articles
from janas.scrape_jp.scrape_jp import get_nhk_arts, get_sankei_arts, get_mainichi_arts
from janas.translation.translation import translate_articles
from janas.sentiment_scoring.sentiment import analyze_sentiment


def test_am_scrape():
    data = fetch_and_save_articles(
        {"Politics": "https://www.cnn.com/politics"}, "CNN", "Left", 1
    )
    assert len(data["link"]) != 0, "Link scraping failed for article"
    assert len(data["content"]) != 0, "Article scrapping failed"


def test_nhk_scrape():
    title, text = get_nhk_arts(
        "https://www3.nhk.or.jp/news/html/20241214/k10014667891000.html"
    )
    assert len(title) != 0, "Failed for scraping article title"
    assert len(text) != 0, "Failed for scraping article content"


def test_san_scrape():
    title, text = get_sankei_arts(
        "https://www.sankei.com/article/20241215-RP4KZNF4OZLFPDL2UD3UVRQTME/"
    )
    assert len(title) != 0, "Failed for scraping article title"
    assert len(text) != 0, "Failed for scraping article content"


def test_mai_scrape():
    title, text = get_mainichi_arts(
        "https://mainichi.jp/articles/20241214/k00/00m/030/134000c"
    )
    assert len(title) != 0, "Failed for scraping article title"
    assert len(text) != 0, "Failed for scraping article content"


def test_translate():
    title_m, text_m = get_mainichi_arts(
        "https://mainichi.jp/articles/20241214/k00/00m/030/134000c"
    )
    title_s, text_s = get_sankei_arts(
        "https://www.sankei.com/article/20241215-RP4KZNF4OZLFPDL2UD3UVRQTME/"
    )
    df = pd.DataFrame({"title": [title_m, title_s], "content": [text_m, text_s]})
    df = translate_articles(df)
    assert "translation" in df.columns, "Failed to make translation column"
    assert len(df["translation"].iloc[0]) > 0, "Translation unsuccessful"
    assert len(df["translation"].iloc[1]) > 0, "Translation unsuccessful"


def test_sentiment_am():
    data = fetch_and_save_articles(
        {"Politics": "https://www.cnn.com/politics"}, "CNN", "Left", 1
    )
    sent = analyze_sentiment(data["content"][0], "US")
    assert sent.isinstance(dict), "Sentiment analysis invalid"
    assert len(sent.keys()), "Not all sentiment scores returned"


def test_sentiment_jp():
    title, text = get_mainichi_arts(
        "https://mainichi.jp/articles/20241214/k00/00m/030/134000c"
    )
    sent = analyze_sentiment(text, "Japan")
    assert sent.isinstance(dict), "Sentiment analysis invalid"
    assert len(sent.keys()), "Not all sentiment scores returned"
