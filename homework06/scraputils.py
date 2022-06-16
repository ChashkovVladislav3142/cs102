from typing import Dict, List, Union

import requests
from bs4 import BeautifulSoup  # type: ignore

last_url = "https://news.ycombinator.com/newest"


def get_last_url() -> str:
    return last_url


def extract_news(parser: BeautifulSoup) -> List[Dict[str, Union[str, int]]]:
    """ Extract news from a given web page """
    news_list = []

    trs = parser.table.find("table", {"class": "itemlist"}).findAll("tr")
    for i in range(len(trs)):
        tr = trs[i]
        if tr.get("class") is not None and "athing" in tr.get("class"):
            i += 1
            info_tr = trs[i]

            title_link = tr.find("a", {"class": "storylink"})
            title = title_link.text
            title_href = title_link["href"]

            points_span = info_tr.find("span", {"class": "score"})
            points = int(points_span.text.replace(" points", "").replace(" point", ""))

            author_link = info_tr.find("a", {"class": "hnuser"})
            author = author_link.text

            comments_link = info_tr.findAll("a")[-1]
            comments = 0
            if comments_link.text.find("comment") != -1:
                comments = int(
                    comments_link.text.replace("\xa0comments", "").replace("\xa0comment", "")
                )

            news_list.append(
                {
                    "author": author,
                    "comments": comments,
                    "points": points,
                    "title": title,
                    "url": title_href,
                }
            )

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """ Extract next page URL """
    more_links = parser.find("a", {"class": "morelink"})
    return str(more_links["href"])


def get_news(url: str, n_pages: int = 1) -> List[Dict[str, Union[str, int]]]:
    global last_url

    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1

    last_url = url

    return news
