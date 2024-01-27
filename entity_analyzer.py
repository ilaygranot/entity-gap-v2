import textrazor

class EntityAnalyzer:
    def __init__(self, api_key):
        textrazor.api_key = api_key

    def get_entities(self, urls):
        entities = []
        for url in urls:
            try:
                print(f"Processing URL with TextRazor: {url}")
                client = textrazor.TextRazor(extractors=["entities"])
                response = client.analyze_url(url)
                for entity in response.entities():
                    entities.append({
                        "URL": url,
                        "Entity": entity.id,
                        "Relevance_Score": entity.relevance_score,
                        "Confidence_Score": entity.confidence_score,
                        "Freebase_Types": ",".join(entity.freebase_types or []),
                        "Matched_Text": entity.matched_text,
                        "Wikipedia_Link": entity.wikipedia_link
                    })
                print(f"Extraction successful for URL: {url}")
            except Exception as e:
                print(f"Failed to extract entities for URL {url}: {e}")
        return entities
