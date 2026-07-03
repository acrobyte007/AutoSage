import dotenv
import os
from tavily import TavilyClient

dotenv.load_dotenv()

def search_and_extract_tavily(query, max_results=5):
    """
    Search using Tavily and extract only URL and content from results.
    
    Args:
        query (str): The search query
        max_results (int): Maximum number of results to return (default: 5)
        
    Returns:
        List of dictionaries with 'url' and 'content' keys
    """
    api_key = os.getenv("TEVELI_API_KEY")
    if not api_key:
        raise ValueError("TEVELI_API_KEY not found in environment variables")
    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search(
        query,
        max_results=max_results
    )
    simplified_results = []
    
    for result in response.get('results', []):
        simplified_results.append({
            'url': result.get('url', ''),
            'content': result.get('content', '')
        })
    
    return simplified_results

# Usage example:
if __name__ == "__main__":
    try:
        results = search_and_extract_tavily("Who is Leo Messi?")
        
        for i, item in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"URL: {item['url']}")
            print(f"Content: {item['content']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")