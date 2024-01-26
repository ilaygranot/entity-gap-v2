import pandas as pd
import streamlit as st

class ConfigLoader:
    @staticmethod
    @st.cache_data
    def load_csv(file_path):
        return pd.read_csv(file_path)
