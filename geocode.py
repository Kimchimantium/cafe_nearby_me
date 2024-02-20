from json import JSONDecodeError

import requests
from dotenv import load_dotenv
import os
import json
from typing import Optional
from pprint import pprint

load_dotenv()

class GetGeo():
    def __init__(self):
        self.url = "https://maps.googleapis.com/maps/api/geocode/json?"
        self.data = None
# ===== Get Place Geocode =====
    def get_geo(self, address: str = '서울', filepath: str = 'geo.json', save: bool = False) -> Optional[dict]:
        """returns api response as json from Google place API
            save as file if save param set as True"""
        params = {
            "address": address,
            'key': os.environ.get('GOOGLE_API_KEY')
                }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            self.data = response.json()
            if save:
                try:
                    with open(filepath, 'r') as file:
                        existing_data = json.load(file)
                        print(existing_data)
                except (FileNotFoundError, JSONDecodeError):
                    existing_data = []
                existing_data.append(self.data)
                with open(filepath, 'w') as file:
                    json.dump(existing_data, file, indent=4)
            return self.data
        else:
            return None

    def get_lat_long(self, address: str='서울') -> list:
        """:returns [lat, long] list"""
        self.data = self.get_geo(address)
        lat = self.data['results'][0]['geometry']['viewport']['southwest']['lat']
        long = self.data['results'][0]['geometry']['viewport']['southwest']['lng']
        return [lat, long]
