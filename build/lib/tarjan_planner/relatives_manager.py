import json
import logging
import os
import pkgutil
from dataclasses import dataclass


@dataclass
class Relative:
    """Data class to store relative information."""
    name: str
    street_name: str
    district: str
    lat: float
    lng: float


class RelativesManager:
    """Class to manage relatives data."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.filePath = os.path.join(self.data_dir, self.file_name)

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.relatives, self.home = self.load_relatives()

    def load_relatives(self):
        """Load relatives from a JSON file."""
        try:
            relatives_data = pkgutil.get_data(__name__, f'data/{self.file_name}')
            if relatives_data:
                relatives_data = json.loads(relatives_data.decode('utf-8'))
                home_data = relatives_data.pop('home', None)
                home = Relative(name='home', **home_data) if home_data else None
                relatives = [Relative(name=rel, street_name=data['street_name'], district=data['district'],
                                      lat=data['lat'], lng=data['lng']) for rel, data in relatives_data.items()]
                return relatives, home
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading relatives {self.filePath}: {e}")
            print(f"Error loading relatives {self.filePath}: {e}")
            return None, None

    def show_all(self):
        """Print all relatives."""
        if self.relatives is None:
            return
        for rel in self.relatives:
            logging.info(
                f"Name: {rel.name}, Street Name: {rel.street_name}, District: {rel.district}, Latitude: {rel.lat}, Longitude: {rel.lng}")
            print(
                f"Name: {rel.name}, Street Name: {rel.street_name}, District: {rel.district}, Latitude: {rel.lat}, Longitude: {rel.lng}")

    def add(self, relative):
        """Add a new relative and save to file."""
        try:
            self.relatives.append(relative)
            self.save_relatives()
            print(f"Relative {relative.name} added successfully")
            logging.info(f"Relative {relative.name} added successfully")
        except Exception as e:
            print(f"Error adding relative {relative.name}: {e}")
            logging.error(f"Error adding relative {relative.name}: {e}")

    def delete(self, name):
        """Delete a relative by name and save to file."""
        try:
            if self.relatives is None:
                return
            self.relatives = [rel for rel in self.relatives if rel.name != name]
            self.save_relatives()
            print(f"Relative {name} deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting relative {name}: {e}")
            print(f"Error deleting relative {name}: {e}")

    def save_relatives(self):
        """Save relatives to a JSON file."""
        try:
            if self.relatives is None:
                return
            relatives_data = {
                rel.name: {'street_name': rel.street_name, 'district': rel.district, 'lat': rel.lat, 'lng': rel.lng} for
                rel in self.relatives}
            if self.home:
                relatives_data['home'] = {'street_name': self.home.street_name, 'district': self.home.district,
                                          'lat': self.home.lat, 'lng': self.home.lng}
            with open(self.filePath, 'w') as f:
                json.dump(relatives_data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving relatives {self.filePath}: {e}")
