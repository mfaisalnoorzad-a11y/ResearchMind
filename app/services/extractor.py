from trafilatura import fetch_url, extract

def extract_content(url: str) -> str:
    if url:
        downloaded = fetch_url(url)
        content = extract(downloaded)
        return content
    
    if not downloaded:
        return None
