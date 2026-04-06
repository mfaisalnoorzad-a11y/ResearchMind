import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="articles")

def add_article(article_id: str, text: str):
    """Save article to database."""
    collection.upsert(
        ids=[article_id],
        documents=[text]
    )

def search(query: str, n_results: int = 5):
    """Search for saved articles in the database"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def remove_article(article_id: str):
    """delete saved articles from the database"""
    collection.delete(
        ids=[article_id]
    )