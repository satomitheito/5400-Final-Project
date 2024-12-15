from janas.src.janas.scrape_am.scrape_am_articles import fetch_and_save_articles
# "test_am_scrape, test_nhk_scrape, test_s_scrape, test_m_scrape, test_translate (check if all characters changed from japanese characters), test_sentiment_am (see if scores are produced for all 4 types), test_sentiment_ja"


def test_am_scrape():
    data = fetch_and_save_articles(
        {"Politics": "https://www.cnn.com/politics"}, "CNN", "Left", 1
    )
    assert len(data["link"]) != 0, "Link scrapping failed for article"
    assert len(data["content"]) != 0, "Article scrapping failed"


# def test_nhk_scrape():
#     pass

# def test_san_scrape():
#     pass

# def test_mai_scrape():
#     pass
