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
        self.url_nearby = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        self.key = os.getenv('GOOGLE_API_KEY')
# ===== Get Place Geocode =====
    def get_geo(self, address: str = 'Jeju-Do', filepath: str = 'geo.json', save: bool = False) -> Optional[list]:
        """
        :param address: str address of the place to search default='Jeju-Do
        :param filepath: file name for the json to be saved as default='geo.json'
        :param save: saves if set True default=False
        :return: list ['lat', 'lng']
        """
        params = {
            "address": address,
            'key': self.key
                }
        response = requests.get(url=self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            if save:
                try:
                    with open(filepath, 'r') as file:
                        existing_data = json.load(file)
                        print(f"existing_data: {existing_data}")
                except (FileNotFoundError, JSONDecodeError):
                    existing_data = []
                existing_data.append(data)
                with open(filepath, 'w') as file:
                    json.dump(existing_data, file, indent=4)
            return data
        else:
            return None

    def by_geo(self, filepath: str = 'place.json', save: bool = False, address: str ='Jeju-Do', keyword: str = None, radius: int=500, type_: str='cafe') -> Optional[dict]:
        """
        :param filepath str filepath name  default='place.json'
        :param save set True to save response json as file, default=False
        :param address place to search for, passes to get_geo()
        :param keyword what to find in the address radius
        :param radius search radius by m² default=500
        :param type_ type of place to search e.g., 'cafe', 'restaurant'
        :returns api response as json from Google place API, save as file if save param set as True"""
        data = self.get_geo(address, save=True)
        print(f"data from get_geo: {data}")
        try:
            geo_list = [
                        data['results'][0]['geometry']['viewport']['southwest']['lat'],
                        data['results'][0]['geometry']['viewport']['southwest']['lng']
                        ]
            params = {
                'location': f"{geo_list[0]},{geo_list[1]}",
                'radius': radius,
                'type': type_,
                'key': self.key,
                'keyword': keyword
            }
            response = requests.get(url=self.url_nearby, params=params).json()
            print(response)
        except IndexError:
            response = {'results': []}

        if save:
            try:
                with open(filepath, 'r') as file:
                    existing_data = json.load(file)
            except (FileNotFoundError, JSONDecodeError):
                existing_data = []
            existing_data.append(response)
            with open(filepath, 'w') as file:
                json.dump(existing_data, file, indent=4, ensure_ascii=False)
        return response
