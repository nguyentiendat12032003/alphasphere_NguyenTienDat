from scrape.scrape_articles import run_scraper
from vector_store.upload_attach import main as upload_and_attach

def main():
    print("====== Step 1: Scraping Zendesk articles ======")
    run_scraper()

    print("\n====== Step 2: Uploading and attaching to OpenAI Vector Store ======")
    upload_and_attach()

    print("\nAll done.")

if __name__ == "__main__":
    main()
