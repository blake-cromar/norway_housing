from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import re
import math

class DataFetcher:
    """
    A class to fetch and parse housing data from Finn.no.

    Attributes:
    -----------
    header : list
        The header used for the dataset
    df : pandas.DataFrame
        Data frame to store housing data.
    main_url : str
        The main URL of the website to fetch data from.
    housing_data : list
        List to store parsed housing data.
    num_results_per_page : int
        Lists the number of results that appear on each page. Default at 50.
    """

    def __init__(self):
        """
        Initializes the DataFetcher object and sets up initial data.
        """
        self.set_header()
        self.df = pd.DataFrame(columns=self.header)
        self.main_webpage= "https://www.finn.no/realestate/homes/search.html?sort=RELEVANCE"
        self.housing_data = None
        self.num_results_per_page = 50
        self.number_of_pages = self.determine_number_of_pages()

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

    def determine_number_of_pages(self):
        """
        When making a search for housing only X number of results display per page. Determining the total number of
        pages to cycle through is important when collecting all the data.
        
        returns
        -------
        number_of_pages : int
            The total number of pages to cycle through.
        """
        
        # Grabbing the information on the webpage where it describes total number of house results
        soup = self.cook_soup(url=self.main_webpage)
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        description = meta_tag.get('content')
        
        # Extracting the total number of houses across all pages
        pattern = f'\d+'
        number_houses_str = re.findall(pattern, description)
        if number_houses_str:
            number_houses = int(number_houses_str[0])
        else:
            raise ValueError("No total number of houses found") 
        
        number_of_pages = math.ceil(number_houses / self.num_results_per_page)
        
        return number_of_pages
    
    def cook_soup(self, url):
        """
        Prepares a BeautifulSoup object that will be used for parsing data.
        
        Arguments
        ---------
        url : str
            The url we are going to create a soup object with.
            
        Returns
        -------
        bs4.BeautifulSoup
            A BeautifulSoup object used to pull information from a webpage
        """
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        return soup

    def pull_data(self):
        """
        Pulls JSON data from the parsed soup. This method locates and extracts JSON data embedded within the webpage and
        loads it into memory.
        """

        soup = self.cook_soup(url=self.main_webpage)
        pulled_json = soup.find("script", {"type": "application/json", "id": "__NEXT_DATA__"})
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