import requests
from bs4 import BeautifulSoup

def scrape_news_by_url(url, keyword):
    # Make an HTTP request
    response = requests.get(url)

    if response.status_code == 200:
  
        soup = BeautifulSoup(response.content, 'lxml')

        
        articles = soup.find_all('div', class_='VXBf7')

        matching_headlines = []
        for article in articles:
            headline = article.find('div', class_='fHv_i').find('span').text.strip()
            time = article.find('div', class_='ZxBIG').text.strip()

            # Check if the keyword is present in the headline
            if keyword.lower() in headline.lower():
                matching_headlines.append({'headline': headline, 'time': time})

        return matching_headlines

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Example Usage
url = "https://timesofindia.indiatimes.com/topic/layoffs/news"
keyword = "layoff"

result = scrape_news_by_url(url, keyword)

if result:
    for article in result:
        print(f"Headline: {article['headline']}")
        print(f"Time: {article['time']}")
        print("\n")
        # print(article)
