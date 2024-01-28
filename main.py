import streamlit as st
import pandas as pd
import textrazor
from serp_api_handler import SerpApiHandler
from config_loader import ConfigLoader
from entity_analyzer import EntityAnalyzer
from html_parser import HTMLParser

class WebEntityAnalyzerApp:
    def __init__(self):
        print("Initializing configuration...")
        self.config_loader = ConfigLoader()
        self.domains = self.config_loader.load_csv('data/Google_Domains.csv')
        self.countries = self.config_loader.load_csv('data/Google_Countries.csv')
        self.languages = self.config_loader.load_csv('data/Google_Languages.csv')
        self.html_parser = HTMLParser()
        self.entity_analyzer = None
        print("Configuration loaded.")

        # Fetch API keys from Streamlit secrets
        self.textrazor_api_key = st.secrets["TEXTRAZOR_API_KEY"]
        self.api_key = st.secrets["SERP_API_KEY"]

    def run(self):
        st.title('Entity Gap Analysis 🕸️🔍')
        st.write("This tool helps you analyze entities found in web content...")

        # Sidebar inputs
        target_url = st.sidebar.text_input("Enter target URL")
        query = st.sidebar.text_input("Enter search keywords")
        no_of_results = st.sidebar.slider("Number of results", 1, 100, 10)
        domain_selection = st.sidebar.selectbox('Select Domain', self.domains['domain'])
        country_selection = st.sidebar.selectbox('Select Country', self.countries['countryName'])
        language_selection = st.sidebar.selectbox('Select Language', self.languages['langName'])

        if query and st.button('Start Process 🚀'):
            self.entity_analyzer = EntityAnalyzer(self.textrazor_api_key)
            self.start_analysis(self.api_key, query, domain_selection, country_selection, language_selection, no_of_results, target_url)

    def extract_urls_from_serp(self, serp_json):
        print("Extracting URLs from SERP results...")
        urls = []
        for result in serp_json.get('organic_results', []):
            url = result.get('link')
            if url:
                print(f"Extracted URL: {url}")
                urls.append(url)
        print(f"Found {len(urls)} URLs.")
        return urls

    def start_analysis(self, api_key, query, domain, country, language, no_of_results, target_url):
        serp_results = SerpApiHandler.fetch_serp_data(query, api_key, domain, country, language, no_of_results)
        if serp_results:
            competitor_urls = self.extract_urls_from_serp(serp_results)
            comp_entities = self.entity_analyzer.get_entities(competitor_urls)

            comp_df = pd.DataFrame(comp_entities, columns=["URL", "Entity", "Relevance_Score", "Confidence_Score", "Freebase_Types", "Matched_Text", "Wikipedia_Link"])
            comp_df.sort_values(by=['Relevance_Score'], ascending=False, inplace=True)

            target_entities = self.entity_analyzer.get_entities([target_url])
            target_df = pd.DataFrame(target_entities, columns=["URL", "Entity", "Relevance_Score", "Confidence_Score", "Freebase_Types", "Matched_Text", "Wikipedia_Link"])
            target_df.sort_values(by=['Relevance_Score'], ascending=False, inplace=True)

            gap_df = comp_df[~comp_df['Entity'].isin(target_df['Entity'])]

            st.download_button('Download Competitor Entities', comp_df.to_csv(index=False), 'competitor_entities.csv', 'text/csv')
            st.download_button('Download Target Entities', target_df.to_csv(index=False), 'target_entities.csv', 'text/csv')
            st.download_button('Download Gap Analysis', gap_df.to_csv(index=False), 'gap_analysis.csv', 'text/csv')
        else:
            st.write("Failed to fetch data.")


if __name__ == '__main__':
    app = WebEntityAnalyzerApp()
    app.run()
