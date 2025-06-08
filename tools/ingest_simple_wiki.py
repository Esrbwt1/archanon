# tools/ingest_simple_wiki.py

import os
from datasets import load_dataset

def download_and_prepare_simple_wiki(output_dir: str, num_articles: int = 100):
    """
    Downloads the Simple Wikipedia dataset and saves a small subset to a text file.

    Args:
        output_dir (str): The directory to save the output file.
        num_articles (int): The number of articles to process.
    """
    print("Downloading Simple Wikipedia dataset from Hugging Face...")
    # Using 'streaming=True' is memory-efficient as it doesn't download the whole dataset at once.
    dataset = load_dataset("wikipedia", "20220301.simple", streaming=True, trust_remote_code=True)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "simple_wiki_corpus_v1.txt")
    
    print(f"Processing the first {num_articles} articles...")
    
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for article in dataset['train']:
            if count >= num_articles:
                break
            
            title = article['title']
            text = article['text']
            
            # Simple preprocessing: We'll just write the title and text.
            # More complex cleaning could happen here in a real pipeline.
            f.write(f"--- ARTICLE: {title} ---\n")
            f.write(text)
            f.write("\n\n")
            
            count += 1
            if count % 10 == 0:
                print(f"  ...processed {count}/{num_articles} articles.")

    print(f"\nSuccessfully created corpus file at: {output_path}")
    print(f"Total articles processed: {count}")

if __name__ == "__main__":
    # Define a directory to store our data corpora
    data_directory = "data_corpus"
    download_and_prepare_simple_wiki(output_dir=data_directory, num_articles=100)