import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
from datetime import date

class VergeScraper:
    def __init__(self):
        self.base_url = "https://www.theverge.com"
        self.article_urls = []
        self.article_data = []

    def get_article_urls(self):
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.text, "html.parser")
        divdata = soup.find('div', "h-full w-full lg:max-h-full lg:w-[380px] lg:pt-[174px]")
        articles = divdata.find("ol")
        for article in articles:
            url = article.find("a")["href"]
            self.article_urls.append(f"https://www.theverge.com{url}")

    def scrape_articles(self):
        for url in self.article_urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            article_heading = soup.find('h1')
            
            # extract article title
            headline = article_heading.text.strip()

            #extract authors
            authors_list = soup.find('div').find('p')
            authors = ""
            for author in authors_list:
                authors = authors.strip() + " " + author.text.strip()

            # extract date
            date_str = soup.find('time').text.strip()            
            article_id = hash(url)
            article = (int(article_id), url, headline, authors, date_str)
            print(article)
            self.article_data.append(article)

    def save_to_csv(self):
        filename = date.today().strftime("%d%m%Y") + "_verge.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "url", "headline", "author", "date"])
            for article in self.article_data:
                writer.writerow(article)

    def save_to_sqlite(self):
        conn = sqlite3.connect("verge_articles.db")
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                url TEXT,
                headline TEXT,
                author TEXT,
                date TEXT
            )
            """
        )
        for article in self.article_data:
            c.execute("INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", article)
        conn.commit()
        conn.close()

if __name__ == "__main__":
    scraper = VergeScraper()
    scraper.get_article_urls()
    scraper.scrape_articles()
    scraper.save_to_csv()
    scraper.save_to_sqlite()


