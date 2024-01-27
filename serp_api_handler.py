import requests
from time import sleep
import backoff

class SerpApiHandler:
    @staticmethod
    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.RequestException, requests.exceptions.HTTPError),
                          max_tries=5)
    def fetch_serp_data(query, api_key, domain, country, language, no_of_results):
        endpoint = f"https://api.spaceserp.com/google/search?apiKey={api_key}&q={query}&domain={domain}&gl={country}&hl={language}&pageSize={no_of_results}&resultBlocks=organic_results"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()  # Raise an exception for HTTP error codes
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # HTTP error
        except requests.exceptions.RequestException as req_err:
            print(f"Other error occurred: {req_err}")  # Other errors like network error, etc.
        return None
