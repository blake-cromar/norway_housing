import datetime
import pytz

class DataManager():
    """
    Manipulates data involving the Norway Housing project.
    """
    def __init__(self):
        pass
    
    def location_string_splitter(self, location_string):
        """
        Takes the location information and splits it into a a street and city string. This will help make the 
        utilization of this string much easier.
        
        parameters
        ----------
        location_string : str
            A string containing the entire street and city information of the house.
        
        returns
        -------
        tuple
            Contains the location information of a house in (street, city) form. The comma from the original string is
            removed.
        """
        if location_string.count(',') == 0:
            road = "N/A"
            city = location_string
        else:
            last_comma_index = location_string.rfind(',')
            road = location_string[:last_comma_index]
            city = location_string[last_comma_index + 2:]  # Skip comma and space
            
        # It is likely not a road or city if a "|" is in the variable 
        road = "N/A" if "|" in road else road
        city = "N/A" if "|" in city else city
        
        return road, city
    
    def milliseconds_to_dates(self, timestamp_milli):
        """
        Takes dates that are representing as the number of milliseconds from January 1st, 1970.
        
        parameters
        ----------
        timestamp_milli : int
            The number of milliseconds from January 1st, 1970
            
        returns
        -------
        tuple
            A tuple of dates in the form (day, month, year).
        """
        
        # Converting the milliseconds to seconds
        timestamp_seconds = timestamp_milli / 1000
        
        # Transforming the second timestamp into readable dates
        norway_tz = pytz.timezone('Europe/Oslo')
        dt_object = datetime.datetime.fromtimestamp(timestamp_seconds, tz=norway_tz)
        
        # Extracting day, month, and year
        day = dt_object.day
        month = dt_object.strftime('%B')
        year = dt_object.year
        
        return day, month, year
        
        