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
        if divdata is not None:
            articles = divdata.find("ol")
            for article in articles:
                url = article.find("a")["href"]
                self.article_urls.append(f"https://www.theverge.com{url}")

    def scrape_articles(self):
        if len(self.article_urls)>0:
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
                date_raw = soup.find('time').text.strip().split(",")
                date_str = date_raw[0] + date_raw[1]

                # create an tuple object of each article                
                article_id = hash(url)
                article = (int(article_id), url, headline, authors, date_str)
                self.article_data.append(article)
        else:
            return "NO ARTICLES FOUND!"

    def save_to_csv(self):
        filename = date.today().strftime("%d%m%Y") + "_verge.csv"
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                csvwriter = csv.writer(f)
                csvwriter.writerow(["id", "url", "headline", "author", "date"])
                for article in self.article_data:
                    csvwriter.writerow(article)

        except:
            return "ERROR SAVING CSV"
        
    def save_to_sqlite(self):
        try:
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

        except:
            return "ERROR SAVING ARTICLES IN DB"

if __name__ == "__main__":
    scraper = VergeScraper()
    scraper.get_article_urls()
    scraper.scrape_articles()
    scraper.save_to_csv()
    scraper.save_to_sqlite()


