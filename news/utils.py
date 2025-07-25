import requests
import feedparser
import time
import nltk
from datetime import datetime
from datetime import timezone as dt_timezone
from django.utils import timezone
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from newspaper import Article  # ✅ For full content

# Ensure required NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def clean_html(raw_html):
    """Strip HTML tags using BeautifulSoup."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)


def generate_summary(text,article_title="", num_sentences=3):
    """Generate a summary from the input text."""
    if not text or not isinstance(text, str):
        return "No content available to summarize."

    # 1. Tokenize into sentences
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    # 2. Tokenize into words and remove stopwords
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # 3. Calculate word frequencies
    word_frequencies = Counter(filtered_words)
    if article_title:
        title_words = word_tokenize(article_title.lower()) 
        for word in title_words: 
            if word in word_frequencies: 
                word_frequencies[word] += 0.5
    # 4. Score sentences
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[i] = sentence_scores.get(i, 0) + word_frequencies[word]
        if i == 0: # First sentence 
            if i in sentence_scores: sentence_scores[i] += 1.0 
            else: sentence_scores[i] = 1.0 # Or assign initial score if not yet scored 
        elif i == 1 and len(sentences) > 1: # Second sentence 
            if i in sentence_scores: sentence_scores[i] += 0.5 
            else: sentence_scores[i] = 0.5
    # 5. Get top N sentences by score
    summarized_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentences_indices = [index for index, _ in summarized_sentences[:num_sentences]]

    # Preserve original order
    final_summary_sentences = [sentences[i] for i in sorted(top_sentences_indices)]
    return " ".join(final_summary_sentences)


def fetch_news_from_rss(feed_url, source_name):
    """Fetch and clean full news content from RSS feed using newspaper3k and generate summaries."""
    articles_data = []

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

            # ✅ Fetch full article content using newspaper3k
            try:
                article = Article(link)
                article.download()
                article.parse()
                full_text = article.text
            except Exception as e:
                print(f"⚠️ Failed to fetch full article from {link}: {e}")
                full_text = entry.get('summary') or entry.get('description') or 'No content available.'

            cleaned_content = clean_html(full_text)
            summary = generate_summary(cleaned_content)

            articles_data.append({
                'title': title,
                'link': link,
                'content': cleaned_content,
                'summary': summary,
                'publication_date': published_date,
                'source': source_name
            })

        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching RSS feed from {source_name}: {e}")
        return []
    except Exception as e:
        print(f"❌ Error parsing RSS from {source_name}: {e}")
        return []
