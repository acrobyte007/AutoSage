from exa_py import Exa
import dotenv

dotenv.load_dotenv()

def search_and_extract(query, num_results=3):
    """
    Search for content and extract only URL and Highlights.
    
    Args:
        query (str): The search query
        num_results (int): Number of results to return (default: 3)
        
    Returns:
        List of dictionaries with 'url' and 'highlights' keys
    """
    exa = Exa()
    result = exa.search(
        query,
        type="auto",
        contents={"highlights": True},
        num_results=num_results
    )
    simplified_results = []
    for item in result.results:
        simplified_results.append({
            'url': item.url,
            'highlights': item.highlights if hasattr(item, 'highlights') else []
        })
    
    return simplified_results

# Usage example:
if __name__ == "__main__":
    results = search_and_extract("blog post about artificial intelligence")
    for i, item in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"URL: {item['url']}")
        print(f"Highlights: {item['highlights']}")
        print("-" * 50)