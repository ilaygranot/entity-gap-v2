import requests

class SerpApiHandler:
    @staticmethod
    def fetch_serp_data(query, api_key, domain, country, language, no_of_results):
        endpoint = f"https://api.spaceserp.com/google/search?apiKey={api_key}&q={query}&domain={domain}&gl={country}&hl={language}&pageSize={no_of_results}&resultBlocks=organic_results"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            return None
