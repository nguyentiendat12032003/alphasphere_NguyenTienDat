import requests
import os
from bs4 import BeautifulSoup
import re
from datetime import datetime

def html_to_markdown(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["nav", "header", "footer", "aside"]):  # Remove UI noise
        tag.decompose()

    for i in range(1, 7):  # Headings
        for tag in soup.find_all(f'h{i}'):
            tag.insert_before(f'\n{"#"*i} {tag.get_text()}\n')
            tag.decompose()

    for pre in soup.find_all("pre"):  # Code blocks
        code = pre.get_text()
        pre.replace_with(f"\n```\n{code}\n```\n")

    for code in soup.find_all("code"):  # Inline code
        code.replace_with(f"`{code.get_text()}`")

    for a in soup.find_all("a", href=True):  # Links
        text = a.get_text()
        href = a["href"]
        a.replace_with(f"[{text}]({href})")

    markdown = soup.get_text()
    return markdown.strip()

def slugify(title):
    return re.sub(r'\W+', '-', title.lower()).strip('-')

def fetch_articles(max_articles=30):
    url = "https://optisignshelp.zendesk.com/api/v2/help_center/en-us/articles.json"
    articles = []
    while url and len(articles) < max_articles:
        print(f"\nFetching URL: {url}")
        res = requests.get(url)
        if res.status_code != 200:
            print("Failed to fetch:", res.status_code)
            break

        data = res.json()
        new_articles = data.get("articles", [])
        articles.extend(new_articles)

        if len(articles) >= max_articles:
            break
        url = data.get("next_page")

    return articles[:max_articles]

def save_article(article, directory="articles"):
    title = article["title"]
    slug = slugify(title)
    print(f"Saving: {title}")
    body = html_to_markdown(article.get("body", ""))
    
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(body)

def run_scraper():
    print("Running full scraper for 30 articles...")
    all_articles = fetch_articles(max_articles=30)

    for article in all_articles:
        save_article(article, directory="articles")

    print("\nDetecting 10 most recently updated articles...")
    latest_articles = sorted(all_articles, key=lambda x: x.get("updated_at", ""), reverse=True)[:10]

    for article in latest_articles:
        save_article(article, directory="articles")

if __name__ == "__main__":
    run_scraper()
