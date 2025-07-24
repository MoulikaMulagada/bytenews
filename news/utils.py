import requests
import feedparser
import time
from datetime import datetime
from datetime import timezone as dt_timezone
from django.utils import timezone
from bs4 import BeautifulSoup

def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def fetch_news_from_rss(feed_url, source_name):
    articles_data = []  # ✅ You missed this earlier

    try:
        response = requests.get(
            feed_url,
            headers={'User-Agent': 'ByteNewsScraper/1.0'},
            timeout=10
        )
        response.raise_for_status()
        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            title = entry.title
            link = entry.link

            if hasattr(entry, 'published_parsed'):
                published_date = datetime.fromtimestamp(
                    time.mktime(entry.published_parsed),
                    tz=dt_timezone.utc
                )
            else:
                published_date = timezone.now()

            content = entry.get('summary', entry.get('description', 'No content available.'))
            cleaned_content = clean_html(content)

            articles_data.append({
                'title': title,
                'link': link,
                'content': cleaned_content,
                'publication_date': published_date,
                'source': source_name
            })

        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed from {source_name}: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during RSS parsing from {source_name}: {e}")
        return []