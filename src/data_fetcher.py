from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# Creating the Pandas DataFrame
header = ["id", 
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
          "longitude"]
df = pd.DataFrame(columns=header)

# Initializing Beautiful Soup object
url = "https://www.finn.no/realestate/homes/search.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Importing Data from website
pulled_json = soup.find("script", {"type": "application/json", "id": "__NEXT_DATA__"})
json_content = pulled_json.text.strip()
json = json.loads(json_content)

# Housing Information
housing_data = json["props"]["pageProps"]["search"]["docs"]

# Collecting a row of data
for house_data in housing_data:
    id = house_data.get("id", "N/A")
    location = house_data.get("location", "N/A")
    timestamp = house_data.get("timestamp", "N/A")
    price_suggestion = house_data.get("price_suggestion", {}).get("amount", "N/A")
    price_total = house_data.get("price_total", {}).get("amount", "N/A")
    house_size_sq_meters = house_data.get("area_range", {}).get("size_from", "N/A")
    plot_size_sq_meters = house_data.get("area_plot", {}).get("size", "N/A")
    organization_name = house_data.get("organisation_name", "N/A")
    local_area_name = house_data.get("local_area_name", "N/A")
    number_of_bedrooms = house_data.get("number_of_bedrooms", "N/A")
    owner_type_description = house_data.get("owner_type_description", "N/A")
    property_type_description = house_data.get("property_type_description", "N/A")
    latitude = house_data.get("coordinates", {}).get("lat", "N/A")
    longitude = house_data.get("coordinates", {}).get("lon", "N/A")

    # Append the data to the DataFrame
    row = pd.DataFrame([{
        "id": id,
        "location": location,
        "timestamp": timestamp,
        "price_suggestion": price_suggestion,
        "price_total": price_total,
        "house_size_sq_meters": house_size_sq_meters,
        "plot_size_sq_meters": plot_size_sq_meters,
        "organization_name": organization_name,
        "local_area_name": local_area_name,
        "number_of_bedrooms": number_of_bedrooms,
        "owner_type_description": owner_type_description,  
        "property_type_description": property_type_description,
        "latitude": latitude,
        "longitude": longitude
    }])
    df = pd.concat([df, row], ignore_index=True)
pass

