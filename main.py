import streamlit as st
import pandas as pd
from serp_api_handler import SerpApiHandler
from config_loader import ConfigLoader
from entity_analyzer import EntityAnalyzer
from html_parser import HTMLParser

class WebEntityAnalyzerApp:
    def __init__(self):
        self.config_loader = ConfigLoader()
        self.domains = self.config_loader.load_csv('data/Google Domains.csv')
        self.countries = self.config_loader.load_csv('data/Google Countries.csv')
        self.languages = self.config_loader.load_csv('data/Google Languages.csv')
        self.html_parser = HTMLParser()
        self.entity_analyzer = None  # Initialized during user input

    def run(self):
        st.title('Entity Gap Analysis 🕸️🔍')
        st.write("This tool helps you analyze entities found in web content...")

        # Sidebar for user input
        textrazor_api_key = st.sidebar.text_input("Enter your TextRazor API key")
        api_key = st.sidebar.text_input("Enter your SERP API key")
        target_url = st.sidebar.text_input("Enter target URL")
        query = st.sidebar.text_input("Enter search keywords")
        no_of_results = st.sidebar.slider("Number of results", 1, 100, 10)
        domain_selection = st.sidebar.selectbox('Select Domain', self.domains['Domain'])
        country_selection = st.sidebar.selectbox('Select Country', self.countries['Country'])
        language_selection = st.sidebar.selectbox('Select Language', self.languages['Language'])

        if textrazor_api_key and st.button('Start Process 🚀'):
            self.entity_analyzer = EntityAnalyzer(textrazor_api_key)
            self.start_analysis(api_key, query, domain_selection, country_selection, language_selection, no_of_results, target_url)
        elif not textrazor_api_key:
            st.error("Please provide a valid TextRazor API key.")

    def extract_urls_from_serp(self, serp_json):
        urls = []
        if 'organic_results' in serp_json:
            for result in serp_json['organic_results']:
                if 'url' in result:
                    urls.append(result['url'])
        return urls

    def start_analysis(self, api_key, query, domain, country, language, no_of_results, target_url):
        serp_results = SerpApiHandler.fetch_serp_data(query, api_key, domain, country, language, no_of_results)
        if serp_results:
            urls = self.extract_urls_from_serp(serp_results)
            # Fetch entities for all competitor URLs
            comp_entities = self.entity_analyzer.analyze_entities(urls)

            comp_df = pd.DataFrame(comp_entities,
                                   columns=["URL", "Entity", "Relevance_Score", "Confidence_Score", "Freebase_Types",
                                            "Matched_Text", "Wikipedia_Link"])
            comp_df.sort_values(by=['Relevance_Score'], ascending=False, inplace=True)

            # Fetch entities for the target URL separately
            target_entities = self.entity_analyzer.analyze_entities([target_url])
            target_df = pd.DataFrame(target_entities,
                                     columns=["URL", "Entity", "Relevance_Score", "Confidence_Score", "Freebase_Types",
                                              "Matched_Text", "Wikipedia_Link"])
            target_df.sort_values(by=['Relevance_Score'], ascending=False, inplace=True)

            # Perform gap analysis
            gap_df = comp_df[~comp_df['Entity'].isin(target_df['Entity'])]

            st.write("Process completed successfully! 🎉")

            # Provide download buttons for the DataFrames
            st.download_button('Download comp_df', comp_df.to_csv(index=False), 'comp_df.csv', 'text/csv')
            st.download_button('Download target_df', target_df.to_csv(index=False), 'target_df.csv', 'text/csv')
            st.download_button('Download gap_df', gap_df.to_csv(index=False), 'gap_df.csv', 'text/csv')
        else:
            st.write("Failed to fetch data.")

if __name__ == '__main__':
    app = WebEntityAnalyzerApp()
    app.run()