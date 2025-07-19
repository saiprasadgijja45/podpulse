import feedparser

RSS_FEEDS = [
    "https://talkpython.fm/episodes/rss",
    "https://pythonbytes.fm/episodes/rss",
    "https://feeds.simplecast.com/54nAGcIl"
]

def fetch_matching_episodes(keyword):
    keyword = keyword.lower()
    episodes = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            if keyword in title.lower() or keyword in summary.lower():
                episodes.append({
                    "title": title,
                    "description": summary[:200] + "...",
                    "link": entry.get("link", "")
                })
    return episodes
 
