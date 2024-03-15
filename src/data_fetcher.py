from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# Creating the Pandas DataFrame
header = ["id", "location", "timestamp", "price_suggestion", "price_total", "price_shared_cost", "house_size_sq_meters", "plot_size_square_meters", "organization_name", "local_area_name", "number_of_bedrooms", "owner_type_description", "property_description", "latitude", "longitude"]
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
