import requests
from bs4 import BeautifulSoup
from datetime import datetime

# function to get the page content
def get_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    content = response.content
    return content


# function to scrape theverge.com
def scrape(self):
    url = 'https://www.theverge.com/'
    content = get_page_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        try:
            url = article.find('a', class_='c-entry-box--compact__image-wrapper')['href']
            headline = article.find('h2', class_='c-entry-box--compact__title').text
            author = article.find('span', class_='c-byline__item').text
            date = article.find('time')['datetime']
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y/%m/%d')
            self.articles.append({
                'url': url,
                'headline': headline,
                'author': author,
                'date': date
            })
        except:
            
            pass


# testing
# print(get_page_content("https://www.theverge.com/"))  
