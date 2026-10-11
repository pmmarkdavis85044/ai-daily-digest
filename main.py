import feedparser
import json
from datetime import datetime
from typing import List, Dict

# Simple LLM call simulation (replace with actual API call)
def summarize_with_llm(items: List[Dict]) -> str:
    # In a real implementation, call your LLM here (e.g., OpenAI, Ollama)
    # For demo, just return first few titles
    return " | ".join([item['title'] for item in items[:3]])

# Fetch and parse RSS feeds
def fetch_rss(feed_urls: List[str]) -> List[Dict]:
    items = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # limit per feed
            items.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', '')
            })
    return items

# Generate daily digest content
def generate_digest(feed_urls: List[str]) -> str:
    print(f"[{datetime.now().isoformat()}] Fetching feeds...")
    items = fetch_rss(feed_urls)
    print(f"Fetched {len(items)} items")
    
    # Sort by published date (newest first)
    items.sort(key=lambda x: x.get('published', ''), reverse=True)
    
    # Summarize with LLM
    summary = summarize_with_llm(items)
    
    # Compose digest
    digest_lines = [
        "# Daily AI Digest",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Top Stories",
        summary,
        "",
        "## Full List",
        *[f"- {item['title']} ({item['link']})" for item in items[:10]]
    ]
    return "\n".join(digest_lines)

# Demo usage
def main():
    rss_feeds = [
        "https://hnrss.org/frontpage",  # Hacker News
        "https://www.reddit.com/r/MachineLearning/.rss"  # ML subreddit
    ]
    digest = generate_digest(rss_feeds)
    with open("daily_digest.md", "w") as f:
        f.write(digest)
    print("Digest saved to daily_digest.md")

if __name__ == "__main__":
    main()