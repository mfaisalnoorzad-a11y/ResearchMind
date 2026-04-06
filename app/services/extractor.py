from trafilatura import fetch_url, extract

def extract_content(url: str) -> str:
    """Extract article text content from a URL."""
    if url:
        downloaded = fetch_url(url)
        if not downloaded:
            return None
        content = extract(downloaded)
        return content
    
    return None
