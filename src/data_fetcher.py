from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

class DataFetcher():
    def __init__(self):
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

        self.df = pd.DataFrame(columns=self.header)
        self.url = "https://www.finn.no/realestate/homes/search.html"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.housing_data = None
    
    def fetch_data(self):
        self.pull_data()
        self.add_single_webpage_data()

    def pull_data(self):
        pulled_json = self.soup.find("script", {"type": "application/json", "id": "__NEXT_DATA__"})
        json_content = pulled_json.text.strip()
        loaded_json = json.loads(json_content)
        self.housing_data = loaded_json["props"]["pageProps"]["search"]["docs"]

    def add_single_webpage_data(self):
        for house_data in self.housing_data:
            # Append the data to the DataFrame
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