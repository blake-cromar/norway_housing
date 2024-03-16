from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np

class DataFetcher:
    """
    A class to fetch and parse housing data from Finn.no.

    Attributes:
    -----------
    header : list
        The header used for the dataset
    df : pandas.DataFrame
        Data frame to store housing data.
    url : str
        URL of the website to fetch data from.
    response : requests.models.Response
        The response from the URL
    soup : bs4.BeautifulSoup
        A soup object used to grab specific website data
    housing_data : list
        List to store parsed housing data.
    """

    def __init__(self):
        """
        Initializes the DataFetcher object and sets up initial data.
        """
        self.initialize_data()

    def initialize_data(self):
        """
        Initializes data attributes.
        """
        self.set_header()
        self.df = pd.DataFrame(columns=self.header)
        self.url = "https://www.finn.no/realestate/homes/search.html"
        self.get_response()
        self.parse_soup()
        self.housing_data = None

    def set_header(self):
        """
        Sets header for the data frame. The header consists of various attributes describing the housing data.
        """
        self.header = ["id", 
                       "location", 
                       "timestamp", 
                       "price_suggestion", 
                       "price_total", 
                       "house_size_sq_meters", 
                       "plot_size_sq_meters", 
                       "organization_name", 
                       "local_area_name", 
                       "number_of_bedrooms", 
                       "owner_type_description", 
                       "property_type_description", 
                       "latitude", 
                       "longitude"
                      ]

    def fetch_data(self):
        """
        Fetches and adds data to the data frame. This method pulls and parses the necessary data from the webpage and 
        adds it to the data frame.
        """
        self.pull_data()
        self.add_single_webpage_data()

    def get_response(self):
        """
        Fetches response from the URL. This method sends a GET request to the specified URL and retrieves the response.
        """
        self.response = requests.get(self.url)

    def parse_soup(self):
        """
        Parses the response text using BeautifulSoup. This method extracts structured data from the HTML content 
        retrieved from the webpage.
        """
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def pull_data(self):
        """
        Pulls JSON data from the parsed soup. This method locates and extracts JSON data embedded within the webpage and
        loads it into memory.
        """
        pulled_json = self.soup.find("script", {"type": "application/json", "id": "__NEXT_DATA__"})
        json_content = pulled_json.text.strip()
        loaded_json = json.loads(json_content)
        self.housing_data = loaded_json["props"]["pageProps"]["search"]["docs"]

    def add_single_webpage_data(self):
        """
        Adds single webpage data to the data frame. This method iterates through the parsed housing data and adds each 
        entry to the data frame.
        """
        for house_data in self.housing_data:
            self.df = pd.concat([
                self.df,
                pd.DataFrame([{
                    "id": house_data.get("id", "N/A"),
                    "location": house_data.get("location", "N/A"),
                    "timestamp": house_data.get("timestamp", "N/A"),
                    "price_suggestion": house_data.get("price_suggestion", {}).get("amount", "N/A"),
                    "price_total": house_data.get("price_total", {}).get("amount", "N/A"),
                    "house_size_sq_meters": house_data.get("area_range", {}).get("size_from", "N/A"),
                    "plot_size_sq_meters": house_data.get("area_plot", {}).get("size", "N/A"),
                    "organization_name": house_data.get("organisation_name", "N/A"),
                    "local_area_name": house_data.get("local_area_name", "N/A"),
                    "number_of_bedrooms": house_data.get("number_of_bedrooms", "N/A"),
                    "owner_type_description": house_data.get("owner_type_description", "N/A"),
                    "property_type_description": house_data.get("property_type_description", "N/A"),
                    "latitude": house_data.get("coordinates", {}).get("lat", "N/A"),
                    "longitude": house_data.get("coordinates", {}).get("lon", "N/A")
                }])
            ], ignore_index=True)

if __name__ == "__main__":
    data_fetcher = DataFetcher()
    data_fetcher.fetch_data()
    dataset = data_fetcher.df