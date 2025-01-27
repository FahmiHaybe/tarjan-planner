import json
import logging
import os.path
import pkgutil
from dataclasses import dataclass


@dataclass
class Transport:
    name: str
    speed_kmh: float
    cost_per_km: float
    transfer_time_min: int


class TransportsManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.filePath = os.path.join(self.data_dir, self.file_name)

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.transports = self.load_transports()

    def load_transports(self):
        try:
            transports_data = pkgutil.get_data(__name__, f'data/{self.file_name}')
            if transports_data:
                transports_data = json.loads(transports_data.decode('utf-8'))
                return [Transport(name=mode, speed_kmh=data['speed_kmh'], cost_per_km=data['cost_per_km'],
                                  transfer_time_min=data['transfer_time_min']) for mode, data in
                        transports_data.items()]
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading transports {self.filePath}: {e}")
            return []

    def save_transports(self):
        try:
            if self.transports is None:
                return
            transports_data = {transport.name: {'speed_kmh': transport.speed_kmh, 'cost_per_km': transport.cost_per_km,
                                                'transfer_time_min': transport.transfer_time_min} for transport in
                               self.transports}
            with open(self.filePath, 'w') as f:
                json.dump(transports_data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving transports {self.filePath}: {e}")
            print(f"Error saving transports {self.filePath}: {e}")

    def show_all(self):
        if self.transports is None:
            return
        for transport in self.transports:
            info = f"Name: {transport.name}, Speed: {transport.speed_kmh} km/h, Cost: {transport.cost_per_km} per km, Transfer Time: {transport.transfer_time_min} min"
            logging.info(info)
            print(info)

    def add(self, transport):
        try:
            self.transports.append(transport)
            self.save_transports()
            print(f"Transport mode {transport.name} added successfully")
            logging.info(f"Transport mode {transport.name} added successfully")
        except Exception as e:
            logging.error(f"Error adding transport mode {transport.name}: {e}")
            print(f"Error adding transport mode {transport.name}: {e}")

    def get_transport(self, name):
        for transport in self.transports:
            if transport.name == name:
                logging.info(f"Transport mode {name} found")
                return transport
        logging.error(f"Transport mode {name} not found")
        return None

    def get_transports(self):
        return self.transports

    def delete(self, name):
        try:
            self.transports = [transport for transport in self.transports if transport.name != name]
            self.save_transports()
            logging.info(f"Transport mode {name} removed successfully")
            print(f"Transport mode {name} removed successfully")
        except Exception as e:
            logging.error(f"Error removing transport mode {name}: {e}")
            print(f"Error removing transport mode {name}: {e}")
