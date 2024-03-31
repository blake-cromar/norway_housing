from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from tqdm import tqdm
from data_manager import DataManager
import statistics

pd.set_option("future.no_silent_downcasting", True)

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
    max_number_of_pages : int
        Finn.no will only show results for a max X number of pages for a single query. Default at 50.
    data_manager : DataManager
        This objects assists by providing tools that help manipulate the data set.
    """
    def __init__(self):
        """
        Initializes the DataFetcher object and sets up initial data.
        """

        self.df = pd.DataFrame()
        self.main_webpage= "https://www.finn.no/realestate/homes/search.html?sort=RELEVANCE"
        self.max_number_of_pages = 50
        self.data_manager = DataManager()
        
    def compile_data(self):
        """
        Fetches and adds data to the data frame. This method pulls and parses the necessary data from the webpage and 
        adds it to the data frame. It will loop through all pages in the search Finn.no can provide.
        """
        
        # Initializing the progress bar
        progress_bar = tqdm(total=self.max_number_of_pages, desc="Processing", unit="page")
        
        # Grabbing the data
        for page_number in range(1, self.max_number_of_pages + 1):
            url = self.main_webpage + f'&page={page_number}'
            housing_data = self.pull_data(url=url)
            self.add_single_webpage_data(housing_data=housing_data)
            progress_bar.update(1)
            
        # Closing the progress bar
        progress_bar.close()
    
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

    def pull_data(self, url):
        """
        Pulls JSON data from the parsed soup. This method locates and extracts JSON data embedded within the webpage and
        loads it into memory.
        
        parameters
        ----------
        url : str
            The url that we will be pulling data from
        
        returns
        -------
        housing data : list
            The parsed JSON file containing the data on houses in the market.
        """

        soup = self.cook_soup(url=url)
        pulled_json = soup.find("script", {"type": "application/json", "id": "__NEXT_DATA__"})
        json_content = pulled_json.text.strip()
        loaded_json = json.loads(json_content)
        housing_data = loaded_json["props"]["pageProps"]["search"]["docs"]
        
        return housing_data

    def average_ranges(self, range_dictionary):
        """
        Takes a dictionary containing ranges for a metric and averages them.
        
        parameters
        ----------
        range_dictionary : dict
            A dictionary where the 2 first values of the key-value contain the range suggestions for a metric.
            
        returns
        -------
        average_value : int or "N/A"
            The average value 
        """
        try:
            from_to = list(range_dictionary.values())[:2]
            average_value = round(statistics.mean(from_to))
        except:
            average_value = "N/A"
        
        return average_value

    def add_single_webpage_data(self, housing_data):
        """
        Adds single webpage data to the data frame. This method iterates through the parsed housing data and adds each 
        entry to the data frame.
        
        parameters
        ----------
        housing_data : list
            Contains parsed housing data from the Finn.no webpage. While it's a list it contains information that
            comes in JSON form.
        """
        for house_data in housing_data:
            # Handling house price data
            price_suggestion = house_data.get("price_suggestion", {}).get("amount", "N/A")
            price_total = house_data.get("price_total", {}).get("amount", "N/A") 
            
            if price_suggestion == "N/A":
                price_suggestion_range = house_data.get("price_range_suggestion", "N/A")
                price_suggestion = self.average_ranges(range_dictionary=price_suggestion_range)
                
            if price_total == "N/A":
                price_total_range = house_data.get("price_range_total", "N/A")
                price_total = self.average_ranges(range_dictionary=price_total_range)
            
            # Modifying location data to pull out road and city data
            location_data = house_data.get("location", "N/A") 
            road, city = self.data_manager.location_string_splitter(location_data)
            
            # Converting millisecond date data to day, month, year
            milliseconds = house_data.get("timestamp", "N/A")
            day, month, year = self.data_manager.milliseconds_to_dates(timestamp_milli=milliseconds)
            
            # Compiling the data together
            self.df = pd.concat([
                self.df,
                pd.DataFrame([{
                    "id": house_data.get("id", "N/A"),
                    "road": road,
                    "city": city,
                    "day": day,
                    "month": month,
                    "year": year,
                    "price_suggestion": price_suggestion,
                    "price_total": price_total,
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
    data_fetcher.compile_data()
    dataset = data_fetcher.df