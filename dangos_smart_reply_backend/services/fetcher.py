import httpx

def fetch_html(value: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = httpx.get(value, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text
