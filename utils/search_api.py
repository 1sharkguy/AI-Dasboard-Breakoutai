import os
import time
from serpapi import GoogleSearch
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for detailed logs
logger = logging.getLogger(__name__)

def search_entity(entity, prompt_template, serpapi_key):
    """
    Perform a web search for the given entity using SerpAPI.
    """
    query = prompt_template.format(entity=entity)
    params = {
        "q": query,
        "location": "Austin, Texas, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": serpapi_key
    }
    
    try:
        # Initialize GoogleSearch with parameters
        search = GoogleSearch(params)
        
        # Execute the search and get results
        results = search.get_dict()
        
        # Debug: Log the full results from SerpAPI
        logger.debug(f"Raw search results for '{query}': {results}")

        # Extract and return relevant information from the results
        output = []
        for result in results.get("organic_results", []):
            output.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet")
            })

        # Debug: Log the extracted output for verification
        logger.info(f"Extracted output for '{entity}': {output}")

        return output
    except Exception as e:
        logger.error(f"Error performing search for {entity}: {e}")
        return []

def search_entities(entities, prompt_template, serpapi_key):
    """
    Perform searches for each entity with rate limiting to avoid API rate limit issues.
    """
    results = {}
    for entity in entities:
        logger.info(f"Searching for entity: {entity}")
        results[entity] = search_entity(entity, prompt_template, serpapi_key)
        
        # Rate limiting (adjust based on SerpAPI rate limit policy)
        time.sleep(1)  # You may adjust this time or calculate based on actual rate limits

    logger.info("Completed all searches.")
    return results
