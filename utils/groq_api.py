import os
from groq import Groq

# Initialize the Groq client using the API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")
print(f"Initializing Groq client with API key: {api_key}")  # Debugging initialization
client = Groq(api_key=api_key)

def extract_information_with_groq(prompt, search_results):
    """
    Send search results to Groq's API to extract specific information based on the prompt.
    
    Args:
        prompt (str): The prompt describing the information to extract.
        search_results (list): List of search result dictionaries to analyze.

    Returns:
        dict: The response containing the extracted information or an error message.
    """
    try:
        print("Received prompt:", prompt)  # Debugging prompt input
        print("Received search results:", search_results)  # Debugging search results input
        
        # Format each search result as a string and join them with newlines
        formatted_results = "\n".join(
            f"Title: {result.get('title', 'N/A')}\nSnippet: {result.get('snippet', 'N/A')}"
            for result in search_results
        )
        print("Formatted search results for LLM:", formatted_results)  # Debugging formatted results

        # Combine the prompt and formatted search results into the message content
        message_content = f"{prompt}\n\n{formatted_results}"
        print("Message content sent to LLM:", message_content)  # Debugging message content

        # Create a chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
            model="llama3-8b-8192",
        )
        print("API response from LLM:", chat_completion)  # Debugging full API response

        # Extract the LLM's response from the chat completion result
        extracted_info = chat_completion.choices[0].message.content
        print("Extracted information from LLM:", extracted_info)  # Debugging extracted information
        return {"extracted_info": extracted_info}
    except Exception as e:
        print("Error during LLM extraction:", e)  # Debugging error
        return {"error": str(e)}
